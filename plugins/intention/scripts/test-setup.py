#!/usr/bin/env python3
"""Focused verify: setup.py readies a fresh repo and is idempotent."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SETUP = Path(__file__).resolve().parents[1] / "skills" / "setup" / "scripts" / "setup.py"


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SETUP), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def states(proc: subprocess.CompletedProcess[str]) -> dict[str, str]:
    return {r["item"]: r["state"] for r in json.loads(proc.stdout)["rows"]}


def git_init(root: Path) -> None:
    subprocess.check_call(["git", "init", "-q"], cwd=root)


def test_not_git() -> None:
    with tempfile.TemporaryDirectory() as td:
        proc = run(["--json", "--root", td], cwd=Path(td))
        expect(proc.returncode == 2, proc.stdout + proc.stderr)
        expect(states(proc)["git repository"] == "missing", proc.stdout)


def test_no_bd_scaffolds_rest() -> None:
    """Without bd: report MISSING, still lay out openspec and gitignore."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        git_init(root)
        (root / ".gitignore").write_text("node_modules", encoding="utf-8")
        env = {**os.environ, "PATH": str(Path(shutil.which("git")).parent)}
        if shutil.which("bd", path=env["PATH"]):
            return  # bd shares git's dir; cannot hide it here
        check = run(["--check", "--json"], cwd=root, env=env)
        expect(check.returncode == 2, check.stdout)
        expect(not (root / "openspec").exists(), "--check wrote files")
        proc = run(["--json"], cwd=root, env=env)
        got = states(proc)
        expect(proc.returncode == 2, proc.stdout)
        expect(got["bd installed"] == "missing", got)
        expect(got["openspec layout"] == "fixed", got)
        for rel in ("specs", "changes/archive", "AGENTS.md", "parked.md"):
            expect((root / "openspec" / rel).exists(), rel)
        gi = (root / ".gitignore").read_text(encoding="utf-8")
        expect(gi.startswith("node_modules\n\n"), gi)
        expect(".worktrees/" in gi and ".spawns/" in gi, gi)
        expect("openspec/" in (root / "AGENTS.md").read_text(encoding="utf-8"), "pointer")
        again = states(run(["--json"], cwd=root, env=env))
        for item in ("openspec layout", ".gitignore", "agent instructions"):
            expect(again[item] == "ok", again)


def test_full_with_bd() -> None:
    if not shutil.which("bd"):
        print("skip: bd not installed")
        return
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        git_init(root)
        proc = run(["--json", "--prefix", "tst"], cwd=root)
        expect(proc.returncode == 0, proc.stdout + proc.stderr)
        got = states(proc)
        expect(got["beads initialized"] == "fixed", got)
        expect(got["bd custom types"] == "fixed", got)
        make = subprocess.run(
            ["bd", "create", "--type", "node", "probe-node", "-q"],
            cwd=root, text=True, capture_output=True,
        )
        expect(make.returncode == 0, make.stderr)
        again = run(["--check", "--json"], cwd=root)
        expect(again.returncode == 0, again.stdout)
        expect(set(states(again).values()) == {"ok"}, again.stdout)


def main() -> int:
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
