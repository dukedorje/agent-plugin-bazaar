#!/usr/bin/env python3
"""Pi tmux adapter. No live session and no network."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import pi_tmux  # noqa: E402
import routing  # noqa: E402

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


def main() -> int:
    tests = [
        test_parse_idle_and_dirty,
        test_turn_streams_then_strips_marker,
        test_dirty_prompt_sends_nothing,
        test_timeout_leaves_the_session,
        test_adapter_routing,
        test_spawn_face_and_lock,
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
