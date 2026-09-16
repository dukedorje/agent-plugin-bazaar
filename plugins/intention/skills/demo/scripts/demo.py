#!/usr/bin/env python3
"""Observe-only demo: present the journey for a landed act, then halt.

  python3 <skill-dir>/scripts/demo.py
  python3 <skill-dir>/scripts/demo.py add-run-wave-workflow
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SESSION_ENV = (
    "INTENTION_SESSION",
    "GROK_SESSION_ID",
    "CLAUDE_SESSION_ID",
    "CODEX_SESSION_ID",
)
SESSION_KEY_RE = re.compile(r"^[A-Za-z0-9._-]+$")
CHANGE_ID_RE = re.compile(
    r"^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
JOURNEY_RE = re.compile(r"^##\s+User journey", re.I)
HEADING_RE = re.compile(r"^##\s+")
NEXT_CMD_RE = re.compile(r"Next:\s*(.+)$", re.I)
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")


def find_openspec() -> Path | None:
    here = Path.cwd()
    for root in [here, *here.parents]:
        cand = root / "openspec"
        if cand.is_dir():
            return cand
        if (root / ".git").exists():
            return cand if cand.is_dir() else None
    return None


def find_change_dir(openspec: Path | None, change_id: str) -> Path | None:
    if openspec is None or not change_id:
        return None
    live = openspec / "changes" / change_id
    if live.is_dir() and (live / "proposal.md").is_file():
        return live
    archive = openspec / "changes" / "archive"
    if archive.is_dir():
        hits = [
            child
            for child in archive.iterdir()
            if child.is_dir()
            and child.name.endswith("-" + change_id)
            and (child / "proposal.md").is_file()
        ]
        if hits:
            return sorted(hits, key=lambda p: p.name)[-1]
    return None


def journey_section(proposal: str) -> str:
    lines = proposal.splitlines()
    start = None
    for i, line in enumerate(lines):
        if JOURNEY_RE.match(line.strip()):
            start = i + 1
            break
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start:]:
        if HEADING_RE.match(line.strip()):
            break
        body.append(line)
    return "\n".join(body).strip()


def next_commands(tasks: str) -> list[str]:
    out: list[str] = []
    for line in tasks.splitlines():
        m = CHECKBOX_RE.match(line)
        text = m.group(3) if m else line
        nxt = NEXT_CMD_RE.search(text)
        if nxt:
            cmd = nxt.group(1).strip().strip("`").strip()
            if cmd and cmd not in out:
                out.append(cmd)
    return out


def session_key() -> str | None:
    for var in SESSION_ENV:
        val = (os.environ.get(var) or "").strip()
        if val and SESSION_KEY_RE.match(val):
            return val
    return None


def read_current() -> str | None:
    key = session_key()
    if not key:
        return None
    path = Path.home() / ".intention" / "sessions" / key / "current.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    roots = data.get("roots")
    if isinstance(roots, list) and roots and isinstance(roots[0], str) and roots[0]:
        return roots[0]
    return None


def landing_from(scope: str | None) -> str | None:
    if not scope:
        return None
    head = scope.strip().split()[0].rstrip(":")
    return head if CHANGE_ID_RE.match(head) else None


def empty_card() -> str:
    return (
        "┌─ DEMO ─────────────────────────────────────────\n"
        "│ YOUR DEMO · empty\n"
        "│ nothing landed to try\n"
        "└───────────────────────────────────────────────\n"
        "\n"
        "Print `/status` and stop. No box. No fold. No `demo.md`.\n"
    )


def working_card(
    change_id: str,
    where: str,
    journey: str,
    commands: list[str],
) -> str:
    try_line = commands[0] if commands else "(see journey)"
    lines = [
        "┌─ DEMO ─────────────────────────────────────────",
        "│ YOUR DEMO · halt",
        f"│ {change_id} · {where}",
        f"│ try: {try_line}",
        "└───────────────────────────────────────────────",
        "",
        "## Journey",
        "",
        journey or "(no User journey section)",
        "",
    ]
    if commands:
        lines.extend(["## Next", ""])
        for cmd in commands:
            lines.append(f"- `{cmd}`")
        lines.append("")
    lines.append("Halt. Do not fold. Do not act. Do not check a box.")
    lines.append("")
    return "\n".join(lines)


def load_fixture(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("fixture must be a JSON object")
    return data


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scope", nargs="?", help="change-id to try")
    p.add_argument("--fixture", type=Path)
    args = p.parse_args()

    if args.fixture:
        fix = load_fixture(args.fixture)
        cid = str(fix.get("change_id") or landing_from(args.scope) or "")
        proposal = str(fix.get("proposal") or "")
        tasks = str(fix.get("tasks") or "")
        if not cid or not proposal:
            print(empty_card(), end="")
            return 0
        where = "archive" if fix.get("archived") else "inflight"
        journey = journey_section(proposal)
        commands = next_commands(tasks)
        if not journey and not commands:
            print(empty_card(), end="")
            return 0
        print(working_card(cid, where, journey, commands), end="")
        return 0

    openspec = find_openspec()
    scope = args.scope or read_current()
    cid = landing_from(scope) if scope else None
    dest = find_change_dir(openspec, cid) if cid else None
    if dest is None:
        print(empty_card(), end="")
        return 0
    proposal = (dest / "proposal.md").read_text(encoding="utf-8")
    tasks_path = dest / "tasks.md"
    tasks = tasks_path.read_text(encoding="utf-8") if tasks_path.is_file() else ""
    journey = journey_section(proposal)
    commands = next_commands(tasks)
    if not journey and not commands:
        print(empty_card(), end="")
        return 0
    where = "archive" if "archive" in dest.parts else "inflight"
    print(working_card(cid or dest.name, where, journey, commands), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
