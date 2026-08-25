#!/usr/bin/env python3
"""Focused verify: map.py prints intend-dag shape with live residue."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "skills" / "map" / "scripts" / "map.py"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MAP), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd),
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


def main() -> int:
    tests = [test_fixture_epic, test_unresolved_scope]
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
