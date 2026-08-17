#!/usr/bin/env python3
"""Focused verify for export-graph.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPORT = HERE / "export-graph.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXPORT), *args],
        text=True,
        capture_output=True,
    )


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    inv = {
        "nodes": [
            {
                "id": "a",
                "title": "open child",
                "status": "open",
                "issue_type": "task",
                "dependencies": [
                    {
                        "issue_id": "a",
                        "depends_on_id": "b",
                        "type": "blocks",
                    },
                    {
                        "issue_id": "a",
                        "depends_on_id": "parked",
                        "type": "blocks",
                    },
                    {
                        "issue_id": "a",
                        "depends_on_id": "epic",
                        "type": "parent-child",
                    },
                ],
            },
            {"id": "b", "title": "closed dep", "status": "closed", "issue_type": "task"},
            {"id": "parked", "title": "parked", "status": "parked", "issue_type": "task"},
            {"id": "epic", "title": "the epic", "status": "open", "issue_type": "epic"},
            {"id": "def", "title": "deferred", "status": "deferred", "issue_type": "task"},
        ]
    }
    failed = 0
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "inv.json"
        out = Path(td) / "graph.json"
        src.write_text(json.dumps(inv), encoding="utf-8")
        proc = run(
            [
                "--inventory",
                str(src),
                "-o",
                str(out),
                "--generated-at",
                "2026-08-16T16:40:00Z",
            ]
        )
        try:
            expect(proc.returncode == 0, proc.stderr)
            doc = json.loads(out.read_text(encoding="utf-8"))
            expect(doc["generated_at"] == "2026-08-16T16:40:00Z", doc)
            expect(doc["source"] == "bazaar", doc)
            expect("ready" not in doc, doc)
            ids = {n["id"] for n in doc["nodes"]}
            expect(ids == {"a", "b", "epic"}, ids)
            by_id = {n["id"]: n for n in doc["nodes"]}
            expect(by_id["b"]["state"] == "landed", by_id["b"])
            expect(by_id["a"]["state"] == "open", by_id["a"])
            expect(by_id["a"]["needs"] == ["b"], by_id["a"])
            expect(by_id["epic"]["kind"] == "intention", by_id["epic"])
            expect("ready" not in by_id["a"], by_id["a"])
            print("pass project fixture")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL project: {exc}\n{proc.stdout}\n{proc.stderr}")
    if failed:
        return 1
    print("pass export-graph")
    return 0


if __name__ == "__main__":
    sys.exit(main())
