#!/usr/bin/env python3
"""Conductor scheduler for `act`.

Ready-set = inbound deps closed AND write-set disjoint from in-flight.
Isolation MAY be a worktree; this process persists. Workers edit.

  python3 plugins/intention/scripts/conductor.py ready [--inventory FILE]
  python3 plugins/intention/scripts/conductor.py take --node ID [--inventory FILE]
  python3 plugins/intention/scripts/conductor.py release --node ID [--inventory FILE]
  python3 plugins/intention/scripts/conductor.py lint-packet FILE
  python3 plugins/intention/scripts/conductor.py isolate --node ID
  python3 plugins/intention/scripts/conductor.py persist --paths P [P ...] -m MSG
  python3 plugins/intention/scripts/conductor.py classify FILE
  python3 plugins/intention/scripts/conductor.py implicated --node ID [--inventory FILE]
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

LADDER_PATH = Path(__file__).resolve().parents[1] / "references" / "ladder.json"

CLOSED = {"closed", "done"}
IN_FLIGHT = {"in_progress"}
PARKED = {"parked", "deferred"}
BLOCKED = {"blocked"}
OPEN = {"open"}

COMMIT_EXEMPT = re.compile(
    r"\b(do not commit|don't commit|do not run git|run no git|conductor commits)\b",
    re.I,
)
DO_NOT_FORBIDDEN = {"commit", "git", "persist"}


def norm_path(p: str) -> str:
    p = p.strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return posixpath.normpath(p).lstrip("/")


def paths_overlap(a: Iterable[str], b: Iterable[str]) -> list[str]:
    hits: list[str] = []
    left = [norm_path(x) for x in a if x]
    right = [norm_path(x) for x in b if x]
    for x in left:
        for y in right:
            if x == y or x.startswith(y + "/") or y.startswith(x + "/"):
                pair = f"{x}∩{y}"
                if pair not in hits:
                    hits.append(pair)
    return hits


def _deps(node: dict) -> list[str]:
    raw = node.get("deps") or []
    return [str(d) for d in raw]


def _status(node: dict) -> str:
    return str(node.get("status") or "open")


def _paths(node: dict) -> list[str]:
    return [str(p) for p in (node.get("paths") or []) if p]


def index_nodes(nodes: list[dict]) -> dict[str, dict]:
    return {str(n["id"]): n for n in nodes if n.get("id")}


def ready_ids(nodes: list[dict]) -> tuple[list[str], list[str]]:
    by_id = index_nodes(nodes)
    ready: list[str] = []
    blocked: list[str] = []
    for nid, node in by_id.items():
        st = _status(node)
        if st in CLOSED | PARKED | IN_FLIGHT:
            continue
        if st in BLOCKED:
            blocked.append(nid)
            continue
        missing = []
        for dep in _deps(node):
            other = by_id.get(dep)
            if other is None or _status(other) not in CLOSED:
                missing.append(dep)
        if missing:
            blocked.append(nid)
        elif st in OPEN:
            ready.append(nid)
    return ready, blocked


def resolve_max_inflight(cli: int | None = None, ladder: Path | None = None) -> int:
    if cli is not None:
        return max(0, int(cli))
    env = os.environ.get("ACT_MAX_INFLIGHT")
    if env:
        return max(0, int(env))
    path = ladder or LADDER_PATH
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        if isinstance(data, dict) and data.get("max_inflight") is not None:
            return max(0, int(data["max_inflight"]))
    return 2


def dispatch(nodes: list[dict], max_inflight: int | None = None) -> dict[str, Any]:
    by_id = index_nodes(nodes)
    ready, blocked = ready_ids(nodes)
    flying_paths: list[str] = []
    in_flight_ids: list[str] = []
    parked: list[dict] = []
    for nid, node in by_id.items():
        st = _status(node)
        if st in IN_FLIGHT:
            in_flight_ids.append(nid)
            flying_paths.extend(_paths(node))
        elif st in PARKED:
            parked.append({"id": nid, "reason": st})

    cap = resolve_max_inflight(max_inflight)
    free = max(0, cap - len(in_flight_ids))
    remaining = free
    dispatchable: list[dict] = []
    deferred: list[dict] = []
    capped: list[dict] = []
    for nid in ready:
        hits = paths_overlap(_paths(by_id[nid]), flying_paths)
        row = {"id": nid, "paths": _paths(by_id[nid])}
        if hits:
            row["reason"] = "paths overlap in-flight: " + ", ".join(hits)
            deferred.append(row)
        elif remaining <= 0:
            row["reason"] = f"max_inflight {cap} reached"
            capped.append(row)
        else:
            dispatchable.append(row)
            remaining -= 1

    return {
        "dispatchable": dispatchable,
        "deferred": deferred,
        "capped": capped,
        "blocked": [{"id": i} for i in blocked],
        "in_flight": [{"id": i, "holder": by_id[i].get("holder")} for i in in_flight_ids],
        "parked": parked,
        "slots": {"max": cap, "in_flight": len(in_flight_ids), "free": free},
    }


def implicated(nodes: list[dict], failed: str) -> list[str]:
    by_id = index_nodes(nodes)
    if failed not in by_id:
        return []
    kids: dict[str, list[str]] = {i: [] for i in by_id}
    for nid, node in by_id.items():
        for dep in _deps(node):
            kids.setdefault(dep, []).append(nid)
    out: list[str] = []
    stack = [failed]
    seen: set[str] = set()
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        if _status(by_id[cur]) not in CLOSED:
            out.append(cur)
        stack.extend(kids.get(cur, []))
    return out


def lint_packet(data: dict) -> list[str]:
    errors: list[str] = []
    constraints = data.get("constraints") if isinstance(data.get("constraints"), dict) else {}
    do_not = constraints.get("do_not") if isinstance(constraints.get("do_not"), list) else []
    for item in do_not:
        token = str(item).strip().lower()
        if token in DO_NOT_FORBIDDEN or token.startswith("git "):
            errors.append(f"constraints.do_not contains commit exemption: {item!r}")
    blob = json.dumps(data, ensure_ascii=False)
    if COMMIT_EXEMPT.search(blob):
        errors.append("packet text contains a commit exemption")
    return errors


def classify(face: dict) -> dict[str, str]:
    disp = str(face.get("disposition") or "")
    if disp == "pass":
        return {"action": "close", "disposition": disp}
    if disp == "baseline-red":
        return {"action": "complete", "disposition": disp}
    if disp == "task-red":
        return {"action": "repair", "disposition": disp}
    if disp == "infra-red":
        return {"action": "retry", "disposition": disp}
    if disp in {"blocked", "parked"}:
        return {"action": "park", "disposition": disp}
    return {"action": "park", "disposition": disp or "blocked"}


def load_inventory(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        nodes = data.get("nodes")
    else:
        nodes = data
    if not isinstance(nodes, list):
        raise SystemExit("inventory must be a list or {nodes: [...]}")
    return [n for n in nodes if isinstance(n, dict)]


def load_packet_paths(repo: Path, node_id: str) -> list[str]:
    packet = repo / "groups" / node_id / "packet.json"
    if not packet.is_file():
        return []
    try:
        data = json.loads(packet.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    constraints = data.get("constraints") if isinstance(data.get("constraints"), dict) else {}
    paths = constraints.get("paths") if isinstance(constraints.get("paths"), list) else []
    return [str(p) for p in paths if p]


def beads_to_nodes(issues: list[dict], repo: Path) -> list[dict]:
    nodes: list[dict] = []
    for issue in issues:
        nid = str(issue.get("id") or "")
        if not nid:
            continue
        deps: list[str] = []
        for edge in issue.get("dependencies") or []:
            if not isinstance(edge, dict):
                continue
            if edge.get("type") in {None, "blocks"} and edge.get("depends_on_id"):
                if edge.get("issue_id", nid) == nid:
                    deps.append(str(edge["depends_on_id"]))
        nodes.append(
            {
                "id": nid,
                "status": str(issue.get("status") or "open"),
                "deps": deps,
                "paths": load_packet_paths(repo, nid),
                "holder": issue.get("assignee") or issue.get("owner"),
            }
        )
    return nodes


def run_bd_json(args: list[str]) -> list[dict]:
    try:
        out = subprocess.check_output(["bd", *args, "--json"], text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"bd failed: {exc}") from exc
    data = json.loads(out)
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict) and isinstance(data.get("issues"), list):
        return [x for x in data["issues"] if isinstance(x, dict)]
    return []


def git(repo: Path, extra: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *extra],
        check=check,
        text=True,
        capture_output=True,
    )


def safe_node(node_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", node_id).strip("-")
    return cleaned or "node"


def write_inventory(path: Path, nodes: list[dict]) -> None:
    path.write_text(json.dumps({"nodes": nodes}, indent=2) + "\n", encoding="utf-8")


def lease_path(repo: Path, node_id: str) -> Path:
    return repo / ".spawns" / "leases" / f"{safe_node(node_id)}.json"


def write_lease(repo: Path, node: dict, holder: str) -> Path:
    dest = lease_path(repo, str(node["id"]))
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "node_id": node["id"],
        "holder": holder,
        "paths": _paths(node),
        "taken_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "held",
    }
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return dest


def take_node(nodes: list[dict], node_id: str, holder: str, max_inflight: int | None = None) -> dict:
    state = dispatch(nodes, max_inflight=max_inflight)
    by_id = index_nodes(nodes)
    node = by_id.get(node_id)
    if node is None:
        raise SystemExit(f"unknown node {node_id}")
    if _status(node) in IN_FLIGHT:
        raise SystemExit(f"already taken: {node_id} holder={node.get('holder')}")
    if node_id not in {r["id"] for r in state["dispatchable"]}:
        raise SystemExit(f"not dispatchable: {node_id}")
    node["status"] = "in_progress"
    node["holder"] = holder
    return node


def release_node(nodes: list[dict], node_id: str) -> dict:
    by_id = index_nodes(nodes)
    node = by_id.get(node_id)
    if node is None:
        raise SystemExit(f"unknown node {node_id}")
    node["status"] = "open"
    node["holder"] = None
    return node


def cmd_ready(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    if args.inventory:
        nodes = load_inventory(args.inventory)
    else:
        nodes = beads_to_nodes(run_bd_json(["list", "--all", "-n", "0"]), repo)
    result = dispatch(nodes, max_inflight=args.max_inflight)
    print(json.dumps(result, indent=2))
    return 0


def cmd_take(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    holder = args.holder or os.environ.get("ACT_HOLDER") or "conductor"
    if args.inventory:
        nodes = load_inventory(args.inventory)
        node = take_node(nodes, args.node, holder, max_inflight=args.max_inflight)
        write_inventory(args.inventory, nodes)
    else:
        nodes = beads_to_nodes(run_bd_json(["list", "--all", "-n", "0"]), repo)
        node = take_node(nodes, args.node, holder, max_inflight=args.max_inflight)
        try:
            subprocess.check_call(
                [
                    "bd",
                    "update",
                    args.node,
                    "--claim",
                    "-a",
                    holder,
                    "-s",
                    "in_progress",
                ]
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise SystemExit(f"bd claim failed: {exc}") from exc
    lease = write_lease(repo, node, holder)
    print(json.dumps({"taken": node["id"], "holder": holder, "paths": _paths(node), "lease": str(lease)}, indent=2))
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    if args.inventory:
        nodes = load_inventory(args.inventory)
        release_node(nodes, args.node)
        write_inventory(args.inventory, nodes)
    else:
        try:
            subprocess.check_call(["bd", "update", args.node, "-s", "open", "-a", ""])
        except (OSError, subprocess.CalledProcessError) as exc:
            raise SystemExit(f"bd release failed: {exc}") from exc
    lease = lease_path(repo, args.node)
    if lease.is_file():
        data = json.loads(lease.read_text(encoding="utf-8"))
        data["status"] = "released"
        lease.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"released": args.node}, indent=2))
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    data = json.loads(args.packet.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("packet is not a JSON object", file=sys.stderr)
        return 1
    errors = lint_packet(data)
    if errors:
        for e in errors:
            print(e)
        return 1
    print("ok")
    return 0


def cmd_isolate(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    node = safe_node(args.node)
    dest = repo / ".worktrees" / node
    branch = f"act/{node}"
    if dest.is_dir():
        print(json.dumps({"worktree": str(dest), "branch": branch, "reused": True}))
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    existing = git(repo, ["rev-parse", "--verify", branch], check=False)
    if existing.returncode == 0:
        proc = git(repo, ["worktree", "add", str(dest), branch], check=False)
    else:
        proc = git(repo, ["worktree", "add", "-b", branch, str(dest)], check=False)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        return proc.returncode
    print(json.dumps({"worktree": str(dest), "branch": branch, "reused": False}))
    return 0


def cmd_persist(args: argparse.Namespace) -> int:
    tree = (args.worktree or args.repo).resolve()
    paths = [norm_path(p) for p in args.paths]
    if not paths:
        print("persist requires --paths", file=sys.stderr)
        return 2
    if any(p in {".", ""} or p.startswith("..") for p in paths):
        print("refuse broad or escaping paths", file=sys.stderr)
        return 2
    add = git(tree, ["add", "--", *paths], check=False)
    if add.returncode != 0:
        sys.stderr.write(add.stderr)
        return add.returncode
    commit = git(
        tree,
        ["commit", "--only", "-m", args.message, "--", *paths],
        check=False,
    )
    if commit.returncode != 0:
        err = (commit.stderr or commit.stdout).strip()
        print(err or "persist failed", file=sys.stderr)
        return 2 if "nothing to commit" in err.lower() or "no changes" in err.lower() else commit.returncode
    sha = git(tree, ["rev-parse", "--short", "HEAD"]).stdout.strip()
    print(json.dumps({"sha": sha, "paths": paths, "worktree": str(tree)}))
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    data = json.loads(args.face.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print("face is not a JSON object", file=sys.stderr)
        return 1
    face = data.get("distilled") if isinstance(data.get("distilled"), dict) else data
    print(json.dumps(classify(face), indent=2))
    return 0


def cmd_implicated(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    if args.inventory:
        nodes = load_inventory(args.inventory)
    else:
        nodes = beads_to_nodes(run_bd_json(["list", "--all", "-n", "0"]), repo)
    print(json.dumps({"node": args.node, "implicated": implicated(nodes, args.node)}, indent=2))
    return 0


def main() -> int:
    repo_default = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=repo_default)
    sub = p.add_subparsers(dest="cmd", required=True)

    ready = sub.add_parser("ready", help="dispatchable ready-set")
    ready.add_argument("--inventory", type=Path)
    ready.add_argument("--max-inflight", type=int)
    ready.set_defaults(func=cmd_ready)

    take = sub.add_parser("take", help="mutex: mark node in_progress")
    take.add_argument("--node", required=True)
    take.add_argument("--holder")
    take.add_argument("--inventory", type=Path)
    take.add_argument("--max-inflight", type=int)
    take.set_defaults(func=cmd_take)

    rel = sub.add_parser("release", help="drop the node mutex")
    rel.add_argument("--node", required=True)
    rel.add_argument("--inventory", type=Path)
    rel.set_defaults(func=cmd_release)

    lint = sub.add_parser("lint-packet", help="reject commit exemptions")
    lint.add_argument("packet", type=Path)
    lint.set_defaults(func=cmd_lint)

    iso = sub.add_parser("isolate", help="create or reuse a worktree")
    iso.add_argument("--node", required=True)
    iso.set_defaults(func=cmd_isolate)

    persist = sub.add_parser("persist", help="conductor commit of exact paths")
    persist.add_argument("--paths", nargs="+", required=True)
    persist.add_argument("-m", "--message", required=True)
    persist.add_argument("--worktree", type=Path)
    persist.set_defaults(func=cmd_persist)

    cls = sub.add_parser("classify", help="action from a distilled face")
    cls.add_argument("face", type=Path)
    cls.set_defaults(func=cmd_classify)

    imp = sub.add_parser("implicated", help="failed node plus dependents")
    imp.add_argument("--node", required=True)
    imp.add_argument("--inventory", type=Path)
    imp.set_defaults(func=cmd_implicated)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
