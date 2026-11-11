#!/usr/bin/env python3
"""Drive the shared Pi tmux session.

A CLI harness (codex exec, claude -p) is a fresh process. Intention sends
the prompt on stdin and reads stdout only after the process exits. This
session is the opposite: one already-running TUI. Keys go in with tmux,
and the screen is the stream. Timeout must not send Ctrl-C, because that
stops Pi itself.

Completion is the pane going quiet at the idle footer, or a reply line
that is exactly INTENTION-DONE. Partial text is appended to stream.log
while that wait runs. The final answer is still one string, matching the
face.json contract callers already parse.
"""

from __future__ import annotations

import fcntl
import json
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

MARKER = "INTENTION-DONE"
BUFFER = "intention-pi"
DEFAULT_PROMPT_PATH = "/tmp/intention-pi-prompt.md"
DEFAULT_SESSION = "pi"
NO_STAGE = object()
# Registered by the copy implementation. Each invocation owns timeout_sec.
# Arguments: normalized step, SSH argv ([] for local), session, timeout_sec.
StageRunner = Callable[[dict[str, str | bool], list[str], str, float], int]
STAGE_RUNNER: StageRunner | None = None


def rsync_argv(step: dict[str, str | bool], ssh_argv: list[str]) -> list[str]:
    """rsync argv for one normalized step. Last ssh_argv item is the host."""
    argv = ["rsync", "-a"]
    if step["delete"] is True:
        argv.append("--delete")
    if not ssh_argv:
        return [*argv, str(step["src"]), str(step["dest"])]
    host = ssh_argv[-1]
    return [*argv, "-e", shlex.join(ssh_argv[:-1]), str(step["src"]),
            f"{host}:{step['dest']}"]


def rsync_runner(step: dict[str, str | bool], ssh_argv: list[str],
                 session: str, timeout_sec: float) -> int:
    """Copy src to dest with rsync. Non-zero on missing src, failure, or timeout."""
    if not os.path.exists(str(step["src"])):
        return 1
    try:
        done = subprocess.run(rsync_argv(step, ssh_argv), stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=timeout_sec, check=False)
    except subprocess.TimeoutExpired:
        return 124
    return done.returncode


# Executed on the session machine, never on the conductor for an SSH pane.
# exec keeps mount inspection and rsync within the caller's single timeout.
STORE_COPY_SCRIPT = r"""
import os
import re
import sys

store, dest, delete = sys.argv[1:]
resolved = os.path.realpath(store)
if resolved == "/" or not os.path.isdir(resolved):
    sys.exit(1)

def unescape(value):
    return re.sub(r"\\([0-7]{3})", lambda m: chr(int(m[1], 8)), value)

mounts = []
with open("/proc/self/mountinfo", encoding="utf-8") as report:
    for line in report:
        fields, filesystem = line.split(" - ", 1)
        mountpoint = unescape(fields.split()[4])
        if resolved == mountpoint or resolved.startswith(mountpoint.rstrip("/") + "/"):
            mounts.append((mountpoint, filesystem.split()[0]))
if not mounts:
    sys.exit(1)
mountpoint, filesystem = max(mounts, key=lambda mount: len(mount[0]))
if mountpoint == "/" or filesystem != "virtiofs":
    sys.exit(1)
argv = ["rsync", "-a"]
if delete == "true":
    argv.append("--delete")
# Match rsync's no-trailing-slash source shape explicitly even on openrsync:
# an existing destination contains the source basename; an absent one is
# the copied directory itself.
source = os.path.normpath(store)
if not os.path.exists(dest):
    source += "/"
argv.extend(["--", source, dest])
os.execvp(argv[0], argv)
"""


def store_copy_argv(step: dict[str, str | bool], ssh_argv: list[str]) -> list[str]:
    argv = ["python3", "-c", STORE_COPY_SCRIPT, str(step["store"]),
            str(step["dest"]), "true" if step["delete"] is True else "false"]
    # SSH joins its command arguments into shell text. Send one fully quoted
    # command so scripts and paths (including spaces) remain single arguments.
    return [*ssh_argv, shlex.join(argv)] if ssh_argv else argv


def store_runner(step: dict[str, str | bool], ssh_argv: list[str],
                 session: str, timeout_sec: float) -> int:
    """Check the session mount before copying or pruning on that machine."""
    try:
        done = subprocess.run(store_copy_argv(step, ssh_argv), stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=timeout_sec, check=False)
    except subprocess.TimeoutExpired:
        return 124
    return done.returncode


def stage_runner(step: dict[str, str | bool], ssh_argv: list[str],
                 session: str, timeout_sec: float) -> int:
    runner = store_runner if "store" in step else rsync_runner
    return runner(step, ssh_argv, session, timeout_sec)


def validate_stage(stage: object) -> None:
    """Reject the whole declaration before any step can run."""
    if not isinstance(stage, list):
        raise ValueError("stage must be an array")
    for index, step in enumerate(stage):
        if not isinstance(step, dict) or set(step) - {"src", "store", "dest", "delete"}:
            raise ValueError(f"stage[{index}] must be a closed src-or-store/dest/delete object")
        if ("src" in step) == ("store" in step):
            raise ValueError(f"stage[{index}] must name exactly one of src or store")
        selector = "src" if "src" in step else "store"
        for field in (selector, "dest"):
            if not isinstance(step.get(field), str) or not step[field]:
                raise ValueError(f"stage[{index}].{field} must be a non-empty string")
        if "delete" in step and not isinstance(step["delete"], bool):
            raise ValueError(f"stage[{index}].delete must be boolean")


def submit_line(prompt_path: str) -> str:
    return (
        f"Read {prompt_path} and carry out that task. "
        f"End with a line that is exactly {MARKER}."
    )


def is_rule(line: str) -> bool:
    text = line.strip()
    return len(text) >= 8 and set(text) <= {"─", "━", "-"}


def parse_pane(text: str) -> dict[str, object]:
    """Split a capture-pane into transcript, composer, and footer.

    Pi's idle screen ends with two horizontal rules (the composer sits
    between them), a path line, and a status line containing '•'.
    A non-empty composer means someone is already typing.
    """
    lines = text.splitlines()
    rules = [i for i, line in enumerate(lines) if is_rule(line)]
    if len(rules) < 2:
        return {
            "ok": False,
            "idle": False,
            "transcript": text.strip(),
            "composer": "",
            "footer": "",
        }
    start, end = rules[-2], rules[-1]
    composer = "\n".join(lines[start + 1 : end]).strip()
    transcript = "\n".join(lines[:start]).strip()
    tail = [line for line in lines[end + 1 :] if line.strip()]
    path = tail[0] if tail else ""
    footer = tail[-1] if tail else ""
    idle = (
        not composer
        and "•" in footer
        and (path.startswith("~") or path.startswith("/") or "/" in path)
    )
    return {
        "ok": True,
        "idle": idle,
        "transcript": transcript,
        "composer": composer,
        "footer": footer,
    }


def added_text(before: str, after: str) -> str:
    before = before.strip()
    after = after.strip()
    if not after or after == before:
        return ""
    if before and after.startswith(before):
        return after[len(before) :].strip()
    if before and before in after:
        return after.split(before, 1)[1].strip()
    return after


def has_marker(text: str) -> bool:
    return any(line.strip() == MARKER for line in text.splitlines())


def strip_marker(text: str) -> str:
    lines = text.splitlines()
    while lines and lines[-1].strip() == MARKER:
        lines.pop()
    return "\n".join(lines).strip()


def reply_region(transcript: str, submitted: str, base: str) -> str:
    """Text after the pasted instruction.

    A TUI scroll means the new capture is not a prefix of the old one.
    The instruction line is the cut, wherever it sits on screen.
    """
    text = transcript.strip()
    lead = submitted.strip()
    if lead and lead in text:
        return text.rsplit(lead, 1)[1].strip()
    return added_text(base, text)


@dataclass
class Turn:
    status: str
    answer: str
    detail: str
    raw: str
    session: str


class DirSession:
    """Frame script for tests. frames.json is a list of pane captures."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.session = "fake"
        self.prefix: list[str] = []
        self.prompt_path = str(root / "remote-prompt.md")
        self._n = 0

    def capture(self) -> str:
        frames = json.loads((self.root / "frames.json").read_text(encoding="utf-8"))
        frame = frames[min(self._n, len(frames) - 1)]
        self._n += 1
        return frame

    def write_prompt(self, text: str) -> None:
        (self.root / "remote-prompt.md").write_text(text, encoding="utf-8")

    def submit(self, line: str) -> None:
        path = self.root / "ops.json"
        ops = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []
        ops.append(line)
        path.write_text(json.dumps(ops), encoding="utf-8")


class TmuxSession:
    """Local tmux, or ssh prefix + remote tmux. The prompt is a file, not keys."""

    def __init__(self, prefix: list[str], session: str, prompt_path: str) -> None:
        self.prefix = prefix
        self.session = session
        self.prompt_path = prompt_path

    def _run(self, argv: list[str], stdin: str | None = None) -> str:
        cmd = [*self.prefix, "--", *argv] if self.prefix else argv
        proc = subprocess.run(
            cmd,
            input=stdin,
            text=True,
            capture_output=True,
            timeout=45,
            check=False,
        )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(detail or f"exit {proc.returncode}")
        return proc.stdout

    def capture(self) -> str:
        return self._run(["tmux", "capture-pane", "-t", self.session, "-p", "-S", "-400"])

    def write_prompt(self, text: str) -> None:
        if self.prefix:
            quoted = shlex.quote(self.prompt_path)
            self._run(["bash", "-c", f"cat > {quoted}"], stdin=text)
            return
        path = Path(self.prompt_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def submit(self, line: str) -> None:
        self._run(["tmux", "load-buffer", "-b", BUFFER, "-"], stdin=line)
        self._run(
            ["tmux", "paste-buffer", "-t", self.session, "-b", BUFFER, "-d"]
        )
        self._run(["tmux", "send-keys", "-t", self.session, "Enter"])


def default_lock_path(env: dict[str, str] | None = None) -> Path:
    env = os.environ if env is None else env
    raw = (env.get("PI_TMUX_LOCK") or "").strip()
    if raw:
        return Path(raw)
    return Path.home() / ".intention" / "pi-tmux.lock"


def try_lock(path: Path):
    """Non-blocking exclusive lock. None means another spawn holds the pane."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        return None
    return fd


def unlock(fd: int) -> None:
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def session_from_env(env: dict[str, str] | None = None) -> DirSession | TmuxSession:
    env = os.environ if env is None else env
    fake = (env.get("PI_TMUX_FAKE_DIR") or "").strip()
    if fake:
        return DirSession(Path(fake))
    session = (env.get("PI_TMUX_SESSION") or DEFAULT_SESSION).strip() or DEFAULT_SESSION
    prompt_path = (env.get("PI_TMUX_PROMPT_PATH") or DEFAULT_PROMPT_PATH).strip()
    ssh = (env.get("PI_TMUX_SSH") or "").strip()
    if ssh:
        return TmuxSession(shlex.split(ssh), session, prompt_path)
    if (env.get("PI_TMUX_LOCAL") or "").strip() == "1":
        return TmuxSession([], session, prompt_path)
    raise RuntimeError("pi tmux is not configured (set PI_TMUX_SSH or PI_TMUX_LOCAL=1)")


def _publish(stream_path: Path | None, written: str, suffix: str) -> str:
    if stream_path is None or not suffix or suffix == written:
        return written
    stream_path.parent.mkdir(parents=True, exist_ok=True)
    if suffix.startswith(written):
        chunk = suffix[len(written) :]
    else:
        chunk = "\n" + suffix
    if chunk:
        with stream_path.open("a", encoding="utf-8") as handle:
            handle.write(chunk)
    return suffix


def run_turn(
    session: DirSession | TmuxSession,
    prompt: str,
    *,
    timeout_sec: float = 600.0,
    stable_sec: float = 12.0,
    marker_stable_sec: float = 1.0,
    poll_sec: float = 0.4,
    stream_path: Path | None = None,
    stage: object = NO_STAGE,
    stage_error: str | None = None,
    stage_runner: StageRunner | None = None,
    clock=time.monotonic,
    sleep=time.sleep,
) -> Turn:
    """Paste one line that points at the prompt file. Do not send Ctrl-C."""
    name = getattr(session, "session", DEFAULT_SESSION)
    try:
        first = parse_pane(session.capture())
    except (OSError, RuntimeError) as exc:
        return Turn("error", "", str(exc), "", name)
    if not first["ok"] or not first["idle"]:
        return Turn(
            "not-idle",
            "",
            "Pi is not at an empty prompt. No keys were sent.",
            str(first["transcript"]),
            name,
        )
    base = str(first["transcript"])
    try:
        if stage_error is not None:
            raise ValueError(stage_error)
        if stage is not NO_STAGE:
            validate_stage(stage)
            runner = stage_runner if stage_runner is not None else STAGE_RUNNER
            if stage and runner is None:
                raise ValueError("stage declared but no runner is registered")
            for step in stage:
                selector = "src" if "src" in step else "store"
                normalized = {selector: step[selector], "dest": step["dest"],
                              "delete": step.get("delete", False)}
                code = runner(normalized, list(session.prefix), name, timeout_sec)
                if code != 0:
                    raise ValueError(f"stage runner failed (exit {code})")
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return Turn("stage-failed", "", str(exc), base, name)

    submitted = submit_line(str(session.prompt_path))
    try:
        session.write_prompt(prompt)
        session.submit(submitted)
    except (OSError, RuntimeError) as exc:
        return Turn("error", "", str(exc), base, name)

    start = clock()
    prev = ""
    written = ""
    stable_since: float | None = None
    last_raw = base
    while True:
        now = clock()
        if now - start >= timeout_sec:
            return Turn(
                "stall",
                strip_marker(prev),
                f"Pi did not finish within {timeout_sec}s. The session was left running.",
                last_raw,
                name,
            )
        sleep(poll_sec)
        try:
            raw = session.capture()
        except (OSError, RuntimeError) as exc:
            return Turn("error", strip_marker(prev), str(exc), last_raw, name)
        last_raw = raw
        pane = parse_pane(raw)
        suffix = reply_region(str(pane["transcript"]), submitted, base)
        written = _publish(stream_path, written, suffix)
        if suffix != prev:
            prev = suffix
            stable_since = clock()
            continue
        if not suffix or stable_since is None:
            continue
        held = clock() - stable_since
        if has_marker(suffix) and held >= marker_stable_sec:
            return Turn("pass", strip_marker(suffix), "marker", last_raw, name)
        if pane["idle"] and held >= stable_sec:
            return Turn("pass", strip_marker(suffix), "idle", last_raw, name)
