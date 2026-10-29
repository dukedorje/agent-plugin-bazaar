#!/usr/bin/env python3
"""Campaign observe + stop predicate. Does not spawn workers.

Lives next to the run skill so a global `skills add` carries it.
Uses the sibling ready skill's script against the current project's
openspec/. Does not require the project to vendor ready.py.

  python3 <skill-dir>/scripts/run.py [scope] [--wait] [--tidy] [--no-fold] [--no-beads]
  python3 <skill-dir>/scripts/run.py add-x --until advise --ready-json FILE
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

_STATUS_SCRIPTS = Path(__file__).resolve().parents[2] / "status" / "scripts"
if str(_STATUS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_STATUS_SCRIPTS))
from advise_status import last_advise_verdict  # noqa: E402
from status import describe_blocker  # noqa: E402

STOPS = ("empty", "advise", "activation", "ask", "eyes", "fold", "roll")
STAGES = ("intend", "change", "advise", "act", "fold")
CHANGE_ID_RE = re.compile(
    r"^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
NODE_TYPES = frozenset({"node", "work-node"})
BANNER_RE = re.compile(r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b")
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")
EYES_RE = re.compile(r"\b(EYES|by-eye|human-verify|human verify)\b", re.I)
SPIKE_RE = re.compile(r"(?im)^\s*-\s*Spike:\s*(.+?)\s*$")
NEXT_CMD_RE = re.compile(r"Next:\s*(.+)$", re.I)
WALK = frozenset({"roll", "ask"})


def sibling_ready_py() -> Path | None:
    parent = Path(__file__).resolve().parents[2]
    for rel in (
        ("status", "scripts", "status.py"),
        ("ready", "scripts", "ready.py"),
        ("status", "scripts", "ready.py"),
    ):
        cand = parent.joinpath(*rel)
        if cand.is_file():
            return cand
    return None


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
        for name in ("status.py", "ready.py"):
            cand = root / "scripts" / name
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


def is_graph_node_bead(bead: dict[str, Any]) -> bool:
    """DAG node: beads type `node`, not a `nod-` title prefix."""
    kind = str(bead.get("issue_type") or bead.get("type") or "").lower()
    if kind in NODE_TYPES:
        return True
    title = str(bead.get("title") or "")
    return title.lower().startswith("nod-")


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


def next_command(item: str) -> str | None:
    m = NEXT_CMD_RE.search((item or "").strip())
    if not m:
        return None
    cmd = m.group(1).strip().strip("`").strip()
    return cmd or None


def looks_for(data: dict[str, Any], openspec: Path | None) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    rows = data.get("eyes")
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and row.get("id"):
                nid = str(row["id"])
                items = [str(x) for x in (row.get("open") or []) if x]
                if not items:
                    items = [""]
                for item in items:
                    if item and not EYES_RE.search(item):
                        continue
                    out.append(
                        {
                            "id": nid,
                            "look": item,
                            "command": next_command(item) or "/status",
                        }
                    )
            elif isinstance(row, str):
                out.append({"id": row, "look": "", "command": "/status"})
    if "eyes" in data:
        return out
    if openspec is None:
        return []
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        tasks = child / "tasks.md"
        if not tasks.is_file():
            continue
        for item in open_owed(tasks.read_text(encoding="utf-8")):
            if not EYES_RE.search(item):
                continue
            out.append(
                {
                    "id": child.name,
                    "look": item,
                    "command": next_command(item) or "/status",
                }
            )
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


def fold_base_module():
    path = Path(__file__).resolve().parents[2] / "fold" / "scripts" / "fold_base.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("fold_base", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stale_base_ids(openspec: Path | None, candidates: list[str]) -> list[str]:
    """Fold-legal ids whose pasted requirements no longer match their base."""
    module = fold_base_module()
    if module is None or openspec is None:
        return []
    stale: list[str] = []
    for change_id in candidates:
        dest = find_change_dir(openspec, change_id)
        if dest is None:
            continue
        report = module.classify(dest)
        if report.get("stale"):
            stale.append(change_id)
    return stale


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


def load_graph() -> list[dict[str, Any]]:
    """Every bead with its edges: owed-work and scope resolution need parents."""
    try:
        proc = subprocess.run(
            ["bd", "list", "--all", "-n", "0", "--json"],
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
    return [row for row in data if isinstance(row, dict)] if isinstance(data, list) else []


def bead_parent(bead: dict[str, Any]) -> str | None:
    nid = str(bead.get("id") or "")
    for edge in bead.get("dependencies") or []:
        if (
            isinstance(edge, dict)
            and edge.get("type") == "parent-child"
            and str(edge.get("issue_id") or nid) == nid
            and edge.get("depends_on_id")
        ):
            return str(edge["depends_on_id"])
    return bead.get("parent") and str(bead["parent"])


def owed_beads(change_id: str, graph: list[dict[str, Any]]) -> list[str]:
    """Open descendants of the bead(s) landing on change_id.

    tasks.md may be a pointer to beads rather than checkboxes, so an empty
    markdown list is not proof of no owed work.
    """
    roots = {
        str(b.get("id"))
        for b in graph
        if landing_from_title(str(b.get("title") or "")) == change_id
    }
    if not roots:
        return []
    kids: dict[str, list[dict[str, Any]]] = {}
    for b in graph:
        parent = bead_parent(b)
        if parent:
            kids.setdefault(parent, []).append(b)
    owed: list[str] = []
    seen: set[str] = set()
    stack = list(roots)
    while stack:
        cur = stack.pop()
        for child in kids.get(cur, []):
            cid = str(child.get("id") or "")
            if not cid or cid in seen:
                continue
            seen.add(cid)
            if str(child.get("status") or "open") not in {"closed", "tombstone"}:
                owed.append(cid)
            stack.append(cid)
    return sorted(owed)


def scope_bead(scope: str, graph: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Beads named by scope: exact id, or a short alias (`ai0` for `mesh-ai0`)."""
    exact = [b for b in graph if str(b.get("id") or "") == scope]
    if exact:
        return exact
    return [b for b in graph if str(b.get("id") or "").endswith("-" + scope)]


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


def resolve_until(
    until: str | None,
    *,
    wait: bool = False,
    tidy: bool = False,
    no_fold: bool = False,
    no_beads: bool = False,
) -> tuple[str, bool, bool]:
    """Operator flags win when --until is omitted. --until stays an alias."""
    if wait:
        until = until or "ask"
    if tidy:
        until = until or "fold"
    if until is None:
        if no_fold and no_beads:
            return "empty", False, False
        return "roll", no_fold, no_beads
    return until, no_fold, no_beads


def decide(
    data: dict[str, Any],
    until: str,
    pause_before: str | None,
    scope: str | None,
    openspec: Path | None,
    skip: list[str] | None = None,
    punt: list[str] | None = None,
    no_fold: bool = False,
    no_beads: bool = False,
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
    raw_graph = data.get("graph")
    graph_box: list[list[dict[str, Any]]] = []
    if isinstance(raw_graph, list):
        graph_box.append([b for b in raw_graph if isinstance(b, dict)])

    def graph() -> list[dict[str, Any]]:
        # Fixtures without a graph never call bd.
        if not graph_box:
            graph_box.append(load_graph() if data.get("beads") is None else [])
        return graph_box[0]

    # An epic / bead id is a scope, not a goal: resolve it to its landing
    # instead of routing to a duplicate intend.
    if scope and not is_change_id(scope):
        named = scope_bead(scope, graph())
        if len(named) > 1:
            row = face("scope-ambiguous", scope, until, [], [], [], [])
            row["diagnostic"] = "matches " + ", ".join(str(b.get("id")) for b in named)
            return row
        if named:
            landing = landing_from_title(str(named[0].get("title") or ""))
            if not landing:
                row = face("scope-unresolved", str(named[0].get("id")), until, [], [], [], [])
                row["diagnostic"] = (
                    f"bead {named[0].get('id')} has no change landing in its title; "
                    f"run /map {named[0].get('id')} or name a child change-id"
                )
                return row
            scope = landing
    ready = ids(data.get("ready"))
    waiting = ids(data.get("waiting"))
    needs_advise = ids(data.get("needs_advise"))
    ask_ids = ids(data.get("ask"))
    eyes = (
        ids(data.get("eyes"))
        if data.get("eyes") is not None
        else eyes_ids(openspec)
    )
    # Fold-skip is not an elicitation. Punt is last-resort when no
    # other-family advise route exists (mailbox PUNT). Same-family
    # advise is spawn, not punt. EYES is its own face, not ASK.
    asks = unique(ask_ids + waiting + list(punt_set))
    if pause_before and (
        pause_before in ready
        or pause_before in waiting
        or pause_before in needs_advise
        or pause_before == scope
    ):
        return face("pause-before", pause_before, until, ready, waiting, needs_advise, asks)
    if until == "ask" and waiting:
        return face("ask", waiting[0], until, ready, waiting, needs_advise, asks)
    if until == "ask" and ask_ids:
        return face("ask", ask_ids[0], until, ready, waiting, needs_advise, asks)
    if until == "ask" and eyes:
        return face("eyes", eyes[0], until, ready, waiting, needs_advise, asks)
    if until == "activation" and waiting:
        focus = scope if scope in waiting else waiting[0]
        return face("activation", focus, until, ready, waiting, needs_advise, asks)
    if scope and scope in waiting:
        return face("activation", scope, until, ready, waiting, needs_advise, asks)

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

    # A refused or punted scope stays scoped. Skip never widens the
    # named campaign to unrelated work; it still advises the same id.
    if scope and (scope in skip_set or scope in punt_set):
        if scope in skip_set and scope in needs_advise:
            return {
                "stop": None,
                "next": "advise",
                "focus": scope,
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        row = face("skipped", scope, until, ready, waiting, needs_advise, asks)
        row["diagnostic"] = f"{scope} is skipped/punted; drop the scope to walk other work"
        return row

    if data.get("fold_legal") is not None:
        fold_ids = ids(data.get("fold_legal"))
    elif until in {"fold", "roll", "ask"}:
        fold_ids = fold_legal_ids(openspec, needs_advise)
    else:
        fold_ids = []
    fold_ids = [i for i in fold_ids if i not in needs_advise]
    if fold_ids:
        fold_ids = [i for i in fold_ids if not owed_beads(i, graph())]

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
    # A stale base is not that skip. It is change, in this same run.
    pick_advise = without(needs_advise, punt_set)
    pick_ready = without(ready, blocked)
    stale = [] if no_fold else stale_base_ids(openspec, pick_fold)
    pick_fold = without(pick_fold, set(stale))

    if until in {"fold", "roll", "ask"} and not scope and pick_fold and not no_fold:
        return fold_row(
            pick_fold[0], until, ready, waiting, needs_advise, asks, openspec
        )
    if until in {"fold", "roll", "ask"} and not scope and stale and not no_fold:
        return stale_row(
            stale[0], stale, until, ready, waiting, needs_advise, asks
        )
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
                "prepare_before_act": unique(pick_ready),
                "until": until,
                "workers_launched": 0,
                "ready": ready,
                "waiting": waiting,
                "needs_advise": needs_advise,
                "ask": asks,
            }
        for bead in beads if not no_beads else []:
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
                and not is_graph_node_bead(bead)
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
        owed = (
            owed_beads(scope, graph())
            if until in {"fold", "roll", "ask"} and fold_legal(openspec, scope, needs_advise)
            else []
        )
        if owed:
            row = face("owed-beads", scope, until, ready, waiting, needs_advise, asks)
            row["owed"] = owed
            row["diagnostic"] = (
                f"{scope} has {len(owed)} open bead(s) under it; not fold-legal. "
                "Run a child landing or /map the umbrella"
            )
            return row
        if (
            until in {"fold", "roll", "ask"}
            and not no_fold
            and fold_legal(openspec, scope, needs_advise)
        ):
            scoped_stale = stale_base_ids(openspec, [scope])
            if scoped_stale:
                return stale_row(
                    scope, scoped_stale, until, ready, waiting, needs_advise, asks
                )
            return fold_row(
                scope, until, ready, waiting, needs_advise, asks, openspec
            )
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
            "prepare_before_act": unique(ready_ids),
            "until": until,
            "workers_launched": 0,
            "ready": ready,
            "waiting": waiting,
            "needs_advise": needs_advise,
            "ask": asks,
        }
    return face("empty", scope, until, ready, waiting, needs_advise, asks)


def fold_row(
    focus: str,
    until: str,
    ready: list[str],
    waiting: list[str],
    needs_advise: list[str],
    asks: list[str],
    openspec: Path | None,
) -> dict[str, Any]:
    row = {
        "stop": None,
        "next": "fold",
        "focus": focus,
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
    }
    module = fold_base_module()
    dest = find_change_dir(openspec, focus)
    if module is not None and dest is not None:
        report = module.classify(dest)
        names = [
            f"{item['capability']}: {item['requirement']}"
            for item in report.get("unstamped") or []
        ]
        if names:
            row["unstamped_base"] = names
            row["diagnostic"] = (
                "unstamped base; diff by hand and stamp before applying"
            )
    return row


def stale_row(
    focus: str,
    stale: list[str],
    until: str,
    ready: list[str],
    waiting: list[str],
    needs_advise: list[str],
    asks: list[str],
) -> dict[str, Any]:
    return {
        "stop": None,
        "next": "change",
        "focus": focus,
        "reason": "stale-base",
        "stale_base": stale,
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
        "diagnostic": (
            f"{focus} paste is stale; re-paste from the living requirement "
            "and stamp the base. Do not fold it."
        ),
    }


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
        "eyes": [],
        "next_steps": [],
    }


def apply_eyes_stop(
    row: dict[str, Any],
    data: dict[str, Any],
    openspec: Path | None,
) -> dict[str, Any]:
    """EYES is a halt, not a quiet empty. Unrelated READY may still move."""
    looks = looks_for(data, openspec)
    eyes = unique([str(x.get("id") or "") for x in looks] + ids(data.get("eyes")))
    row = dict(row)
    row["eyes"] = eyes
    row["next_steps"] = looks
    until = str(row.get("until") or "")
    focus = row.get("focus")
    nxt = row.get("next")
    stop = row.get("stop")
    if until == "ask" and stop == "ask" and focus in eyes and focus not in ids(
        data.get("waiting")
    ) and focus not in ids(data.get("ask")):
        row["stop"] = "eyes"
        row["next"] = None
    if until in WALK and eyes:
        if stop is None and nxt in {"act", "fold"} and focus in eyes:
            row["stop"] = "eyes"
            row["next"] = None
        elif stop is None and nxt == "intend":
            row["stop"] = "eyes"
            row["focus"] = eyes[0]
            row["next"] = None
        elif (
            stop is None
            and nxt == "change"
            and isinstance(focus, str)
            and find_change_dir(openspec, focus) is None
        ):
            row["stop"] = "eyes"
            row["focus"] = eyes[0]
            row["next"] = None
        elif stop == "empty":
            row["stop"] = "eyes"
            row["focus"] = eyes[0]
            row["next"] = None
    # This is a conductor obligation, not semantic reconciliation or permission.
    row["prepare_before_act"] = (
        without(row.get("prepare_before_act", []), set(eyes))
        if row.get("next") == "act" and row.get("stop") is None
        else []
    )
    return row


def spike_still_open(text: str) -> bool:
    found = False
    for match in SPIKE_RE.finditer(text or ""):
        low = match.group(1).strip().lower().replace("—", "-")
        tail = low.split("-")[-1].strip()
        if tail in {"go", "skipped"} or low.startswith(("go", "skipped")):
            continue
        if "override" in low:
            continue
        found = True
    return found


def _prio(row: dict[str, Any]) -> int:
    try:
        return int(row.get("priority"))
    except (TypeError, ValueError):
        return 99


def _join_and(parts: list[str]) -> str:
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def _blocker_bits(item: object) -> str:
    info = describe_blocker(item)
    if info["gate"] == "human":
        return f"human gate `{info['id']}`"
    if info["gate"]:
        return f"{info['gate']} gate `{info['id']}`"
    if info["external"]:
        where = str(info["source"] or "another project")
        if info["where"]:
            where = f"{where} at {info['where']}"
        state = str(info["status"] or "not closed")
        return f"`{info['id']}` in {where} ({state})"
    state = str(info["status"] or "open")
    where = str(info["source"] or "this repo")
    return f"`{info['id']}` ({state}, {where})"


def _do_bits(items: list[object]) -> str:
    infos = [describe_blocker(item) for item in items]
    bits: list[str] = []
    externals = [info for info in infos if info["external"]]
    gates = [info for info in infos if info["gate"]]
    local = [info for info in infos if not info["external"] and not info["gate"]]
    if externals:
        names = _join_and([str(info["source"] or "that project") for info in externals])
        bits.append(f"fix or close the bead in {names}")
    if any(info["gate"] == "human" for info in gates):
        bits.append("close the human gate")
    if any(info["gate"] in {"gh:run", "gh:pr", "timer", "bead"} for info in gates):
        bits.append("let the gate finish, or resolve it")
    if local:
        names = ", ".join(f"`{info['id']}`" for info in local[:3])
        bits.append(f"run or close {names}")
    if not bits:
        return "See `status`."
    return "Do: " + "; ".join(bits) + "."


def _lead(row: dict[str, Any]) -> str | None:
    stop = str(row.get("stop") or "")
    focus = row.get("focus") or "that bead"
    leads = {
        "ask": f"`{focus}` is waiting on you. Run `steer`. The loop will not decide it.",
        "activation": (
            f"`{focus}` is PENDING. Activate it (`steer`, or the campaign grant) "
            "before the loop will build it."
        ),
        "eyes": f"`{focus}` needs your eyes. Look, then check the box. The loop will not.",
        "pause-before": (
            f"Paused before `{focus}`. Drop `--pause-before` when you want the loop to take it."
        ),
        "owed-beads": f"`{focus}` still has open beads. Run or close them before fold.",
        "skipped": f"`{focus}` is skipped. Drop the scope to walk other work.",
        "scope-ambiguous": f"`{focus}` matches more than one bead. Name the child.",
        "scope-unresolved": (
            f"`{focus}` has no change landing. `map` it, or name a child change-id."
        ),
    }
    return leads.get(stop)


def _order_note(ready: list[dict[str, Any]], blocked: list[dict[str, Any]]) -> str | None:
    if len(ready) < 2 or not blocked:
        return None
    unblocks: dict[str, list[str]] = {}
    for issue in blocked:
        nid = str(issue.get("id") or "")
        raw = issue.get("blocked_by") or []
        if not isinstance(raw, list):
            raw = [raw]
        for item in raw:
            info = describe_blocker(item)
            blocker_id = str(info["raw_id"] or info["id"] or "")
            if blocker_id and nid:
                unblocks.setdefault(blocker_id, []).append(nid)
        for item in issue.get("gated_by") or []:
            info = describe_blocker(item)
            blocker_id = str(info["raw_id"] or info["id"] or "")
            if blocker_id and nid:
                unblocks.setdefault(blocker_id, []).append(nid)
    if not unblocks:
        return None

    def dep_key(bead: dict[str, Any]) -> tuple:
        count = len(unblocks.get(str(bead.get("id") or ""), []))
        return (-count, _prio(bead), str(bead.get("id") or ""))

    by_priority = sorted(ready, key=lambda bead: (_prio(bead), str(bead.get("id") or "")))
    by_dependency = sorted(ready, key=dep_key)
    first_pri = by_priority[0]
    first_dep = by_dependency[0]
    if str(first_pri.get("id") or "") == str(first_dep.get("id") or ""):
        return None
    unlocked = unblocks.get(str(first_dep.get("id") or ""), [])
    if not unlocked:
        return None
    names = ", ".join(f"`{nid}`" for nid in unlocked[:4])
    if _prio(first_dep) == _prio(first_pri):
        why = "Same priority; the id sort would do the other one first."
    else:
        why = "Priority would leave that chain waiting."
    return (
        f"Order: do `{first_dep.get('id')}` (P{_prio(first_dep)}) before "
        f"`{first_pri.get('id')}` (P{_prio(first_pri)}). It blocks {names}. "
        f"{why}"
    )


def human_unblock(row: dict[str, Any], data: dict[str, Any]) -> list[str]:
    """What a person does when a stop left a bead unexecuted.

    Empty when the loop is still going, or when nothing open explains the stop.
    """
    if row.get("stop") is None:
        return []
    if row.get("stop") == "no-ready":
        return []
    lines: list[str] = []
    lead = _lead(row)
    if lead:
        lines.append(lead)

    blocked = data.get("blocked") if isinstance(data.get("blocked"), list) else []
    actionable: list[tuple[dict[str, Any], list[Any]]] = []
    for issue in blocked:
        if not isinstance(issue, dict) or not issue.get("id"):
            continue
        raw = list(issue.get("blocked_by") or [])
        raw.extend(issue.get("gated_by") or [])
        if raw:
            actionable.append((issue, raw))
    for issue, raw in actionable[:6]:
        waiting = _join_and([_blocker_bits(item) for item in raw[:4]])
        lines.append(
            f"`{issue['id']}` stayed open. Waiting on {waiting}. {_do_bits(raw)}"
        )
    extra = len(actionable) - 6
    if extra > 0:
        lines.append(f"{extra} more open beads are blocked. `status --queue` lists them.")

    seen: set[str] = set()
    pools: list[Any] = []
    if isinstance(data.get("ready_beads"), list):
        pools.extend(data["ready_beads"])
    pools.extend(blocked)
    if isinstance(data.get("beads"), list):
        pools.extend(data["beads"])
    for bead in pools:
        if not isinstance(bead, dict):
            continue
        nid = str(bead.get("id") or "")
        if not nid or nid in seen:
            continue
        if not spike_still_open(str(bead.get("description") or "")):
            continue
        seen.add(nid)
        lines.append(
            f"`{nid}` has an open spike. Spike now, or note a skip. The loop will not land it."
        )

    ready = data.get("ready_beads") if isinstance(data.get("ready_beads"), list) else []
    ready_dicts = [bead for bead in ready if isinstance(bead, dict) and bead.get("id")]
    note = _order_note(ready_dicts, [b for b in blocked if isinstance(b, dict)])
    if note:
        lines.append(note)
    return lines


def load_explain() -> dict[str, Any]:
    """`bd ready --explain` when this is a live board, not a fixture."""
    try:
        proc = subprocess.run(
            ["bd", "ready", "--explain", "--json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=str(Path.cwd()),
        )
    except OSError:
        return {}
    if proc.returncode != 0 or not proc.stdout.strip():
        return {}
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {}
    if isinstance(payload, dict) and "blocked" not in payload and isinstance(payload.get("data"), dict):
        payload = payload["data"]
    return payload if isinstance(payload, dict) else {}


def card(row: dict[str, Any]) -> str:
    stop = row["stop"] or "continue"
    focus = row.get("focus") or "—"
    eyes = row.get("eyes") or []
    lines = [
        "┌─ RUN ─────────────────────────────────────────",
        f"│ until {row['until']} · stop {stop} · workers {row['workers_launched']}",
        f"│ next {row['next'] or '—'} · focus {focus}",
        f"│ ready {len(row['ready'])} · pending {len(row['waiting'])} · "
        f"advise {len(row['needs_advise'])} · ask {len(row['ask'])} · "
        f"eyes {len(eyes)}",
        "└───────────────────────────────────────────────",
    ]
    if row.get("prepare_before_act"):
        lines.insert(-1, "│ prepare before act: " + ", ".join(row["prepare_before_act"]))
    if row.get("reason"):
        lines.insert(-1, "│ reason " + str(row["reason"]))
    if row.get("diagnostic"):
        lines.insert(-1, "│ " + str(row["diagnostic"]))
    if stop == "eyes":
        lines.append("")
        lines.append("╔══ YOUR EYES ══════════════════════════════════")
        steps = row.get("next_steps") or []
        if not steps:
            for eid in eyes:
                lines.append(f"║ {eid}")
            lines.append("║")
            lines.append("║ Next:")
            lines.append("║   /status")
        else:
            seen: set[str] = set()
            for step in steps:
                nid = str(step.get("id") or "")
                look = str(step.get("look") or "").strip()
                cmd = str(step.get("command") or "/status")
                lines.append(f"║ {nid}")
                if look:
                    lines.append(f"║   {look}")
                if cmd not in seen:
                    seen.add(cmd)
                    lines.append("║")
                    lines.append("║ Next:")
                    lines.append(f"║   {cmd}")
        lines.append("╚═══════════════════════════════════════════════")
    unblock = [str(line) for line in (row.get("unblock") or []) if str(line).strip()]
    if unblock:
        lines.append("")
        lines.append("UNBLOCK")
        for line in unblock:
            lines.append(f"- {line}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scope", nargs="?", help="change-id to focus (e.g. add-sheaf-type)")
    p.add_argument(
        "--until",
        choices=STOPS,
        default=None,
        help="alias (roll is default). Prefer --wait / --tidy / --no-fold",
    )
    p.add_argument(
        "--wait",
        action="store_true",
        help="roll walk; stop at first ASK / PENDING / EYES",
    )
    p.add_argument(
        "--interrupt",
        action="store_true",
        help="alias for --wait",
    )
    p.add_argument(
        "--tidy",
        action="store_true",
        help="fold-legal only",
    )
    p.add_argument(
        "--only",
        choices=("fold",),
        help="alias for --tidy",
    )
    p.add_argument("--no-fold", action="store_true", dest="no_fold")
    p.add_argument("--no-beads", action="store_true", dest="no_beads")
    p.add_argument(
        "--autonomous",
        action="store_true",
        help="ignored; desk mode is --wait",
    )
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
    if args.autonomous:
        print(
            "warning: --autonomous is ignored; desk mode is --wait",
            file=sys.stderr,
        )
    until, no_fold, no_beads = resolve_until(
        args.until,
        wait=args.wait or args.interrupt,
        tidy=args.tidy or args.only == "fold",
        no_fold=args.no_fold,
        no_beads=args.no_beads,
    )
    data = load_ready(args.ready_json)
    row = decide(
        data,
        until,
        args.pause_before,
        args.scope,
        find_openspec(),
        parse_skip(args.skip),
        parse_skip(args.punt),
        no_fold=no_fold,
        no_beads=no_beads,
    )
    row = apply_eyes_stop(row, data, find_openspec())
    if args.ready_json is None and row.get("stop") and row.get("stop") != "no-ready":
        explained = load_explain()
        if explained:
            data = dict(data)
            if explained.get("blocked") is not None:
                data["blocked"] = explained.get("blocked")
            if explained.get("ready") is not None:
                data["ready_beads"] = explained.get("ready")
    row["unblock"] = human_unblock(row, data)
    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(card(row))
        print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
