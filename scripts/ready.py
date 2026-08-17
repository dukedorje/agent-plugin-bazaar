#!/usr/bin/env python3
"""List ready/unblocked work and parked items.

Ready: in-flight ACTIVE BUILD with at least one open owed checkbox.
Needs activation: PENDING (draft, not available until a human activates).
Parked: in-flight PARKED banners plus openspec/parked.md (parks that are
not change directories).

Usage:
  python3 scripts/ready.py
  python3 scripts/ready.py --parked
  python3 scripts/ready.py --ready
  python3 scripts/ready.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_INTENTION_SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "intention" / "scripts"
if str(_INTENTION_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_INTENTION_SCRIPTS))
from advise_status import last_advise_verdict, needs_advise  # noqa: E402

# Keep in lockstep with check-hygiene.py (same banner and owed-work rules).
BANNER_RE = re.compile(r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b")
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")
SCOPE_HEADING_RE = re.compile(
    r"^#+\s+(out[ -]of[ -]scope|not in this change|deliberately not|handoffs?|findings|deferred)\b",
    re.I,
)
SCOPE_ITEM_RE = re.compile(
    r"(not in this change|out of scope|handoff|deliberately not)",
    re.I,
)
REVIVE_RE = re.compile(r"revive when\s+(.+)", re.I)
TABLE_ROW_RE = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$"
)


def first_banner(text: str) -> tuple[str | None, str]:
    for i, line in enumerate(text.splitlines()):
        if i >= 40:
            break
        m = BANNER_RE.match(line.strip())
        if m:
            revive = ""
            rm = REVIVE_RE.search(line)
            if rm:
                revive = rm.group(1).strip().rstrip(".")
            return m.group(1), revive
    return None, ""


def open_owed(tasks: str) -> list[str]:
    heading = ""
    open_items: list[str] = []
    for line in tasks.splitlines():
        if re.match(r"^#+\s+", line):
            heading = line
        m = CHECKBOX_RE.match(line)
        if not m:
            continue
        text = m.group(3).strip()
        if SCOPE_HEADING_RE.match(heading) or SCOPE_ITEM_RE.search(text):
            continue
        if m.group(2).lower() != "x":
            open_items.append(text)
    return open_items


def inflight(openspec: Path) -> list[dict]:
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    rows: list[dict] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        proposal = child / "proposal.md"
        if not proposal.is_file():
            continue
        banner, revive = first_banner(proposal.read_text(encoding="utf-8"))
        tasks_path = child / "tasks.md"
        open_items = open_owed(tasks_path.read_text(encoding="utf-8")) if tasks_path.is_file() else []
        rows.append(
            {
                "id": child.name,
                "kind": "change",
                "banner": banner or "none",
                "open": open_items,
                "revive": revive,
                "where": str(proposal.relative_to(openspec.parent)),
            }
        )
    return rows


def register(openspec: Path) -> list[dict]:
    path = openspec / "parked.md"
    if not path.is_file():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        m = TABLE_ROW_RE.match(line)
        if not m:
            continue
        cols = [c.strip() for c in m.groups()]
        if cols[0].lower() in {"id", "---"} or set(cols[0]) <= {"-"}:
            continue
        if cols[0].startswith("-"):
            continue
        rows.append(
            {
                "id": cols[0],
                "kind": cols[1],
                "banner": "PARKED",
                "open": [],
                "revive": cols[2],
                "where": cols[3],
            }
        )
    return rows


def classify(openspec: Path) -> dict[str, list[dict]]:
    ready, waiting, parked, needs = [], [], [], []
    changes = openspec / "changes"
    for row in inflight(openspec):
        change_dir = changes / row["id"]
        if needs_advise(change_dir):
            row["advise"] = last_advise_verdict(change_dir) or "missing"
            needs.append(row)
        if row["banner"] == "ACTIVE BUILD" and row["open"]:
            ready.append(row)
        elif row["banner"] == "PENDING":
            waiting.append(row)
        elif row["banner"] == "PARKED":
            parked.append(row)
    parked.extend(register(openspec))
    return {
        "ready": ready,
        "waiting": waiting,
        "parked": parked,
        "needs_advise": needs,
    }


def fmt(row: dict) -> str:
    extra = ""
    if row["open"]:
        extra = f"  open: {'; '.join(row['open'][:3])}"
    elif row["revive"]:
        extra = f"  revive: {row['revive']}"
    return f"{row['id']:28} {row['kind']:8} {row['where']}{extra}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--ready", action="store_true")
    p.add_argument("--parked", action="store_true")
    args = p.parse_args()
    repo = Path(__file__).resolve().parents[1]
    openspec = args.root.resolve() if args.root else (repo / "openspec")
    data = classify(openspec)
    if args.json:
        if args.parked and not args.ready:
            print(json.dumps({"parked": data["parked"]}, indent=2))
        elif args.ready and not args.parked:
            print(
                json.dumps(
                    {
                        "ready": data["ready"],
                        "waiting": data["waiting"],
                        "needs_advise": data["needs_advise"],
                    },
                    indent=2,
                )
            )
        else:
            print(json.dumps(data, indent=2))
        return 0

    show_ready = args.ready or not args.parked
    show_parked = args.parked or not args.ready
    if show_ready:
        print("READY (ACTIVE BUILD, unblocked)")
        if data["ready"]:
            for row in data["ready"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("NEEDS ACTIVATION (PENDING)")
        if data["waiting"]:
            for row in data["waiting"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("NEEDS ADVISE (ACTIVE BUILD, architecture/instrument)")
        if data["needs_advise"]:
            for row in data["needs_advise"]:
                print("  " + fmt(row) + f"  advise: {row.get('advise', 'missing')}")
        else:
            print("  (none)")
    if show_parked:
        print("PARKED")
        if data["parked"]:
            for row in data["parked"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
