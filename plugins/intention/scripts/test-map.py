#!/usr/bin/env python3
"""Focused verify: map.py prints intend-dag shape with live residue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "skills" / "map" / "scripts" / "map.py"
DROP_ENV = (
    "INTENTION_SESSION",
    "GROK_SESSION_ID",
    "CLAUDE_SESSION_ID",
    "CODEX_SESSION_ID",
)


def run(
    args: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MAP), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def test_fixture_epic() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {
                "id": "bazaar-6os",
                "title": "debrief: expand a finished or failed unit",
                "status": "open",
                "description": "Opposite analog of brief.",
            },
            "children": [
                {
                    "id": "bazaar-6os.1",
                    "title": "add-debrief-verb: opposite analog of brief",
                    "status": "closed",
                    "issue_type": "feature",
                    "close_reason": "act landed 3f054b9",
                    "dependencies": [],
                }
            ],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = proc.stdout
        expect("# debrief: expand a finished or failed unit" in out, out)
        expect("### bazaar-6os.1" in out, out)
        expect("Status: closed" in out, out)
        expect("act landed 3f054b9" in out, out)
        expect("## Ready-set" in out, out)
        expect("## Done" in out, out)
        expect("bazaar-6os.1" in out.split("## Done", 1)[1], out)


def test_unresolved_scope() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = {
            "epic": {"id": "nope", "title": "nope", "status": "missing"},
            "children": [],
        }
        path = Path(td) / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path), "nope"], cwd=Path(td))
        expect(proc.returncode == 1, proc.stdout)
        expect("unresolved" in proc.stderr, proc.stderr)


def test_index_not_a_dump() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu sibling host", "issue_type": "epic"},
                {"id": "bazaar-db8", "title": "Dossier becomes a Project", "issue_type": "epic"},
            ]
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = proc.stdout
        expect("# Intentions" in out, out)
        expect("`bazaar-tvm`" in out, out)
        expect("`bazaar-db8`" in out, out)
        expect("## DAG" not in out, out)
        expect("No current intention" in out, out)


def test_pin_current_and_reuse() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        fixture = {
            "epic": {"id": "bazaar-tvm", "title": "Tatastu", "status": "open"},
            "children": [
                {
                    "id": "bazaar-tvm.2",
                    "title": "add-tatastu-host: kernel ADR",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["--fixture", str(path), "--store", str(store), "--current", "bazaar-tvm"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("Current: `bazaar-tvm`" in proc.stdout, proc.stdout)
        expect("### bazaar-tvm.2" in proc.stdout, proc.stdout)
        pin = json.loads((store / "current.json").read_text(encoding="utf-8"))
        expect(pin["roots"] == ["bazaar-tvm"], pin)

        index = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu", "issue_type": "epic"},
                {"id": "bazaar-db8", "title": "Dossier", "issue_type": "epic"},
            ]
        }
        idx_path = root / "idx.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        listed = run(
            ["--fixture", str(idx_path), "--store", str(store)],
            cwd=root,
        )
        expect(listed.returncode == 0, listed.stderr + listed.stdout)
        expect("Current: `bazaar-tvm`" in listed.stdout, listed.stdout)
        expect("`bazaar-tvm` *" in listed.stdout, listed.stdout)


def test_peek_does_not_change_pin() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        store.mkdir()
        (store / "current.json").write_text(
            json.dumps({"roots": ["bazaar-tvm"]}),
            encoding="utf-8",
        )
        fixture = {
            "epic": {"id": "bazaar-db8", "title": "Dossier", "status": "open"},
            "children": [],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["bazaar-db8", "--fixture", str(path), "--store", str(store)],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("Current: `bazaar-tvm`" in proc.stdout, proc.stdout)
        expect("Peek: `bazaar-db8`" in proc.stdout, proc.stdout)
        pin = json.loads((store / "current.json").read_text(encoding="utf-8"))
        expect(pin["roots"] == ["bazaar-tvm"], pin)


def test_clear_current() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        store.mkdir()
        (store / "current.json").write_text(
            json.dumps({"roots": ["bazaar-tvm"]}),
            encoding="utf-8",
        )
        fixture = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu", "issue_type": "epic"},
            ]
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["--fixture", str(path), "--store", str(store), "--current", "-"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect(not (store / "current.json").is_file(), "pin still on disk")
        expect("No current intention" in proc.stdout, proc.stdout)


def test_current_needs_session() -> None:
    with tempfile.TemporaryDirectory() as td:
        env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
        proc = run(["--current", "bazaar-tvm"], cwd=Path(td), env=env)
        expect(proc.returncode == 2, proc.stderr + proc.stdout)
        expect("no session id" in proc.stderr, proc.stderr)


def main() -> int:
    tests = [
        test_fixture_epic,
        test_unresolved_scope,
        test_index_not_a_dump,
        test_pin_current_and_reuse,
        test_peek_does_not_change_pin,
        test_clear_current,
        test_current_needs_session,
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
