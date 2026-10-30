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
PINNED = re.compile(r"pinned campaign is still ([A-Za-z0-9.-]+)")
ACCEPTED_BY = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*) accepted by (\S+)")
SENT_BACK = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*) sent back by (\S+)")
NEXT_CHANGE = re.compile(r"Next is change: ([^\n]+)")
R_ACCEPT = re.compile(r"(r\d+ accepted that spec)")
FOLD_IS = re.compile(r"The fold is ([0-9a-f]{7,}): \S*specs/([a-z0-9-]+)/")
REFUSED = re.compile(
    r"(?m)^[^\n]*?([a-z0-9]+(?:-[a-z0-9]+)*) (?:still has \d+ open|says |is landed except)"
)
HUMAN_GATE = re.compile(
    r"([a-z0-9]+(?:-[a-z0-9]+)*) \(([A-Za-z0-9.-]+)\) is still a human gate[^\n]*not activated"
)
ACT_NOT = re.compile(r"([a-z0-9]+(?:-[a-z0-9]+)*) is accepted and still owes[^\n]*")


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
    pinned = PINNED.search(text)
    if pinned and not campaign:
        campaign = pinned.group(1)
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
    for match in ACCEPTED_BY.finditer(text):
        events.append((match.start(), "accepted", {"change": match.group(1), "evidence": match.group(0).rstrip(".")}))
    for match in SENT_BACK.finditer(text):
        events.append((match.start(), "sendback", {"change": match.group(1), "evidence": match.group(0).rstrip(".")}))
    for match in NEXT_CHANGE.finditer(text):
        events.append((match.start(), "nextchange", {"evidence": match.group(0).strip()}))
    for match in R_ACCEPT.finditer(text):
        events.append((match.start(), "raccept", {"evidence": match.group(1)}))
    for match in FOLD_IS.finditer(text):
        events.append((match.start(), "foldis", {"change": match.group(2), "evidence": f"The fold is {match.group(1)}"}))
    for match in REFUSED.finditer(text):
        events.append((match.start(), "refused", {"change": match.group(1), "evidence": match.group(0).strip()}))
    for match in HUMAN_GATE.finditer(text):
        events.append((match.start(), "gate", {"change": match.group(1), "node": match.group(2), "evidence": match.group(0).strip()}))
    for match in ACT_NOT.finditer(text):
        events.append((match.start(), "actnot", {"change": match.group(1), "evidence": match.group(0).strip()}))
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
    last_change = ""
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
        if data.get("change"):
            last_change = data["change"]
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
        elif kind == "accepted":
            add("advising", "advise", "accepted", data["change"], data["evidence"])
            state = "accepted"
        elif kind == "sendback":
            add("advising", "advise", "send_back", data["change"], data["evidence"])
            state = "send_back"
        elif kind == "nextchange":
            add("send_back", "change", "scaffolded", last_change, data["evidence"])
            state = "scaffolded"
        elif kind == "raccept":
            add("advising", "advise", "accepted", last_change, data["evidence"])
            state = "accepted"
        elif kind == "foldis":
            add("accepted", "fold", "folded", data["change"], data["evidence"])
            state = "folded"
        elif kind == "refused":
            add(state, "fold", state, data["change"], data["evidence"], taken=False)
        elif kind == "gate":
            last_change = data.get("change") or last_change
            add(state, "activate", "ask", data["change"], data["evidence"], taken=False)
            if data["node"] not in open_nodes:
                open_nodes.append(data["node"])
        elif kind == "actnot":
            add("accepted", "act", "accepted", data["change"], data["evidence"], taken=False)
    for row in rows:
        if not row["open"]:
            row["open"] = list(open_nodes)
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
