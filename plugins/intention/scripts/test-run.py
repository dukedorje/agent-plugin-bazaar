#!/usr/bin/env python3
"""Focused verify: empty ready-set prints a card and launches no worker."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE / "run.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUN), *args],
        text=True,
        capture_output=True,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def test_empty_ready_no_worker() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = Path(td) / "empty.json"
        fixture.write_text(
            json.dumps(
                {"ready": [], "waiting": [], "needs_advise": [], "ask": []}
            ),
            encoding="utf-8",
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


def test_until_advise() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = Path(td) / "adv.json"
        fixture.write_text(
            json.dumps(
                {
                    "ready": [{"id": "add-x"}],
                    "waiting": [],
                    "needs_advise": [{"id": "add-x"}],
                    "ask": [],
                }
            ),
            encoding="utf-8",
        )
        proc = run(["--ready-json", str(fixture), "--until", "advise", "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "advise", face)
        expect(face["workers_launched"] == 0, face)


def main() -> int:
    tests = [test_empty_ready_no_worker, test_until_advise]
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
