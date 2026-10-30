#!/usr/bin/env python3
"""Append settled-run transitions and parse them into edge counts.

The log is references/transition-log.jsonl. One JSON object per line.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "references" / "transition-log.jsonl"
VERBS = json.loads((ROOT / "references" / "transitions.json").read_text(encoding="utf-8"))[
    "commands"
].keys()

SPIKE = re.compile(r"Spike (\S+) — go \(([0-9a-f]{7,})\)")
CLOSED = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*) — closed \(([0-9a-f]{7,})\)")
NO_FOLD = re.compile(r"Do not fold ([a-z0-9]+(?:-[a-z0-9]+)*)")
STILL_OPEN = re.compile(r"Still open on ([A-Za-z0-9-]+): (.+)")
OPEN_ITEM = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*) \(([A-Za-z0-9-]+)\)")
DEMO = re.compile(r"(?m)^[ \t]*Demo[ \t]*$")
ACTIVATE = re.compile(r"activate and run")


def load_rows() -> list[dict]:
    if not LOG.exists():
        return []
    rows = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if row.get("v") != 1 or row.get("verb") not in VERBS:
            raise SystemExit(f"bad transition row: {line[:120]}")
        if "from" not in row or "to" not in row or "evidence" not in row:
            raise SystemExit(f"transition row is missing a field: {line[:120]}")
        rows.append(row)
    return rows


def append_rows(rows: list[dict]) -> int:
    have = {row["evidence"] for row in load_rows()}
    fresh = [row for row in rows if row["evidence"] not in have]
    if not fresh:
        return 0
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        for row in fresh:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(fresh)


def unwrap(text: str) -> str:
    """Join pane wraps so a change id split across lines is one token."""
    lines = [re.sub(r"[ \t]+", " ", line.replace("█", "")).strip() for line in text.splitlines()]
    joined: list[str] = []
    for line in lines:
        if not line:
            joined.append("")
            continue
        if joined and joined[-1].endswith("-") and line[:1].islower():
            joined[-1] = joined[-1] + line
        else:
            joined.append(line)
    return "\n".join(joined)


def observe(text: str) -> list[dict]:
    """Walk a settled transcript left to right and emit one row per verb."""
    text = unwrap(text)
    campaign = ""
    open_nodes: list[str] = []
    still = STILL_OPEN.search(text)
    if still:
        campaign = still.group(1)
        open_nodes = [item.group(2) for item in OPEN_ITEM.finditer(still.group(2))]
    events: list[tuple[int, str, dict]] = []
    started = ACTIVATE.search(text)
    if started:
        events.append((started.start(), "activate", {}))
    for match in SPIKE.finditer(text):
        events.append((match.start(), "spike", {"change": match.group(1), "evidence": match.group(0)}))
    for match in CLOSED.finditer(text):
        events.append((match.start(), "closed", {"change": match.group(1), "evidence": match.group(0)}))
    for match in NO_FOLD.finditer(text):
        events.append((match.start(), "nofold", {"change": match.group(1), "evidence": match.group(0)}))
    demo = DEMO.search(text)
    if demo:
        events.append((demo.start(), "demo", {"evidence": "Demo"}))
    events.sort(key=lambda item: item[0])
    seen: set[tuple[str, str]] = set()
    unique: list[tuple[int, str, dict]] = []
    for event in events:
        key = (event[1], event[2].get("evidence", event[1]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(event)
    events = unique

    state = "campaign"
    rows: list[dict] = []

    def add(frm: str, verb: str, to: str, change: str, evidence: str, taken: bool = True) -> None:
        rows.append(
            {
                "v": 1,
                "campaign": campaign,
                "change": change,
                "from": frm,
                "verb": verb,
                "to": to,
                "open": open_nodes,
                "taken": taken,
                "evidence": evidence,
            }
        )

    for _pos, kind, data in events:
        if kind == "activate":
            add(state, "activate_and_run", "campaign", "", "activate and run")
            state = "campaign"
        elif kind == "spike":
            add("spike", "spike", "ready", data["change"], data["evidence"])
            state = "ready"
        elif kind == "closed":
            # A second landing, with nodes still open, is change then act.
            if state == "landed":
                add("landed", "change", "scaffolded", data["change"], f"next node {data['evidence']}")
                state = "scaffolded"
            add(state, "act", "landed", data["change"], data["evidence"])
            state = "landed"
        elif kind == "demo":
            add(state, "demo", state, "", data["evidence"])
        elif kind == "nofold":
            add(state, "fold", state, data["change"], data["evidence"], taken=False)
    return rows


def parse(rows: list[dict]) -> dict:
    edges: dict[tuple[str, str, str, bool], int] = {}
    for row in rows:
        key = (row["from"], row["verb"], row["to"], bool(row.get("taken", True)))
        edges[key] = edges.get(key, 0) + 1
    return {
        "edges": [
            {"from": frm, "verb": verb, "to": to, "taken": taken, "count": count}
            for (frm, verb, to, taken), count in sorted(edges.items())
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observe", action="store_true", help="read a transcript on stdin and append")
    parser.add_argument("--parse", action="store_true", help="print edge counts")
    args = parser.parse_args()
    if args.observe:
        added = append_rows(observe(sys.stdin.read()))
        print(f"appended {added}")
    if args.parse or not args.observe:
        json.dump(parse(load_rows()), sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
