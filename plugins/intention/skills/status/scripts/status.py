#!/usr/bin/env python3
"""List ready/unblocked work from OpenSpec and beads.

Travels with the ready skill. Finds openspec/ by walking up from cwd
(or --root). Beads come from `bd list --ready` (cwd). Does not assume
this file lives in the project.

  python3 <skill-dir>/scripts/ready.py
  python3 <skill-dir>/scripts/ready.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
from advise_status import last_advise_verdict, needs_advise  # noqa: E402

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
PUNT_BOX_RE = re.compile(r"\bPUNT\b", re.I)
EYES_BOX_RE = re.compile(r"\b(EYES|by-eye|human-verify|human verify)\b", re.I)
ASK_BOX_RE = re.compile(r"\bASK\b", re.I)
NEXT_CMD_RE = re.compile(r"Next:\s*(.+)$", re.I)


def box_kind(item: str) -> str | None:
    if PUNT_BOX_RE.search(item):
        return "punt"
    if EYES_BOX_RE.search(item):
        return "eyes"
    if ASK_BOX_RE.search(item):
        return "ask"
    return None


def with_open(row: dict, items: list[str]) -> dict:
    out = dict(row)
    out["open"] = items
    return out


def next_command(item: str) -> str | None:
    m = NEXT_CMD_RE.search((item or "").strip())
    if not m:
        return None
    cmd = m.group(1).strip().strip("`").strip()
    return cmd or None


def find_openspec(start: Path | None = None) -> Path | None:
    here = (start or Path.cwd()).resolve()
    for root in [here, *here.parents]:
        cand = root / "openspec"
        if cand.is_dir():
            return cand
        if (root / ".git").exists():
            return cand if cand.is_dir() else None
    return None


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
        try:
            where = str(proposal.relative_to(openspec.parent))
        except ValueError:
            where = str(proposal)
        rows.append(
            {
                "id": child.name,
                "kind": "change",
                "source": "openspec",
                "banner": banner or "none",
                "open": open_items,
                "revive": revive,
                "where": where,
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
                "source": "openspec",
                "banner": "PARKED",
                "open": [],
                "revive": cols[2],
                "where": cols[3],
            }
        )
    return rows


def classify(openspec: Path) -> dict[str, list[dict]]:
    ready, waiting, parked, needs = [], [], [], []
    ask, eyes, punt = [], [], []
    changes = openspec / "changes"
    for row in inflight(openspec):
        change_dir = changes / row["id"]
        if needs_advise(change_dir):
            row["advise"] = last_advise_verdict(change_dir) or "missing"
            needs.append(row)
        kinds: dict[str, list[str]] = {"ask": [], "eyes": [], "punt": [], "work": []}
        for item in row["open"]:
            kind = box_kind(item) or "work"
            kinds[kind].append(item)
        if row["banner"] == "ACTIVE BUILD":
            if kinds["work"]:
                ready.append(with_open(row, kinds["work"]))
            if kinds["ask"]:
                ask.append(with_open(row, kinds["ask"]))
            if kinds["eyes"]:
                eyes.append(with_open(row, kinds["eyes"]))
            if kinds["punt"]:
                punt.append(with_open(row, kinds["punt"]))
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
        "ask": ask,
        "eyes": eyes,
        "punt": punt,
    }


def fmt(row: dict) -> str:
    extra = ""
    if row["open"]:
        extra = f"  open: {'; '.join(row['open'][:3])}"
    elif row["revive"]:
        extra = f"  revive: {row['revive']}"
    return f"{row['id']:28} {row['kind']:8} {row['where']}{extra}"


def empty() -> dict[str, list[dict]]:
    return {
        "ready": [],
        "waiting": [],
        "parked": [],
        "needs_advise": [],
        "ask": [],
        "eyes": [],
        "punt": [],
        "beads": [],
    }


def load_beads() -> list[dict]:
    """Unblocked beads (`bd list --ready`). Empty if bd is missing."""
    try:
        proc = subprocess.run(
            ["bd", "list", "--ready", "--json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=str(Path.cwd()),
        )
    except OSError:
        return []
    if proc.returncode != 0:
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return []
    return normalize_beads(data)


def load_beads_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return normalize_beads(data)


def normalize_beads(raw: Any) -> list[dict]:
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for row in raw:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        item = dict(row)
        item["source"] = "beads"
        out.append(item)
    return out


def fmt_bead(row: dict) -> str:
    nid = str(row.get("id") or "")
    kind = str(row.get("issue_type") or row.get("type") or "bead")
    title = " ".join(str(row.get("title") or "").split())
    if len(title) > 72:
        title = title[:69] + "..."
    return f"{nid:28} {kind:8} {title}"


def print_card(
    data: dict[str, list[dict]],
    *,
    show_ready: bool,
    show_parked: bool,
    missing: str | None = None,
) -> None:
    if show_ready:
        print("READY (OpenSpec · ACTIVE BUILD, unblocked)")
        if data["ready"]:
            for row in data["ready"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("NEEDS ACTIVATION (OpenSpec · PENDING)")
        if data["waiting"]:
            for row in data["waiting"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("NEEDS ADVISE (OpenSpec · architecture/instrument)")
        if data["needs_advise"]:
            for row in data["needs_advise"]:
                print("  " + fmt(row) + f"  advise: {row.get('advise', 'missing')}")
        else:
            print("  (none)")
        print("ASK (decision owed)")
        if data.get("ask"):
            for row in data["ask"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("EYES — YOUR EYES (look owed, not READY)")
        if data.get("eyes"):
            for row in data["eyes"]:
                print("  " + fmt(row))
                cmds: list[str] = []
                for item in row.get("open") or []:
                    cmd = next_command(str(item))
                    if cmd and cmd not in cmds:
                        cmds.append(cmd)
                print("  Next:")
                if cmds:
                    for cmd in cmds:
                        print(f"    {cmd}")
                else:
                    print("    /status")
        else:
            print("  (none)")
        print("PUNT (second-family advise, last-resort)")
        if data.get("punt"):
            for row in data["punt"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
        print("BEADS (bd ready · unblocked)")
        if data.get("beads"):
            for row in data["beads"]:
                print("  " + fmt_bead(row))
        else:
            print("  (none)")
    if show_parked:
        print("PARKED (OpenSpec)")
        if data["parked"]:
            for row in data["parked"]:
                print("  " + fmt(row))
        else:
            print("  (none)")
    if missing == "openspec":
        if data.get("beads"):
            print("no openspec/ from cwd — OpenSpec lens empty; beads still shown")
        else:
            print("no openspec/ from cwd — not a guessed ready-set")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--ready", action="store_true")
    p.add_argument("--parked", action="store_true")
    p.add_argument(
        "--beads-json",
        type=Path,
        help="fixture beads instead of `bd list --ready`",
    )
    args = p.parse_args()
    if args.beads_json is not None:
        beads = load_beads_json(args.beads_json)
    else:
        beads = load_beads()
    if args.root:
        openspec = args.root.resolve()
    else:
        found = find_openspec()
        openspec = found if found else Path.cwd() / "openspec"
    missing = None
    if not openspec.is_dir():
        data = empty()
        missing = "openspec"
    else:
        data = classify(openspec)
    data["beads"] = beads
    show_ready = args.ready or not args.parked
    show_parked = args.parked or not args.ready
    if args.json:
        payload: dict[str, Any]
        if args.parked and not args.ready:
            payload = {"parked": data["parked"]}
        elif args.ready and not args.parked:
            payload = {
                "ready": data["ready"],
                "waiting": data["waiting"],
                "needs_advise": data["needs_advise"],
                "ask": data.get("ask") or [],
                "eyes": data.get("eyes") or [],
                "punt": data.get("punt") or [],
                "beads": data["beads"],
            }
        else:
            payload = dict(data)
        if missing:
            payload["missing"] = missing
        print(json.dumps(payload, indent=2))
        return 0
    print_card(data, show_ready=show_ready, show_parked=show_parked, missing=missing)
    return 0


if __name__ == "__main__":
    sys.exit(main())
