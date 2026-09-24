#!/usr/bin/env python3
"""List ready/unblocked work from OpenSpec and beads.

Travels with the ready skill. Finds openspec/ by walking up from cwd
(or --root). Beads come from `bd list --ready` (cwd). Does not assume
this file lives in the project.

  python3 <skill-dir>/scripts/status.py
  python3 <skill-dir>/scripts/status.py --json
  python3 <skill-dir>/scripts/status.py --queue
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


def first_heading(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return ""


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
        body = proposal.read_text(encoding="utf-8")
        banner, revive = first_banner(body)
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
                "title": first_heading(body) or child.name,
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
    """Legacy one-liner; printers use print_change / print_bead_line."""
    extra = ""
    if row.get("open"):
        extra = f"  open: {'; '.join(row['open'][:3])}"
    elif row.get("revive"):
        extra = f"  revive: {row['revive']}"
    return f"{row['id']:28} {row.get('kind', ''):8} {row.get('where', '')}{extra}"


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
    title = short_what(row.get("title") or "", 72)
    return f"{nid:28} {kind:8} {title}"


def short_what(text: object, limit: int = 72) -> str:
    title = " ".join(str(text or "").split())
    if len(title) > limit:
        return title[: limit - 3] + "..."
    return title


def pri_label(row: dict) -> str:
    p = row.get("priority")
    if p is None or p == "":
        return "—"
    try:
        return f"P{int(p)}"
    except (TypeError, ValueError):
        return str(p)


def load_blocked() -> list[dict]:
    """Open beads with unsatisfied blockers. Empty if bd is missing."""
    try:
        proc = subprocess.run(
            ["bd", "blocked", "--json"],
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


def load_blocked_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return normalize_beads(data)


def blocked_ids(rows: list[dict]) -> set[str]:
    out: set[str] = set()
    for row in rows:
        nid = str(row.get("id") or "")
        if nid:
            out.add(nid)
    return out


def parent_ids(rows: list[dict]) -> set[str]:
    out: set[str] = set()
    for row in rows:
        parent = row.get("parent")
        if parent:
            out.add(str(parent))
    return out


def is_umbrella_epic(row: dict, parents: set[str]) -> bool:
    kind = str(row.get("issue_type") or row.get("type") or "").lower()
    nid = str(row.get("id") or "")
    return kind == "epic" and nid in parents


def queue_row(row: dict, *, source: str) -> dict:
    title = row.get("title")
    if not title or title == row.get("id"):
        opens = row.get("open") or []
        if opens:
            title = strip_next(str(opens[0]))
    if not title:
        title = row.get("id")
    blocked_by = row.get("blocked_by") or []
    if not isinstance(blocked_by, list):
        blocked_by = [blocked_by]
    return {
        "id": str(row.get("id") or ""),
        "priority": row.get("priority"),
        "issue_type": str(row.get("issue_type") or row.get("type") or row.get("kind") or "bead"),
        "title": short_what(title, 72),
        "source": source,
        "blocked_by": [str(x) for x in blocked_by if x],
    }


def build_queue(
    data: dict[str, list[dict]],
    *,
    blocked: list[dict],
) -> dict[str, list[dict]]:
    """Honest startable pile: unblocked leaves + OpenSpec READY implement.

    Umbrella epics (have children in this payload) stay off the queue —
    the child is the work. Blocked beads are a separate list, never mixed
    in. Empty ASK/EYES/PUNT faces are omitted by the printer.
    """
    beads = list(data.get("beads") or [])
    blocked_set = blocked_ids(blocked)
    # bd list --ready has included blocked ids; subtract rather than trust it.
    parents = parent_ids(beads) | parent_ids(blocked)
    queue: list[dict] = []
    for row in data.get("ready") or []:
        queue.append(queue_row(row, source="openspec"))
    for row in beads:
        nid = str(row.get("id") or "")
        if nid in blocked_set:
            continue
        if is_umbrella_epic(row, parents):
            continue
        queue.append(queue_row(row, source="beads"))
    waiting = [queue_row(row, source="openspec") for row in data.get("waiting") or []]

    def sort_key(row: dict) -> tuple:
        try:
            pri = int(row["priority"])
        except (TypeError, ValueError):
            pri = 99
        return (pri, row["id"])

    queue.sort(key=sort_key)
    blocked_rows = [queue_row(row, source="beads") for row in blocked]
    blocked_rows.sort(key=sort_key)
    waiting.sort(key=sort_key)
    return {"queue": queue, "blocked": blocked_rows, "waiting": waiting}


def code_id(nid: object) -> str:
    return f"`{nid}`"


def pri_sort(row: dict) -> tuple:
    try:
        pri = int(row.get("priority"))
    except (TypeError, ValueError):
        pri = 99
    return (pri, str(row.get("id") or ""))


def family_of(nid: str) -> str | None:
    if "." in nid:
        return nid.split(".", 1)[0]
    return None


def print_bullets(items: list[str], *, limit: int = 6, indent: str = "  ") -> None:
    shown = items[:limit]
    for item in shown:
        print(f"{indent}- {item}")
    extra = len(items) - len(shown)
    if extra > 0:
        print(f"{indent}- +{extra} more")


def strip_next(item: str) -> str:
    return NEXT_CMD_RE.sub("", item or "").rstrip(" .—-").strip()


def display_title(row: dict, *, from_open: bool = True) -> str:
    nid = str(row.get("id") or "")
    title = short_what(row.get("title") or "", 88)
    if title and title != nid:
        return title
    if from_open:
        opens = row.get("open") or []
        if opens:
            return short_what(strip_next(str(opens[0])), 88)
    return ""


def print_change(row: dict, *, note: str | None = None, from_open: bool = True) -> None:
    nid = str(row.get("id") or "")
    title = display_title(row, from_open=from_open)
    kind = str(row.get("kind") or "")
    head = f"- **{code_id(nid)}**"
    if kind and kind not in {"change", "bead"}:
        head += f" · {kind}"
    if title:
        head += f"  {title}"
    print(head)
    if note:
        print(f"  {note}")
    opens = [str(x) for x in (row.get("open") or []) if x]
    title_is_first_open = bool(
        from_open and opens and title == short_what(strip_next(str(opens[0])), 88)
    )
    rest = opens[1:] if title_is_first_open else opens
    if rest:
        print_bullets(rest)
    elif row.get("revive") and not opens:
        print(f"  Revive when {row['revive']}")


def print_bead_line(row: dict, *, waiting: str | None = None) -> None:
    nid = str(row.get("id") or "")
    kind = str(row.get("issue_type") or row.get("type") or row.get("kind") or "bead")
    title = short_what(row.get("title") or "", 80)
    pri = pri_label(row)
    bits = [f"- {code_id(nid)}"]
    if pri != "—":
        bits.append(pri)
    if kind and kind not in {"bead", "change"}:
        bits.append(kind)
    if title:
        bits.append(title)
    print(" · ".join(bits))
    if waiting:
        print(f"  waiting on {waiting}")


def grouped_rows(rows: list[dict]) -> list[tuple[str | None, dict | None, list[dict]]]:
    """Group dotted children under a family id. Ungrouped rows have family None."""
    by_id = {str(r.get("id") or ""): r for r in rows if r.get("id")}
    children: dict[str, list[dict]] = {}
    ungrouped: list[dict] = []
    for row in rows:
        nid = str(row.get("id") or "")
        parent = str(row.get("parent") or "") or family_of(nid)
        if parent and parent != nid:
            children.setdefault(parent, []).append(row)
        else:
            ungrouped.append(row)
    used_children: set[str] = set()
    groups: list[tuple[str | None, dict | None, list[dict]]] = []
    families = sorted(children, key=lambda fid: pri_sort(by_id.get(fid) or {"id": fid}))
    for fid in families:
        kids = sorted(children[fid], key=pri_sort)
        used_children.update(str(k.get("id") or "") for k in kids)
        head = by_id.get(fid)
        groups.append((fid, head, kids))
    rest = [r for r in ungrouped if str(r.get("id") or "") not in used_children]
    rest = [r for r in rest if str(r.get("id") or "") not in children]
    rest.sort(key=pri_sort)
    if rest:
        groups.append((None, None, rest))
    return groups


def print_grouped(rows: list[dict], *, line) -> None:
    groups = grouped_rows(rows)
    for i, (fid, head, members) in enumerate(groups):
        if i:
            print()
        if fid is not None:
            if head is not None:
                title = short_what(head.get("title") or "", 80)
                pri = pri_label(head)
                label = f"**{code_id(fid)}**"
                if pri != "—":
                    label += f" · {pri}"
                if title:
                    label += f"  {title}"
                print(label)
            else:
                print(f"**{code_id(fid)}**")
            for row in members:
                line(row)
        else:
            if i > 0:
                print("**Also**")
            for row in members:
                line(row)


def tally(data: dict[str, list[dict]], *, show_ready: bool, show_parked: bool) -> str:
    pairs: list[tuple[str, int]] = []
    if show_ready:
        pairs.extend(
            [
                ("Ready", len(data.get("ready") or [])),
                ("Pending", len(data.get("waiting") or [])),
                ("Advise", len(data.get("needs_advise") or [])),
                ("Ask", len(data.get("ask") or [])),
                ("Eyes", len(data.get("eyes") or [])),
                ("Punt", len(data.get("punt") or [])),
                ("Beads", len(data.get("beads") or [])),
            ]
        )
    if show_parked:
        pairs.append(("Parked", len(data.get("parked") or [])))
    bits = [f"{label} {n}" for label, n in pairs if n]
    return " · ".join(bits) if bits else "Empty"


def print_section(title: str, blurb: str | None, rows: list, printer) -> None:
    if not rows:
        return
    print(f"## {title} · {len(rows)}")
    if blurb:
        print(blurb)
    print()
    printer(rows)
    print()


def print_queue(face: dict[str, list[dict]]) -> None:
    print("# Queue")
    print()
    print("Open, unblocked.")
    print()
    if face["queue"]:
        print_grouped(face["queue"], line=print_bead_line)
    else:
        print("(none)")
    if face["blocked"]:
        print()
        print(f"## Blocked · {len(face['blocked'])}")
        print()

        def blocked_line(row: dict) -> None:
            waiting = ", ".join(code_id(x) for x in row.get("blocked_by") or []) or "—"
            print_bead_line(row, waiting=waiting)

        print_grouped(face["blocked"], line=blocked_line)
    if face["waiting"]:
        print()
        print(f"## Needs activation · {len(face['waiting'])}")
        print("OpenSpec · PENDING")
        print()
        for row in face["waiting"]:
            print_bead_line(row)


def print_card(
    data: dict[str, list[dict]],
    *,
    show_ready: bool,
    show_parked: bool,
    missing: str | None = None,
) -> None:
    print("# Status")
    print()
    print(tally(data, show_ready=show_ready, show_parked=show_parked))
    print()

    if show_ready:
        eyes = data.get("eyes") or []
        if eyes:
            print(f"## YOUR EYES · {len(eyes)}")
            print("Look owed — not READY. Check the box after you look.")
            print()
            for row in eyes:
                heading = dict(row)
                heading["open"] = []
                print_change(heading, from_open=False)
                cmds: list[str] = []
                looks: list[str] = []
                for item in row.get("open") or []:
                    text = str(item)
                    cmd = next_command(text)
                    if cmd and cmd not in cmds:
                        cmds.append(cmd)
                    look = strip_next(text)
                    if look:
                        looks.append(look)
                if looks:
                    print_bullets(looks)
                if not cmds:
                    cmds = ["/status"]
                print("  Next: " + ", ".join(f"`{c}`" for c in cmds))
            print()

        print_section(
            "Ready",
            "OpenSpec · ACTIVE BUILD, unblocked implement work.",
            data.get("ready") or [],
            lambda rows: [print_change(r) for r in rows],
        )
        print_section(
            "Needs activation",
            "OpenSpec · PENDING.",
            data.get("waiting") or [],
            lambda rows: [print_change(r) for r in rows],
        )
        print_section(
            "Needs advise",
            "OpenSpec · architecture / instrument.",
            data.get("needs_advise") or [],
            lambda rows: [
                print_change(r, note=f"advise: {r.get('advise', 'missing')}") for r in rows
            ],
        )
        print_section(
            "Ask",
            "Decision owed. Next is `steer`.",
            data.get("ask") or [],
            lambda rows: [print_change(r) for r in rows],
        )
        print_section(
            "Punt",
            "Second-family advise, last-resort.",
            data.get("punt") or [],
            lambda rows: [print_change(r) for r in rows],
        )
        beads = data.get("beads") or []
        if beads:
            print(f"## Beads · {len(beads)}")
            print("Unblocked (`bd ready`).")
            print()
            print_grouped(beads, line=print_bead_line)
            print()
        elif show_ready and not any(
            data.get(k)
            for k in ("ready", "waiting", "needs_advise", "ask", "eyes", "punt")
        ):
            print("## Beads · 0")
            print()
            print("(none)")
            print()

    if show_parked:
        parked = data.get("parked") or []
        if parked:
            print(f"## Parked · {len(parked)}")
            print("OpenSpec.")
            print()
            for row in parked:
                print_change(row)
            print()
        elif not show_ready:
            print("## Parked · 0")
            print()
            print("(none)")
            print()

    if missing == "openspec":
        if data.get("beads"):
            print("No `openspec/` from cwd — OpenSpec lens empty; beads still shown.")
        else:
            print("No `openspec/` from cwd — not a guessed ready-set.")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=None)
    p.add_argument("--json", action="store_true")
    p.add_argument("--ready", action="store_true")
    p.add_argument("--parked", action="store_true")
    p.add_argument(
        "--queue",
        action="store_true",
        help="honest open pile: unblocked leaves + OpenSpec READY, plus blocked",
    )
    p.add_argument(
        "--beads-json",
        type=Path,
        help="fixture beads instead of `bd list --ready`",
    )
    p.add_argument(
        "--blocked-json",
        type=Path,
        help="fixture blocked beads instead of `bd blocked`",
    )
    args = p.parse_args()
    if args.beads_json is not None:
        beads = load_beads_json(args.beads_json)
    else:
        beads = load_beads()
    if args.blocked_json is not None:
        blocked = load_blocked_json(args.blocked_json)
    elif args.beads_json is not None:
        blocked = []
    else:
        blocked = load_blocked()
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
    if args.queue:
        face = build_queue(data, blocked=blocked)
        if args.json:
            print(json.dumps(face, indent=2))
            return 0
        print_queue(face)
        return 0
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
