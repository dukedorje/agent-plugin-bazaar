#!/usr/bin/env python3
"""Project a signed result (or a raw dump) to the conductor-facing face.

The conductor reads this. The full report stays at raw_ref.

  python3 plugins/intention/scripts/distill-result.py <result.json>
  python3 plugins/intention/scripts/distill-result.py --raw <file> --out face.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _as_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(x) for x in value if isinstance(x, str) and x]


def from_result(data: dict, raw_ref: str) -> dict:
    evidence = data.get("evidence") if isinstance(data.get("evidence"), dict) else {}
    commit = data.get("commit") if isinstance(data.get("commit"), dict) else None
    artifacts = data.get("artifacts") if isinstance(data.get("artifacts"), list) else []
    existing = data.get("distilled") if isinstance(data.get("distilled"), dict) else {}

    changed = existing.get("changed_files")
    if not isinstance(changed, list):
        changed = []
        if commit and isinstance(commit.get("paths"), list):
            changed = [p for p in commit["paths"] if isinstance(p, str)]
        elif artifacts:
            changed = [
                a["path"]
                for a in artifacts
                if isinstance(a, dict) and isinstance(a.get("path"), str)
            ]

    verify_command = existing.get("verify_command")
    if verify_command is None:
        cmd = evidence.get("command")
        verify_command = cmd if isinstance(cmd, str) and cmd else None

    verify_exit = existing.get("verify_exit")
    if verify_exit is None:
        exit_code = evidence.get("exit_code")
        verify_exit = exit_code if isinstance(exit_code, int) else None

    commit_sha = existing.get("commit_sha")
    if commit_sha is None and commit:
        sha = commit.get("sha")
        commit_sha = sha if isinstance(sha, str) else None

    disposition = data.get("disposition")
    if not isinstance(disposition, str):
        disposition = "blocked"

    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        summary = "(no summary)"

    blockers = existing.get("blockers")
    if not isinstance(blockers, list):
        blockers = []
    if disposition in {"blocked", "task-red", "infra-red", "parked"} and not blockers:
        note = evidence.get("note")
        if isinstance(note, str) and note:
            blockers = [note]

    return {
        "disposition": disposition,
        "summary": summary,
        "verify_command": verify_command,
        "verify_exit": verify_exit,
        "commit_sha": commit_sha,
        "changed_files": _as_str_list(changed),
        "blockers": _as_str_list(blockers),
        "raw_ref": existing.get("raw_ref") if isinstance(existing.get("raw_ref"), str) else raw_ref,
    }


def from_raw_text(text: str, raw_ref: str) -> dict:
    text = text.strip()
    if text.startswith("{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict) and "disposition" in data:
            return from_result(data, raw_ref)
    return {
        "disposition": "blocked",
        "summary": "Unparsed worker transcript. Open raw_ref.",
        "verify_command": None,
        "verify_exit": None,
        "commit_sha": None,
        "changed_files": [],
        "blockers": ["unparsed-raw"],
        "raw_ref": raw_ref,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("result", type=Path, nargs="?")
    p.add_argument("--raw", type=Path, help="Transcript or JSON dump")
    p.add_argument("--out", type=Path, help="Write distilled JSON here")
    p.add_argument(
        "--embed",
        action="store_true",
        help="Write distilled back onto the result file (result mode only)",
    )
    args = p.parse_args()

    src = args.raw or args.result
    if src is None:
        p.error("result.json or --raw FILE is required")

    raw_ref = str(src)
    if args.raw:
        face = from_raw_text(src.read_text(encoding="utf-8"), raw_ref)
    else:
        data = json.loads(src.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            print("result is not a JSON object", file=sys.stderr)
            return 1
        face = from_result(data, raw_ref)
        if args.embed:
            data["distilled"] = face
            data["raw_ref"] = face["raw_ref"]
            src.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    blob = json.dumps(face, indent=2) + "\n"
    if args.out:
        args.out.write_text(blob, encoding="utf-8")
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
