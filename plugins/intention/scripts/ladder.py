#!/usr/bin/env python3
"""Resolve the assignment ladder. Human pick always wins.

  python3 plugins/intention/scripts/ladder.py assign --shape known
  python3 plugins/intention/scripts/ladder.py assign --shape architecture-review
  python3 plugins/intention/scripts/ladder.py show
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LADDER = Path(__file__).resolve().parents[1] / "references" / "ladder.json"


def load(path: Path | None = None) -> dict:
    data = json.loads((path or LADDER).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        raise SystemExit("ladder.json must have a routes array")
    return data


def assign(data: dict, shape: str, allow_unavailable: bool = False) -> dict:
    shape = shape.strip()
    hits = []
    for route in data["routes"]:
        if not isinstance(route, dict):
            continue
        shapes = route.get("shapes") or []
        if shape not in shapes:
            continue
        if route.get("available") is False and not allow_unavailable:
            continue
        hits.append(route)
    if not hits:
        raise SystemExit(f"no available route for shape {shape!r}")
    return hits[0]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file", type=Path)
    sub = p.add_subparsers(dest="cmd", required=True)

    show = sub.add_parser("show", help="print the ladder")
    show.set_defaults(cmd="show")

    a = sub.add_parser("assign", help="resolve one shape")
    a.add_argument("--shape", required=True)
    a.add_argument("--include-unavailable", action="store_true")
    a.set_defaults(cmd="assign")

    args = p.parse_args()
    data = load(args.file)
    if args.cmd == "show":
        print(json.dumps(data, indent=2))
        return 0
    route = assign(data, args.shape, allow_unavailable=args.include_unavailable)
    print(json.dumps(route, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
