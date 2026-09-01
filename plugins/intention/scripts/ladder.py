#!/usr/bin/env python3
"""Resolve the assignment ladder. Human pick always wins.

  python3 plugins/intention/scripts/ladder.py assign --shape known
  python3 plugins/intention/scripts/ladder.py assign --shape architecture-review
  python3 plugins/intention/scripts/ladder.py assign --shape fold
  python3 plugins/intention/scripts/ladder.py show
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

LADDER = Path(__file__).resolve().parents[1] / "references" / "ladder.json"
OPENAI_KEY_VARS = ("OPENAI_API", "OPENAI_API_KEY")


def openai_api_key() -> str | None:
    for name in OPENAI_KEY_VARS:
        val = (os.environ.get(name) or "").strip()
        if val:
            return val
    return None


def apply_env(data: dict) -> dict:
    """Sol is available when OPENAI_API or OPENAI_API_KEY is set."""
    routes = []
    for route in data.get("routes") or []:
        if not isinstance(route, dict):
            continue
        row = dict(route)
        if row.get("id") == "sol-arch-review":
            if openai_api_key():
                row["available"] = True
                row["notes"] = (
                    "Second-family reader via OpenAI API "
                    "(OPENAI_API or OPENAI_API_KEY). Packet-only; spawn --adapter openai."
                )
            else:
                row["available"] = False
        routes.append(row)
    out = dict(data)
    out["routes"] = routes
    return out


def load(path: Path | None = None) -> dict:
    data = json.loads((path or LADDER).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        raise SystemExit("ladder.json must have a routes array")
    return apply_env(data)


def assign(
    data: dict,
    shape: str,
    allow_unavailable: bool = False,
    route_id: str | None = None,
) -> dict:
    shape = shape.strip()
    hits = []
    for route in data["routes"]:
        if not isinstance(route, dict):
            continue
        shapes = route.get("shapes") or []
        if shape not in shapes:
            continue
        if route_id and route.get("id") != route_id:
            continue
        if route.get("available") is False and not allow_unavailable:
            continue
        hits.append(route)
    if not hits:
        want = f"shape {shape!r}" + (f" id {route_id!r}" if route_id else "")
        raise SystemExit(f"no available route for {want}")
    return hits[0]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", type=Path)
    sub = p.add_subparsers(dest="cmd", required=True)

    show = sub.add_parser("show", help="print the ladder")
    show.set_defaults(cmd="show")

    a = sub.add_parser("assign", help="resolve one shape")
    a.add_argument("--shape", required=True)
    a.add_argument("--id", dest="route_id", help="pick this route id (e.g. sol-arch-review)")
    a.add_argument("--include-unavailable", action="store_true")
    a.set_defaults(cmd="assign")

    args = p.parse_args()
    data = load(args.file)
    if args.cmd == "show":
        print(json.dumps(data, indent=2))
        return 0
    route = assign(
        data,
        args.shape,
        allow_unavailable=args.include_unavailable,
        route_id=getattr(args, "route_id", None),
    )
    print(json.dumps(route, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())
