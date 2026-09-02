#!/usr/bin/env python3
"""Campaign observe + stop predicate. Does not spawn workers.

Lives next to the run skill so a global `skills add` carries it.
Uses the sibling ready skill's script against the current project's
openspec/. Does not require the project to vendor ready.py.

  python3 <skill-dir>/scripts/run.py [scope] [--until …] [--skip id,id] [--punt id,id]
  python3 <skill-dir>/scripts/run.py add-x --until advise --ready-json FILE
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

STOPS = ("empty", "advise", "activation", "ask", "fold", "roll")
ADVISE_RE = re.compile(
    r"^>\s*\*\*ADVISE:\*\*\s*(accept-with-nits|accept|send-back)\b",
    re.I,
)
STAGES = ("intend", "change", "advise", "act", "fold")
CHANGE_ID_RE = re.compile(
    r"^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
BANNER_RE = re.compile(r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b")
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")
EYES_RE = re.compile(r"\b(ASK|EYES|by-eye|human-verify|human verify)\b", re.I)
WALK = frozenset({"roll", "ask"})


def sibling_ready_py() -> Path | None:
    cand = Path(__file__).resolve().parents[2] / "ready" / "scripts" / "ready.py"
    return cand if cand.is_file() else None


def find_openspec() -> Path | None:
    here = Path.cwd()
    for root in [here, *here.parents]:
        cand = root / "openspec"
        if cand.is_dir():
            return cand
        if (root / ".git").exists():
            return cand if cand.is_dir() else None
    return None


def find_ready_py() -> Path | None:
    sib = sibling_ready_py()
    if sib:
        return sib
    here = Path.cwd()
    for root in [here, *here.parents]:
        cand = root / "scripts" / "ready.py"
        if cand.is_file():
            return cand
        if (root / ".git").exists() or (root / "openspec").is_dir():
            break
    return None


def find_change_dir(openspec: Path | None, change_id: str) -> Path | None:
    if openspec is None or not change_id:
        return None
    cand = openspec / "changes" / change_id
    if cand.is_dir() and (cand / "proposal.md").is_file():
        return cand
    return None


def is_change_id(scope: str | None) -> bool:
    return bool(scope and CHANGE_ID_RE.match(scope))


def first_banner(text: str) -> str | None:
    for i, line in enumerate(text.splitlines()):
        if i >= 40:
            break
        m = BANNER_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def open_owed(tasks: str) -> list[str]:
    open_items: list[str] = []
    for line in tasks.splitlines():
        m = CHECKBOX_RE.match(line)
        if not m:
            continue
        if m.group(2).lower() != "x":
            open_items.append(m.group(3).strip())
    return open_items


def landing_from_title(title: str) -> str | None:
    if not title:
        return None
    head = title.strip().split()[0].rstrip(":")
    return head if is_change_id(head) else None


def last_advise_verdict(change_dir: Path) -> str | None:
    reviews = change_dir / "reviews"
    if not reviews.is_dir():
        return None
    files = sorted(
        p for p in reviews.iterdir() if p.is_file() and p.name.endswith(".md")
    )
    if not files:
        return None
    text = files[-1].read_text(encoding="utf-8")
    for line in text.splitlines()[:40]:
        m = ADVISE_RE.match(line.strip())
        if m:
            return m.group(1).lower()
    return None


def eyes_ids(openspec: Path | None) -> list[str]:
    if openspec is None:
        return []
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    out: list[str] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        tasks = child / "tasks.md"
        if not tasks.is_file():
            continue
        for item in open_owed(tasks.read_text(encoding="utf-8")):
            if EYES_RE.search(item):
                out.append(child.name)
                break
    return out


def unique(ids_: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for i in ids_:
        if i and i not in seen:
            seen.add(i)
            out.append(i)
    return out


def without(ids_: list[str], skip: set[str]) -> list[str]:
    return [i for i in ids_ if i not in skip]


def parse_skip(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def open_owed_for(change_dir: Path) -> list[str]:
    tasks = change_dir / "tasks.md"
    if not tasks.is_file():
        return []
    return open_owed(tasks.read_text(encoding="utf-8"))


def fold_legal_ids(
    openspec: Path | None,
    needs_advise: list[str] | None = None,
) -> list[str]:
    if openspec is None:
        return []
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    out: list[str] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        if fold_legal(openspec, child.name, needs_advise):
            out.append(child.name)
    return out


def _active_inflight(openspec: Path | None) -> list[Path]:
    if openspec is None:
        return []
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    out: list[Path] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        if not (child / "proposal.md").is_file():
            continue
        if first_banner((child / "proposal.md").read_text(encoding="utf-8")) != "ACTIVE BUILD":
            continue
        out.append(child)
    return out


def send_back_ids(openspec: Path | None) -> list[str]:
    """Last advise send-back AND open owed boxes → amend (change), not fold."""
    out: list[str] = []
    for child in _active_inflight(openspec):
        if last_advise_verdict(child) == "send-back" and open_owed_for(child):
            out.append(child.name)
    return out


def send_back_stuck_ids(openspec: Path | None) -> list[str]:
    """Last send-back, no open boxes → re-advise / park, not change, not fold."""
    out: list[str] = []
    for child in _active_inflight(openspec):
        if last_advise_verdict(child) == "send-back" and not open_owed_for(child):
            out.append(child.name)
    return out


def load_beads() -> list[dict[str, Any]]:
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
    if not isinstance(data, list):
        return []
    return [row for row in data if isinstance(row, dict)]


def fold_legal(
    openspec: Path | None,
    change_id: str,
    needs_advise: list[str] | None = None,
) -> bool:
    """ACTIVE BUILD, no open owed box, not PARKED, not needs_advise."""
    dest = find_change_dir(openspec, change_id)
    if dest is None:
        return False
    if needs_advise and change_id in needs_advise:
        return False
    banner = first_banner((dest / "proposal.md").read_text(encoding="utf-8"))
    if banner != "ACTIVE BUILD":
        return False
    if open_owed_for(dest):
        return False
    return True


def load_ready(path: Path | None) -> dict[str, Any]:
    if path:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SystemExit("ready-json must be an object")
        return data
    ready_py = find_ready_py()
    if ready_py is None:
        return {
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
            "missing": "ready.py",
        }
    argv = [sys.executable, str(ready_py), "--json"]
    openspec = find_openspec()
    if openspec is not None:
        argv.extend(["--root", str(openspec)])
    proc = subprocess.run(
        argv,
        check=False,
        capture_output=True,
        text=True,
        cwd=str(Path.cwd()),
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or "ready.py failed")
    return json.loads(proc.stdout)


def ids(rows: Any) -> list[str]:
    if not isinstance(rows, list):
        return []
    out: list[str] = []
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            out.append(str(row["id"]))
        elif isinstance(row, str):
            out.append(row)
    return out


def decide(
    data: dict[str, Any],
    until: str,
    pause_before: str | None,
    scope: str | None,
    openspec: Path | None,
    skip: list[str] | None = None,
    punt: list[str] | None = None,
) -> dict[str, Any]:
    if data.get("missing") == "ready.py":
        return {
            "stop": "no-ready",
            "next": None,
            "focus": scope,
            "until": until,
            "workers_launched": 0,
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
        }
    skip_set = set(skip or [])
    punt_set = set(punt or [])
    ready = ids(data.get("ready"))
    waiting = ids(data.get("waiting"))
    needs_advise = ids(data.get("needs_advise"))
    asks = ids(data.get("ask"))
    eyes = (
        ids(data.get("eyes"))
        if data.get("eyes") is not None
        else eyes_ids(openspec)
    )
    elicited = unique(asks + waiting + eyes)
    # Fold-skip is not an elicitation. Punt is last-resort when no
    # other-family advise route exists (mailbox PUNT). Same-family
    # advise is spawn, not punt.
    asks = unique(elicited + list(punt_set))
    if pause_before and (
        pause_before in ready
        or pause_before in waiting
        or pause_before in needs_advise
        or pause_before == scope
    ):
        return face("pause-before", pause_before, until, ready, waiting, needs_advise, asks)
    if until == "ask" and elicited:
        return face("ask", elicited[0], until, ready, waiting, needs_advise, elicited)
    if until == "activation" and waiting:
        focus = scope if scope in waiting else waiting[0]
        return face("activation", focus, until, ready, waiting, needs_advise, asks)
    if scope and scope in waiting:
        return face("activation", scope, until, ready, waiting, needs_advise, asks)

    if scope and (scope in skip_set or scope in punt_set):
        scope = None

    if data.get("send_back") is not None:
        send_ids = ids(data.get("send_back"))
        stuck = []
    elif until in WALK:
        send_ids = send_back_ids(openspec)
        stuck = send_back_stuck_ids(openspec)
    else:
        send_ids = []
        stuck = []
    needs_advise = unique(needs_advise + stuck)

    if data.get("fold_legal") is not None:
        fold_ids = ids(data.get("fold_legal"))
    elif until in {"fold", "roll", "ask"}:
        fold_ids = fold_legal_ids(openspec, needs_advise)
    else:
        fold_ids = []
    fold_ids = [i for i in fold_ids if i not in needs_advise]

    raw_beads = data.get("beads")
    if raw_beads is None:
        beads = load_beads() if until in WALK else []
    elif isinstance(raw_beads, list):
        beads = [b for b in raw_beads if isinstance(b, dict)]
    else:
        beads = []

    blocked = skip_set | punt_set
    pick_fold = without(fold_ids, blocked)
    pick_send = without(send_ids, blocked)
    # Fold-skip still advises — that is how a refused fold unsticks.
    pick_advise = without(needs_advise, punt_set)
    pick_ready = without(ready, blocked)

    if until in {"fold", "roll", "ask"} and not scope and pick_fold:
        return {
            "stop": None,
            "next": "fold",
            "focus": pick_fold[0],
            "until": until,
            "workers_launched": 0,
            "ready": ready,
            "waiting": waiting,
            "needs_advise": needs_advise,
            "ask": asks,
        }
    if until == "fold" and not scope:
        return face("empty", None, until, ready, waiting, needs_advise, asks)

    if until in WALK and not scope:
        if pick_send:
            return {
                "stop": None,
                "next": "change",
                "focus": pick_send[0],
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        if pick_advise:
            return {
                "stop": None,
                "next": "advise",
                "focus": pick_advise[0],
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        if pick_ready:
            return {
                "stop": None,
                "next": "act",
                "focus": pick_ready[0],
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        for bead in beads:
            title = str(bead.get("title") or "")
            kind = str(bead.get("issue_type") or bead.get("type") or "").lower()
            landing = landing_from_title(title)
            nid = str(bead.get("id") or "")
            if nid in blocked or (landing and landing in blocked):
                continue
            if landing and find_change_dir(openspec, landing) is None:
                return {
                    "stop": None,
                    "next": "change",
                    "focus": landing,
                    "until": until,
                    "workers_launched": 0,
                    "ready": ready,
                    "waiting": waiting,
                    "needs_advise": needs_advise,
                    "ask": asks,
                }
            if (
                kind in {"task", "feature"}
                and not landing
                and not title.lower().startswith("nod-")
            ):
                if nid:
                    return {
                        "stop": None,
                        "next": "intend",
                        "focus": nid,
                        "until": until,
                        "workers_launched": 0,
                        "ready": ready,
                        "waiting": waiting,
                        "needs_advise": needs_advise,
                        "ask": asks,
                    }
        return face("empty", None, until, ready, waiting, needs_advise, asks)

    # Decision table (not a preference order):
    # verb-led kebab → change-id; anything else with a scope → goal / intend.
    if scope and not is_change_id(scope):
        return {
            "stop": None,
            "next": "intend",
            "focus": scope,
            "until": until,
            "workers_launched": 0,
            "ready": ready,
            "waiting": waiting,
            "needs_advise": needs_advise,
            "ask": asks,
        }

    if scope and is_change_id(scope):
        if find_change_dir(openspec, scope) is None:
            return {
                "stop": None,
                "next": "change",
                "focus": scope,
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        if (
            until in {"fold", "roll", "ask"}
            and fold_legal(openspec, scope, needs_advise)
        ):
            return {
                "stop": None,
                "next": "fold",
                "focus": scope,
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        if until == "fold":
            return face("empty", scope, until, ready, waiting, needs_advise, asks)
        if until in WALK and scope in pick_send:
            return {
                "stop": None,
                "next": "change",
                "focus": scope,
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }

    advise_ids = [scope] if scope and scope in pick_advise else list(pick_advise)
    ready_ids = [scope] if scope and scope in pick_ready else list(pick_ready)
    if scope and scope in pick_advise:
        ready_ids = [scope] if scope in pick_ready else []

    if advise_ids:
        return {
            "stop": None,
            "next": "advise",
            "focus": advise_ids[0],
            "until": until,
            "workers_launched": 0,
            "ready": ready,
            "waiting": waiting,
            "needs_advise": needs_advise,
            "ask": asks,
        }
    if until == "advise":
        return face("empty", scope, until, ready, waiting, needs_advise, asks)
    if ready_ids:
        return {
            "stop": None,
            "next": "act",
            "focus": ready_ids[0],
            "until": until,
            "workers_launched": 0,
            "ready": ready,
            "waiting": waiting,
            "needs_advise": needs_advise,
            "ask": asks,
        }
    return face("empty", scope, until, ready, waiting, needs_advise, asks)


def face(
    why: str,
    focus: str | None,
    until: str,
    ready: list[str],
    waiting: list[str],
    needs_advise: list[str],
    asks: list[str],
) -> dict[str, Any]:
    return {
        "stop": why,
        "next": None,
        "focus": focus,
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
    }


def card(row: dict[str, Any]) -> str:
    stop = row["stop"] or "continue"
    focus = row.get("focus") or "—"
    return (
        f"┌─ RUN ─────────────────────────────────────────\n"
        f"│ until {row['until']} · stop {stop} · workers {row['workers_launched']}\n"
        f"│ next {row['next'] or '—'} · focus {focus}\n"
        f"│ ready {len(row['ready'])} · pending {len(row['waiting'])} · "
        f"advise {len(row['needs_advise'])} · ask {len(row['ask'])}\n"
        f"└───────────────────────────────────────────────"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scope", nargs="?", help="change-id to focus (e.g. add-sheaf-type)")
    p.add_argument("--until", choices=STOPS, default="roll")
    p.add_argument("--autonomous", action="store_true")
    p.add_argument("--pause-before")
    p.add_argument(
        "--skip",
        default="",
        help="exclude from fold/change/act/beads this pick; still advise",
    )
    p.add_argument(
        "--punt",
        default="",
        help="last-resort: exclude from this pick including advise (no other-family route)",
    )
    p.add_argument("--ready-json", type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    data = load_ready(args.ready_json)
    row = decide(
        data,
        args.until,
        args.pause_before,
        args.scope,
        find_openspec(),
        parse_skip(args.skip),
        parse_skip(args.punt),
    )
    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(card(row))
        print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
