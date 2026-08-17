#!/usr/bin/env python3
"""Project beads into the Taskmaster snapshot contract.

Contract: archive/2026-08-16-add-taskmaster-edge-source/design.md
Output the app vendors: docs/taskmaster/graph.json

  python3 scripts/export-graph.py
  python3 scripts/export-graph.py --inventory FILE -o OUT.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OMIT = {"deferred", "parked"}
CLOSED = {"closed", "done"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def needs_of(issue: dict, nid: str) -> list[str]:
    out: list[str] = []
    for edge in issue.get("dependencies") or []:
        if not isinstance(edge, dict):
            continue
        if edge.get("type") != "blocks":
            continue
        dep = edge.get("depends_on_id")
        if dep and edge.get("issue_id", nid) == nid:
            out.append(str(dep))
    return out


def kind_of(issue: dict) -> str:
    raw = str(issue.get("issue_type") or "task")
    return "intention" if raw == "epic" else "node"


def project(issues: list[dict], generated_at: str, source: str = "bazaar") -> dict[str, Any]:
    kept: list[dict] = []
    for issue in issues:
        nid = str(issue.get("id") or "")
        if not nid:
            continue
        status = str(issue.get("status") or "open")
        if status in OMIT:
            continue
        state = "landed" if status in CLOSED else "open"
        kept.append(
            {
                "id": nid,
                "title": str(issue.get("title") or nid),
                "kind": kind_of(issue),
                "state": state,
                "needs": needs_of(issue, nid),
            }
        )
    ids = {n["id"] for n in kept}
    for node in kept:
        node["needs"] = [i for i in node["needs"] if i in ids]
    doc = {"generated_at": generated_at, "source": source, "nodes": kept}
    assert "ready" not in doc
    for node in kept:
        assert "ready" not in node
    return doc


def load_inventory(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        nodes = data.get("nodes") or data.get("issues")
    else:
        nodes = data
    if not isinstance(nodes, list):
        raise SystemExit("inventory must be a list or {nodes|issues: [...]}")
    return [n for n in nodes if isinstance(n, dict)]


def load_beads() -> list[dict]:
    try:
        out = subprocess.check_output(
            ["bd", "list", "--all", "-n", "0", "--json"],
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"bd list failed: {exc}") from exc
    data = json.loads(out)
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return []


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory", type=Path)
    p.add_argument("-o", "--output", type=Path, default=root / "docs" / "taskmaster" / "graph.json")
    p.add_argument("--source", default="bazaar")
    p.add_argument("--generated-at")
    args = p.parse_args()
    issues = load_inventory(args.inventory) if args.inventory else load_beads()
    doc = project(issues, args.generated_at or utc_now(), source=args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(args.output), "nodes": len(doc["nodes"]), "generated_at": doc["generated_at"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
