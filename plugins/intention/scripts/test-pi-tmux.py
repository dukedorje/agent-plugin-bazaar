#!/usr/bin/env python3
"""Pi tmux adapter. No live session and no network."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import argparse
import contextlib
import io
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import pi_tmux  # noqa: E402
import routing  # noqa: E402
import spawn  # noqa: E402

SPAWN = SCRIPTS / "spawn.py"


def expect(cond: bool, detail: object) -> None:
    if not cond:
        raise AssertionError(detail)


def pane(transcript: str, composer: str = "") -> str:
    mid = composer if composer else ""
    return (
        transcript.rstrip()
        + "\n\n────────────────────────────────\n"
        + mid
        + "\n────────────────────────────────\n"
        + "~/hypersigil-store-frontend (feat/sveltekit-creative-tools)\n"
        + "↑99k ↓21k  gpt-6.1-sol • low\n"
    )


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now

    def sleep(self, sec: float) -> None:
        self.now += sec


def test_parse_idle_and_dirty() -> None:
    idle = pi_tmux.parse_pane(pane("Committed as f668c8f and pushed."))
    expect(idle["ok"] is True, idle)
    expect(idle["idle"] is True, idle)
    expect("f668c8f" in str(idle["transcript"]), idle)
    expect(idle["composer"] == "", idle)
    dirty = pi_tmux.parse_pane(pane("Committed as f668c8f.", composer="kb-time"))
    expect(dirty["idle"] is False, dirty)
    expect(dirty["composer"] == "kb-time", dirty)


def test_turn_streams_then_strips_marker() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        base = "Committed as f668c8f and pushed."
        user = pi_tmux.submit_line(str(root / "remote-prompt.md"))
        partial = base + "\n\n" + user + "\n\nLooking at the routes."
        final = partial + "\nThe studio links are in.\nINTENTION-DONE"
        (root / "frames.json").write_text(
            json.dumps([pane(base), pane(partial), pane(final)]),
            encoding="utf-8",
        )
        clock = Clock()
        stream = root / "stream.log"
        turn = pi_tmux.run_turn(
            pi_tmux.DirSession(root),
            "do the task",
            timeout_sec=30,
            stable_sec=12,
            marker_stable_sec=1,
            poll_sec=0.5,
            stream_path=stream,
            clock=clock,
            sleep=clock.sleep,
        )
        expect(turn.status == "pass", turn)
        expect("The studio links are in." in turn.answer, turn.answer)
        expect("INTENTION-DONE" not in turn.answer, turn.answer)
        expect("Looking at the routes." in stream.read_text(encoding="utf-8"), stream.read_text())
        ops = json.loads((root / "ops.json").read_text(encoding="utf-8"))
        expect(ops == [user], ops)
        expect((root / "remote-prompt.md").read_text(encoding="utf-8") == "do the task", "prompt")


def test_scrolled_pane_keeps_only_the_new_reply() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        user = pi_tmux.submit_line(str(root / "remote-prompt.md"))
        old = "Committed as f668c8f and pushed.\n\nA long previous answer that scrolled."
        final = old + "\n\n" + user + "\n\nread /tmp/intention-pi-prompt.md\n\npong\nINTENTION-DONE"
        (root / "frames.json").write_text(
            json.dumps([pane("Committed as f668c8f and pushed."), pane(final)]),
            encoding="utf-8",
        )
        clock = Clock()
        turn = pi_tmux.run_turn(
            pi_tmux.DirSession(root),
            "Reply with exactly the single word pong.\n",
            timeout_sec=30,
            marker_stable_sec=1,
            poll_sec=0.5,
            clock=clock,
            sleep=clock.sleep,
        )
        expect(turn.status == "pass", turn)
        expect("f668c8f" not in turn.answer, turn.answer)
        expect("pong" in turn.answer, turn.answer)
        expect("INTENTION-DONE" not in turn.answer, turn.answer)


def test_dirty_prompt_sends_nothing() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "frames.json").write_text(
            json.dumps([pane("idle text", composer="already typing")]),
            encoding="utf-8",
        )
        turn = pi_tmux.run_turn(
            pi_tmux.DirSession(root),
            "do the task",
            timeout_sec=5,
            clock=Clock(),
            sleep=lambda _sec: None,
        )
        expect(turn.status == "not-idle", turn)
        expect(not (root / "ops.json").exists(), "typed into a dirty composer")
        expect(not (root / "remote-prompt.md").exists(), "wrote prompt anyway")


def test_timeout_leaves_the_session() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "frames.json").write_text(
            json.dumps([pane("Committed as f668c8f.")]),
            encoding="utf-8",
        )
        clock = Clock()
        turn = pi_tmux.run_turn(
            pi_tmux.DirSession(root),
            "do the task",
            timeout_sec=1,
            poll_sec=0.5,
            clock=clock,
            sleep=clock.sleep,
        )
        expect(turn.status == "stall", turn)
        ops = json.loads((root / "ops.json").read_text(encoding="utf-8"))
        expect(len(ops) == 1, ops)
        expect("C-c" not in ops[0], ops)


def test_adapter_routing() -> None:
    env = {"PI_TMUX_SSH": "ssh example", "CODEX_BIN": "codex"}
    expect(routing.adapter_for("codex", env=env, which=lambda _b: "/codex") == "codex", "default stays codex")
    env["INTENTION_CODEX_VIA_PI"] = "1"
    expect(routing.adapter_for("codex", env=env, which=lambda _b: "/codex") == "pi", env)
    expect(routing.adapter_for("pi", env={"PI_TMUX_LOCAL": "1"}, which=lambda _b: None) == "pi", "local")
    expect(routing.adapter_for("pi", env={}, which=lambda _b: None) == "none", "unconfigured")


def test_spawn_face_and_lock() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prompt = root / "prompt.md"
        prompt.write_text("Reply with the single word pong.\n", encoding="utf-8")
        base = "Committed as f668c8f."
        user = pi_tmux.submit_line(str(root / "fake" / "remote-prompt.md"))
        final = base + "\n\n" + user + "\n\npong\nINTENTION-DONE"
        fake = root / "fake"
        fake.mkdir()
        (fake / "frames.json").write_text(
            json.dumps([pane(base), pane(final)]),
            encoding="utf-8",
        )
        spec = {
            "prompt_file": str(prompt),
            "adapter": "pi",
            "interface": "gpt-6.1-sol",
            "timeout_sec": 30,
            "workspace": str(root),
        }
        spec_path = root / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        env = {
            **os.environ,
            "PI_TMUX_FAKE_DIR": str(fake),
            "PI_TMUX_LOCK": str(root / "pi.lock"),
        }
        proc = subprocess.run(
            [sys.executable, str(SPAWN), "run", "--spec", str(spec_path), "--adapter", "pi"],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["disposition"] == "pass", face)
        expect(face["verify_command"] == "pi-tmux:fake", face)
        expect("pong" in face["summary"], face)
        last = (prompt.parent / "last.md").read_text(encoding="utf-8")
        expect(last.strip() == "pong", last)
        expect("INTENTION-DONE" not in last, last)
        # Held lock: a second spawn must not type.
        import fcntl

        fd = os.open(root / "pi.lock", os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            (fake / "ops.json").unlink()
            blocked = subprocess.run(
                [sys.executable, str(SPAWN), "run", "--spec", str(spec_path), "--adapter", "pi"],
                text=True,
                capture_output=True,
                env=env,
            )
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
        expect(blocked.returncode == 0, blocked.stderr + blocked.stdout)
        blocked_face = json.loads(blocked.stdout)
        expect(blocked_face["disposition"] == "infra-red", blocked_face)
        expect("pi-session-locked" in blocked_face["blockers"], blocked_face)
        expect(not (fake / "ops.json").exists(), "typed while locked")


class StageSession(pi_tmux.TmuxSession):
    """Record the seam without starting tmux, SSH, or a copy process."""

    def __init__(self, events: list, prefix: list[str], dirty: bool = False) -> None:
        super().__init__(prefix, "selected-pane", "/tmp/test-stage-prompt.md")
        self.events = events
        self.dirty = dirty
        self.submitted = ""

    def capture(self) -> str:
        self.events.append("capture")
        if self.submitted:
            return pane("previous\n" + self.submitted + "\nanswer\nINTENTION-DONE")
        return pane("previous", "typing" if self.dirty else "")

    def write_prompt(self, text: str) -> None:
        self.events.append(("write", text))

    def submit(self, line: str) -> None:
        self.events.append("submit")
        self.submitted = line


def test_stage_order_transport_delete_and_clock() -> None:
    for prefix in ([], ["ssh", "-J", "jump", "worker"]):
        events = []
        session = StageSession(events, prefix)
        clock = Clock()

        def runner(step, transport, name, timeout):
            events.append(("stage", step))
            expect(transport == prefix, transport)
            expect(name == session.session, name)
            expect(timeout == 600.0, timeout)
            # Stage time is owned by the runner, outside the turn clock.
            clock.sleep(601)
            return 0

        steps = [{"src": "one", "dest": "/one"},
                 {"src": "two", "dest": "/two", "delete": False},
                 {"src": "three", "dest": "/three", "delete": True}]
        with patch.dict(os.environ, {"PI_TMUX_DELETE": "1"}):
            turn = pi_tmux.run_turn(
                session, "task", stage=steps, stage_runner=runner,
                marker_stable_sec=0, clock=clock, sleep=clock.sleep,
            )
        expect(turn.status == "pass", turn)
        expect(events[:6] == ["capture",
               ("stage", {"src": "one", "dest": "/one", "delete": False}),
               ("stage", {"src": "two", "dest": "/two", "delete": False}),
               ("stage", {"src": "three", "dest": "/three", "delete": True}),
               ("write", "task"), "submit"], events)
        expect("delete" not in steps[0], "runner normalization mutated the packet")


def malformed_stages() -> list:
    return [None, False, {}, "", [None], [[]], [{}],
            [{"src": "tree"}], [{"dest": "/tree"}],
            [{"src": "", "dest": "/tree"}],
            [{"src": "tree", "dest": 1}],
            [{"src": "tree", "dest": "/tree", "delete": "true"}],
            [{"src": "tree", "dest": "/tree", "delete": 1}],
            [{"src": "tree", "dest": "/tree", "extra": True}],
            [{"src": "valid", "dest": "/valid"}, {"src": "missing-dest"}]]


def test_stage_validates_every_entry_before_running() -> None:
    for stage in malformed_stages():
        events = []
        runner = lambda *args: events.append("stage") or 0
        turn = pi_tmux.run_turn(StageSession(events, []), "task",
                                stage=stage, stage_runner=runner)
        expect(turn.status == "stage-failed", (stage, turn))
        expect(events == ["capture"], (stage, events))


def test_stage_failures_stop_before_prompt() -> None:
    steps = [{"src": "one", "dest": "/one"}, {"src": "two", "dest": "/two"}]
    for failure in (1, OSError("launch failed"), RuntimeError("transport failed"),
                    TimeoutError("deadline"), subprocess.TimeoutExpired("copy", 7),
                    subprocess.CalledProcessError(2, "copy")):
        events = []

        def runner(*args):
            events.append("stage")
            if isinstance(failure, Exception):
                raise failure
            return failure

        turn = pi_tmux.run_turn(StageSession(events, []), "task", stage=steps,
                                stage_runner=runner, timeout_sec=7)
        expect(turn.status == "stage-failed", turn)
        expect(events == ["capture", "stage"], events)
    events = []
    turn = pi_tmux.run_turn(StageSession(events, []), "task", stage=steps)
    expect(turn.status == "stage-failed", turn)
    expect(events == ["capture"], events)


def test_empty_stage_and_dirty_composer() -> None:
    for stage in (pi_tmux.NO_STAGE, []):
        events = []
        clock = Clock()
        turn = pi_tmux.run_turn(StageSession(events, []), "task", stage=stage,
                                marker_stable_sec=0, clock=clock, sleep=clock.sleep)
        expect(turn.status == "pass", turn)
        expect(events[:3] == ["capture", ("write", "task"), "submit"], events)
    for stage in ([{"src": "tree", "dest": "/tree"}], None):
        events = []
        turn = pi_tmux.run_turn(StageSession(events, [], dirty=True), "task",
                                stage=stage, stage_runner=lambda *args: events.append("stage"))
        expect(turn.status == "not-idle", turn)
        expect(events == ["capture"], events)


def stage_packet(root: Path, stage=pi_tmux.NO_STAGE) -> dict:
    """Exercise the actual packet -> cmd_stage -> on-disk spec boundary."""
    example = SCRIPTS.parents[2] / "docs/contracts/examples/density-explicit.packet.json"
    packet = json.loads(example.read_text(encoding="utf-8"))
    if stage is not pi_tmux.NO_STAGE:
        packet["stage"] = stage
    packet_path = root / "packet.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    args = argparse.Namespace(packet=packet_path, node=None, surface=None, root=root, timeout=7)
    with contextlib.redirect_stdout(io.StringIO()) as output:
        expect(spawn.cmd_stage(args) == 0, "cmd_stage")
    staged = json.loads(output.getvalue())
    return json.loads(Path(staged["spec_file"]).read_text(encoding="utf-8"))


def test_packet_stage_schema_and_spec() -> None:
    import jsonschema

    contracts = SCRIPTS.parents[2] / "docs/contracts"
    schema = json.loads((contracts / "agent-surface.schema.json").read_text(encoding="utf-8"))
    target = {"$ref": "#/$defs/taskPacket", "$defs": schema["$defs"]}
    validator = jsonschema.Draft7Validator(target)
    for stage in (pi_tmux.NO_STAGE, [], [{"src": "tree", "dest": "/tree"}],
                  [{"src": "tree", "dest": "/tree", "delete": True}],
                  *malformed_stages()):
        with tempfile.TemporaryDirectory() as td:
            spec = stage_packet(Path(td), stage)
            packet = json.loads(Path(spec["packet_file"]).read_text(encoding="utf-8"))
            errors = list(validator.iter_errors(packet))
            if stage is pi_tmux.NO_STAGE:
                expect(not errors and "stage" not in spec and "stage_error" not in spec, spec)
            elif errors:
                expect("stage_error" in spec and "stage" not in spec, (stage, spec))
            else:
                expect(spec.get("stage") == stage and "stage_error" not in spec, spec)


def test_packet_to_turn_face_and_lock_release() -> None:
    steps = [{"src": "one", "dest": "/one"}, {"src": "two", "dest": "/two"}]
    cases = [(steps, "success", False, False, None),
             (steps, "missing", False, False, "pi-stage-failed"),
             (steps, "nonzero", False, False, "pi-stage-failed"),
             (steps, "timeout", False, False, "pi-stage-failed"),
             (steps, "launch", False, False, "pi-stage-failed"),
             (steps, "transport", False, False, "pi-stage-failed"),
             (steps, "success", True, False, "pi-session-not-idle"),
             (steps, "success", False, True, "pi-session-locked"),
             ([], "missing", False, False, None),
             (pi_tmux.NO_STAGE, "missing", False, False, None)]
    cases.extend((stage, "success", False, False, "pi-stage-failed")
                 for stage in malformed_stages())
    for stage, mode, dirty, locked, blocker in cases:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            spec = stage_packet(root, stage)
            prompt = Path(spec["prompt_file"])
            events = []
            session = StageSession(events, ["ssh", "worker"], dirty)
            lock_path = root / "pi.lock"
            clock = Clock()
            real_turn = pi_tmux.run_turn

            def fast_turn(*args, **kwargs):
                expect(pi_tmux.try_lock(lock_path) is None, "turn ran without lock")
                return real_turn(*args, **kwargs, marker_stable_sec=0,
                                 clock=clock, sleep=clock.sleep)

            def runner(step, transport, name, timeout):
                expect(pi_tmux.try_lock(lock_path) is None, "stage ran without lock")
                expect(transport == session.prefix and name == session.session, (transport, name))
                expect(timeout == 7, timeout)
                events.append(("stage", step))
                if mode == "timeout":
                    raise subprocess.TimeoutExpired("copy", timeout)
                if mode == "launch":
                    raise OSError("launch failed")
                if mode == "transport":
                    raise RuntimeError("transport failed")
                return 1 if mode == "nonzero" else 0

            held = pi_tmux.try_lock(lock_path) if locked else None
            try:
                with patch.dict(os.environ, {"PI_TMUX_LOCK": str(lock_path)}), \
                     patch.object(pi_tmux, "session_from_env", return_value=session), \
                     patch.object(pi_tmux, "STAGE_RUNNER", None if mode == "missing" else runner), \
                     patch.object(pi_tmux, "run_turn", side_effect=fast_turn), \
                     patch.object(routing, "record_execution"), \
                     contextlib.redirect_stdout(io.StringIO()) as output:
                    expect(spawn.run_pi(spec, prompt, root / "raw.log", root / "face.json") == 0, spec)
            finally:
                if held is not None:
                    pi_tmux.unlock(held)
            face = json.loads(output.getvalue())
            expect(face == json.loads((root / "face.json").read_text()), face)
            expect(face["blockers"] == ([blocker] if blocker else []), (mode, stage, face))
            if blocker:
                expect(face["disposition"] == "infra-red", face)
                expect("submit" not in events and not any(e[0] == "write" for e in events), events)
                count = sum(isinstance(e, tuple) and e[0] == "stage" for e in events)
                expect(count == (1 if mode in {"nonzero", "timeout", "launch", "transport"} else 0), events)
            else:
                expect(face["disposition"] == "pass", face)
                stage_events = [e for e in events if isinstance(e, tuple) and e[0] == "stage"]
                expect(len(stage_events) == (len(stage) if isinstance(stage, list) else 0), events)
                expect(events.index("submit") > events.index(("write", prompt.read_text())), events)
            if locked:
                expect(events == [], events)
            probe = pi_tmux.try_lock(lock_path)
            expect(probe is not None, "session lock leaked")
            pi_tmux.unlock(probe)


def main() -> int:
    tests = [
        test_parse_idle_and_dirty,
        test_turn_streams_then_strips_marker,
        test_scrolled_pane_keeps_only_the_new_reply,
        test_dirty_prompt_sends_nothing,
        test_timeout_leaves_the_session,
        test_adapter_routing,
        test_spawn_face_and_lock,
        test_stage_order_transport_delete_and_clock,
        test_stage_validates_every_entry_before_running,
        test_stage_failures_stop_before_prompt,
        test_empty_stage_and_dirty_composer,
        test_packet_stage_schema_and_spec,
        test_packet_to_turn_face_and_lock_release,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"pass {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    if failed:
        print(f"FAIL {failed}/{len(tests)}")
        return 1
    print(f"ok {len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
