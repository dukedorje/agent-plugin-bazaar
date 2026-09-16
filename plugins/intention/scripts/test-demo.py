#!/usr/bin/env python3
"""Focused verify: demo.py presents a journey and invents no tracker."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

DEMO = Path(__file__).resolve().parents[1] / "skills" / "demo" / "scripts" / "demo.py"


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DEMO), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd),
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def test_inflight_journey() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "change_id": "add-run-wave-workflow",
            "proposal": (
                "# add-run-wave-workflow\n\n"
                "> **ACTIVE BUILD**\n\n"
                "## User journey & surfaces\n\n"
                "Duke runs the wave from a Grok tab.\n\n"
                "## Out of scope\n"
            ),
            "tasks": "- [ ] EYES: one real two-node wave. Next: /run-wave\n",
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = proc.stdout
        expect("YOUR DEMO" in out, out)
        expect("halt" in out, out)
        expect("Duke runs the wave" in out, out)
        expect("/run-wave" in out, out)
        expect("Do not fold" in out, out)
        expect(not (root / "demo.md").exists(), "wrote demo.md")
        expect(not list(root.glob("**/demo.md")), "wrote demo.md somewhere")


def test_archive_not_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "change_id": "add-run-wave-workflow",
            "archived": True,
            "proposal": (
                "## User journey & surfaces\n\n"
                "Try the folded wave.\n"
            ),
            "tasks": "- [x] EYES: look. Next: /run-wave\n",
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("empty" not in proc.stdout.split("YOUR DEMO", 1)[-1][:80], proc.stdout)
        expect("archive" in proc.stdout, proc.stdout)
        expect("Try the folded wave" in proc.stdout, proc.stdout)


def test_empty_unknown() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {"change_id": ""}
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("YOUR DEMO · empty" in proc.stdout, proc.stdout)
        expect("`/status`" in proc.stdout, proc.stdout)
        expect(not (root / "demo.md").exists(), "empty wrote demo.md")


def test_live_archive_resolve() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        dest = root / "openspec" / "changes" / "archive" / "2026-09-02-add-live-demo"
        dest.mkdir(parents=True)
        (dest / "proposal.md").write_text(
            "# add-live-demo\n\n## User journey & surfaces\n\nFrom archive.\n",
            encoding="utf-8",
        )
        (dest / "tasks.md").write_text(
            "- [x] EYES: look. Next: /status\n",
            encoding="utf-8",
        )
        proc = run(["add-live-demo"], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("From archive" in proc.stdout, proc.stdout)
        expect("archive" in proc.stdout, proc.stdout)
        expect("YOUR DEMO · empty" not in proc.stdout, proc.stdout)


def main() -> int:
    tests = [
        test_inflight_journey,
        test_archive_not_empty,
        test_empty_unknown,
        test_live_archive_resolve,
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
