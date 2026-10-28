#!/usr/bin/env python3
"""Refusal card: outside, review, and separate waits for one node.

Reads a beads export (JSONL fixture via --export, else `bd export`) and prints
the card from openspec/changes/add-relay-refusal-card/design.md. Renders only:
it never flips a banner, closes a bead, or decides that a verb must refuse.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

CLOSED = {"closed", "done", "resolved"}


def load_export(path: Path | None) -> list[dict] | None:
    """Issue records, or None when the export cannot be read."""
    try:
        if path is not None:
            text = path.read_text(encoding="utf-8")
        else:
            proc = subprocess.run(
                ["bd", "export"], check=False, capture_output=True, text=True
            )
            if proc.returncode != 0:
                return None
            text = proc.stdout
        rows = [json.loads(ln) for ln in text.splitlines() if ln.strip()]
    except (OSError, json.JSONDecodeError):
        return None
    return [r for r in rows if isinstance(r, dict)]


def fields(desc: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in (desc or "").splitlines():
        key, sep, val = line.partition(":")
        key = key.strip().lower()
        if sep and key in {"project", "external", "blocks", "upstream"}:
            out.setdefault(key, val.strip())
    return out


def labels(rec: dict) -> set[str]:
    return {str(x) for x in rec.get("labels") or []}


def is_open(rec: dict) -> bool:
    return str(rec.get("status") or "open") not in CLOSED


def edges(node: dict, kind: str) -> list[str]:
    """Ids the node depends on by edge type (`blocks` or `related`)."""
    out = []
    for d in node.get("dependencies") or []:
        if not isinstance(d, dict):
            continue
        t = str(d.get("type") or d.get("dependency_type") or "blocks")
        target = str(d.get("depends_on_id") or "")
        if t == kind and target and not target.startswith("external:"):
            out.append(target)
    return out


def classify(nid: str, rows: list[dict]) -> dict[str, list[dict]] | None:
    by_id = {str(r.get("id")): r for r in rows}
    node = by_id.get(nid)
    if node is None:
        return None
    got: dict[str, list[dict]] = {"outside": [], "review": [], "internal": [], "deferred": []}
    for bid in edges(node, "blocks"):
        rec = by_id.get(bid)
        if rec is None or not is_open(rec):
            continue
        lab = labels(rec)
        if "outside" in lab:
            got["outside"].append(rec)
        elif "review" in lab or str(rec.get("issue_type")) == "gate":
            got["review"].append(rec)
        elif "internal" in lab:
            got["internal"].append(rec)
    for bid in edges(node, "related"):
        rec = by_id.get(bid)
        if rec is not None and is_open(rec) and "deferred" in labels(rec):
            got["deferred"].append(rec)
    return got


def review_reason(rec: dict) -> str:
    """Human gates store the sentence after `Reason:`, not in the title."""
    for line in str(rec.get("description") or "").splitlines():
        if line.lower().startswith("reason:"):
            text = line.split(":", 1)[1].strip()
            if text:
                return text
    title = str(rec.get("title") or "").strip()
    if title and title.lower() != "gate: human":
        return title
    return "no reason recorded"


def applies(rec: dict, nid: str, action: str) -> bool:
    blocks = [b.strip() for b in fields(rec.get("description", "")).get("blocks", "").split(",") if b.strip()]
    if not blocks:
        return action in {"activate", nid}
    return action in blocks


def surface(rec: dict, nid: str) -> list[str]:
    blocks = [b.strip() for b in fields(rec.get("description", "")).get("blocks", "").split(",") if b.strip()]
    return blocks or [nid]


def render(nid: str, action: str, rows: list[dict] | None) -> str:
    if rows is None:
        return f"Could not read beads for {nid}."
    got = classify(nid, rows)
    if got is None:
        return f"Could not read beads for {nid}."
    if not any(got.values()):
        return f"No outside wait recorded for {nid}."

    outside = [r for r in got["outside"] if applies(r, nid, action)]
    moved = [r for r in got["outside"] if r not in outside]
    unlocks: list[str] = []
    for r in outside:
        for s in surface(r, nid):
            if s not in unlocks:
                unlocks.append(s)
    lines = [
        f"Refused: {nid} stays as it is",
        f"Action: {action}",
        f"This refusal does not unlock {', '.join(unlocks) if unlocks else action}.",
    ]
    if outside:
        lines += ["", "Outside"]
        for r in outside:
            f = fields(r.get("description", ""))
            proj = f.get("project") or "project missing"
            ext = f.get("external") or "external missing"
            lines.append(f"- {proj} · {r.get('title') or r.get('id')}")
            lines.append(f"  {r.get('id')} · {ext}")
            if f.get("upstream"):
                lines.append(f"  upstream: {f['upstream']}")
    if got["review"]:
        lines += ["", "Review"]
        for r in got["review"]:
            lines.append(f"- {r.get('id')} · {review_reason(r)}")
    sep = [("internal", r) for r in got["internal"]]
    sep += [("outside", r) for r in moved]
    sep += [("deferred", r) for r in got["deferred"]]
    if sep:
        lines += ["", "Separate"]
        for kind, r in sep:
            lines.append(f"- {kind} · {r.get('id')} · {r.get('title') or ''}".rstrip(" ·"))
    return "\n".join(lines)


def waiting_lines(nid: str, rows: list[dict] | None) -> list[str]:
    """Outside and review lines for status Blocked and map. Empty if none or unreadable."""
    got = classify(nid, rows) if rows is not None else None
    if not got:
        return []
    out = []
    for r in got["outside"]:
        f = fields(r.get("description", ""))
        out.append(
            f"{f.get('project') or 'project missing'} · {r.get('id')} · "
            f"{f.get('external') or 'external missing'}"
        )
    for r in got["review"]:
        out.append(f"review · {r.get('id')} · {review_reason(r)}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node")
    ap.add_argument("--action", default="activate")
    ap.add_argument("--export", type=Path, help="beads export JSONL fixture instead of `bd export`")
    args = ap.parse_args(argv)
    print(render(args.node, args.action, load_export(args.export)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
