#!/usr/bin/env python3
"""Focused verify: run.py card + stage dispatch. No worker launched."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parents[0] / "skills" / "run" / "scripts" / "run.py"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUN), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def write_ready(td: Path, payload: dict) -> Path:
    fixture = td / "ready.json"
    fixture.write_text(json.dumps(payload), encoding="utf-8")
    return fixture


def test_empty_ready_no_worker() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
        expect(face["workers_launched"] == 0, face)
        expect(face["next"] is None, face)
        text = run(["--ready-json", str(fixture)])
        expect(text.returncode == 0, text.stderr)
        expect("RUN" in text.stdout, text.stdout)
        expect("workers 0" in text.stdout, text.stdout)


def test_missing_ready_py_is_no_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "missing": "ready.py",
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "no-ready", face)
        expect(face["workers_launched"] == 0, face)
        expect(face["next"] is None, face)


def test_missing_openspec_no_scope_is_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(
            [sys.executable, str(RUN), "--json"],
            text=True,
            capture_output=True,
            cwd=td,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
        expect(face["next"] is None, face)
        expect(face.get("missing") is None or face.get("missing") != "ready.py", face)


def test_scope_missing_dir_is_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-sheaf-type", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] is None, face)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-sheaf-type", face)
        expect(face["workers_launched"] == 0, face)


def test_advise_before_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [{"id": "add-x"}],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-x", face)
        expect(face["stop"] is None, face)


def test_until_advise_runs_read() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [{"id": "add-x"}],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--until", "advise", "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["stop"] is None, face)
        expect(face["workers_launched"] == 0, face)


def test_until_advise_does_not_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--until", "advise", "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_ready_is_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "act", face)
        expect(face["focus"] == "add-x", face)


def test_goal_scope_is_intend() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            [
                "we need extract-from on intend",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "intend", face)
        expect(face["stop"] is None, face)
        expect(face["workers_launched"] == 0, face)


def test_until_fold_when_legal() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-x", "--until", "fold", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "fold", face)
        expect(face["focus"] == "add-x", face)
        expect(face["workers_launched"] == 0, face)


def test_empty_does_not_fold_when_legal() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-x", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_pending_scope_does_not_flip() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [{"id": "add-x"}],
                "needs_advise": [],
                "ask": [],
            },
        )
        proc = run(["add-x", "--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "activation", face)
        expect(face["next"] is None, face)
        expect(face["focus"] == "add-x", face)


def main() -> int:
    tests = [
        test_empty_ready_no_worker,
        test_until_advise_runs_read,
        test_until_advise_does_not_act,
        test_missing_ready_py_is_no_ready,
        test_missing_openspec_no_scope_is_empty,
        test_scope_missing_dir_is_change,
        test_advise_before_act,
        test_ready_is_act,
        test_pending_scope_does_not_flip,
        test_goal_scope_is_intend,
        test_until_fold_when_legal,
        test_empty_does_not_fold_when_legal,
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
    print(f"pass {len(tests)} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
