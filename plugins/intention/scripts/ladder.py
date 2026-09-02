#!/usr/bin/env python3
"""Resolve the assignment ladder. Human pick always wins.

  python3 plugins/intention/scripts/ladder.py assign --shape known
  python3 plugins/intention/scripts/ladder.py assign --shape known --all
  python3 plugins/intention/scripts/ladder.py assign --shape known --after terra-known
  python3 plugins/intention/scripts/ladder.py panel --shape architecture-review
  python3 plugins/intention/scripts/ladder.py show
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

LADDER = Path(__file__).resolve().parents[1] / "references" / "ladder.json"
OPENAI_KEY_VARS = ("OPENAI_API_KEY",)


def openai_api_key() -> str | None:
    for name in OPENAI_KEY_VARS:
        val = (os.environ.get(name) or "").strip()
        if val:
            return val
    return None


def codex_cli_present() -> bool:
    binary = os.environ.get("CODEX_BIN", "codex")
    return shutil.which(binary) is not None


def requirement_met(req: str | None) -> bool:
    if not req:
        return True
    if req == "codex-cli":
        return codex_cli_present()
    if req == "openai-key":
        return bool(openai_api_key())
    if req == "codex":
        return codex_cli_present() or bool(openai_api_key())
    return False


def apply_env(data: dict) -> dict:
    routes = []
    for route in data.get("routes") or []:
        if not isinstance(route, dict):
            continue
        row = dict(route)
        req = row.get("requires")
        if req:
            row["available"] = bool(requirement_met(str(req)))
        routes.append(row)
    out = dict(data)
    out["routes"] = routes
    return out


def load(path: Path | None = None) -> dict:
    data = json.loads((path or LADDER).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        raise SystemExit("ladder.json must have a routes array")
    return apply_env(data)


def _priority(route: dict) -> int:
    try:
        return int(route.get("priority") or 99)
    except (TypeError, ValueError):
        return 99


def candidates(
    data: dict,
    shape: str,
    allow_unavailable: bool = False,
    route_id: str | None = None,
    not_harness: str | None = None,
    after: str | None = None,
) -> list[dict[str, Any]]:
    shape = shape.strip()
    skip_harness = (not_harness or "").strip()
    hits: list[dict[str, Any]] = []
    for route in data["routes"]:
        if not isinstance(route, dict):
            continue
        shapes = route.get("shapes") or []
        if shape not in shapes:
            continue
        if route_id and route.get("id") != route_id:
            continue
        hits.append(route)
    hits.sort(key=lambda r: (_priority(r), str(r.get("id") or "")))
    if after:
        ids = [str(r.get("id") or "") for r in hits]
        if after in ids:
            hits = hits[ids.index(after) + 1 :]
        else:
            hits = []
    if skip_harness:
        hits = [r for r in hits if str(r.get("harness") or "") != skip_harness]
    if not allow_unavailable:
        hits = [r for r in hits if r.get("available") is not False]
    return hits


def assign(
    data: dict,
    shape: str,
    allow_unavailable: bool = False,
    route_id: str | None = None,
    not_harness: str | None = None,
    after: str | None = None,
) -> dict:
    hits = candidates(
        data,
        shape,
        allow_unavailable=allow_unavailable,
        route_id=route_id,
        not_harness=not_harness,
        after=after,
    )
    if not hits:
        want = f"shape {shape!r}"
        if route_id:
            want += f" id {route_id!r}"
        if after:
            want += f" after {after!r}"
        raise SystemExit(f"no available route for {want}")
    return hits[0]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", type=Path)
    sub = p.add_subparsers(dest="cmd", required=True)

    show = sub.add_parser("show", help="print the ladder")
    show.set_defaults(cmd="show")

    a = sub.add_parser("assign", help="resolve one shape (first available by priority)")
    a.add_argument("--shape", required=True)
    a.add_argument("--id", dest="route_id", help="pick this route id")
    a.add_argument("--after", help="handoff: next available route after this id")
    a.add_argument("--all", action="store_true", help="print every available route in priority order")
    a.add_argument(
        "--not-harness",
        dest="not_harness",
        help="skip routes whose harness matches (ADR-005 other-family)",
    )
    a.add_argument("--include-unavailable", action="store_true")
    a.set_defaults(cmd="assign")

    pan = sub.add_parser("panel", help="available routes for a shape, priority order (fan-out)")
    pan.add_argument("--shape", required=True)
    pan.add_argument("--not-harness", dest="not_harness")
    pan.set_defaults(cmd="panel")

    args = p.parse_args()
    data = load(args.file)
    if args.cmd == "show":
        print(json.dumps(data, indent=2))
        return 0
    if args.cmd == "panel":
        hits = candidates(data, args.shape, not_harness=getattr(args, "not_harness", None))
        print(json.dumps(hits, indent=2))
        return 0
    if getattr(args, "all", False):
        hits = candidates(
            data,
            args.shape,
            allow_unavailable=args.include_unavailable,
            route_id=getattr(args, "route_id", None),
            not_harness=getattr(args, "not_harness", None),
            after=getattr(args, "after", None),
        )
        print(json.dumps(hits, indent=2))
        return 0
    route = assign(
        data,
        args.shape,
        allow_unavailable=args.include_unavailable,
        route_id=getattr(args, "route_id", None),
        not_harness=getattr(args, "not_harness", None),
        after=getattr(args, "after", None),
    )
    print(json.dumps(route, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
