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
import re
import sys
from pathlib import Path
from typing import Any

import routing

LADDER = Path(__file__).resolve().parents[1] / "references" / "ladder.json"
def apply_env(data: dict, permission: str = "write", **kwargs) -> dict:
    return {**data, "routes": [routing.resolve(r, data, permission, **kwargs) for r in data["routes"]]}


def load(path: Path | None = None, permission: str = "write", **kwargs) -> dict:
    data = json.loads((path or LADDER).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("routes"), list):
        raise SystemExit("ladder.json must have a routes array")
    return apply_env(data, permission, **kwargs)


def canonical(data, route_id):
    return data.get("migration_aliases", {}).get(route_id, route_id)


def _priority(route: dict) -> int:
    try:
        return int(route.get("priority") or 99)
    except (TypeError, ValueError):
        return 99


def candidates(
    data: dict, shape: str, allow_unavailable: bool = False,
    route_id: str | None = None, not_harness: str | None = None,
    after: str | None = None, author_family: str | None = None,
    fallback_hops: int = 0,
) -> list[dict[str, Any]]:
    explicit = bool(route_id)
    route_id, after = canonical(data, route_id), canonical(data, after)
    hits = sorted([r for r in data["routes"] if shape.strip() in (r.get("shapes") or [])],
                  key=lambda r: (_priority(r), str(r.get("id") or "")))
    if route_id:
        hits = [r for r in hits if r["id"] == route_id]
    if after:
        ids = [r["id"] for r in hits]
        hits = hits[ids.index(after) + 1:] if after in ids else []
        fallback_hops += 1
    if fallback_hops > min(2, data.get("max_fallback_hops", 2)):
        raise SystemExit("automatic fallback exhausted (maximum two hops)")
    author = author_family or not_harness
    if author and not explicit:
        try:
            vendor = routing.vendor_of(author, data)
        except ValueError as exc:
            raise SystemExit(str(exc))
        hits = [r for r in hits if r.get("vendor") != vendor]
    if not allow_unavailable:
        hits = [r for r in hits if r.get("executable", r.get("available")) and
                (explicit or r.get("health") != "degraded")]
    if explicit:
        hits = [human_warning(r) for r in hits]
    hits = [{**r, "fallback_hops": fallback_hops} for r in hits]
    return hits


def human_warning(route):
    row = dict(route)
    warnings = []
    if row.get("health") == "degraded":
        warnings.append("human pick overrides degraded infrastructure health")
    if not row.get("executable"):
        warnings.append("human pick is not executable for the requested permission")
    if warnings:
        row["warnings"] = warnings
    return row


def nicknames(route: dict) -> set[str]:
    """Shape-scoped names: exact id, interface, JSON aliases, family, x.y version."""
    out: set[str] = set()
    rid = str(route.get("id") or "").strip().lower()
    iface = str(route.get("interface") or "").strip().lower()
    if rid:
        out.add(rid)
    if iface:
        out.add(iface)
    for raw in route.get("aliases") or []:
        alias = str(raw).strip().lower()
        if alias:
            out.add(alias)
    family = route.get("family")
    if family:
        out.add(family)
        out.update(routing.registry()["families"].get(family, {}).get("aliases", []))
    for match in re.finditer(r"\d+\.\d+", f"{iface} {rid}"):
        out.add(match.group(0))
    return {n for n in out if n}


def parse_who(raw: list[str] | None) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    for item in raw or []:
        for part in str(item).split(","):
            tok = part.strip().lower()
            if tok and tok not in seen:
                seen.add(tok)
                tokens.append(tok)
    return tokens


def resolve_who(
    data: dict,
    shape: str,
    tokens: list[str],
    not_harness: str | None = None,
    allow_unavailable: bool = True,
) -> list[dict[str, Any]]:
    """Resolve nicknames/ids for a shape. Unknown or ambiguous → error. Priority order."""
    if not tokens:
        raise SystemExit("empty --who")
    rows = candidates(data, shape, allow_unavailable=True)
    for row in rows:
        row["aliases"] = [*row.get("aliases", []), *[a for a, target in data.get("migration_aliases", {}).items() if target == row["id"]]]
    if not rows:
        raise SystemExit(f"no routes for shape {shape!r}")
    matched: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for tok in tokens:
        hits = [r for r in rows if tok in nicknames(r)]
        if not hits:
            raise SystemExit(f"unknown who {tok!r} for shape {shape!r}")
        if len(hits) > 1:
            ids = ", ".join(str(r.get("id") or "?") for r in hits)
            raise SystemExit(f"ambiguous who {tok!r} for shape {shape!r}: {ids}")
        rid = str(hits[0].get("id") or "")
        if rid in seen_ids:
            continue
        seen_ids.add(rid)
        matched.append(hits[0])
    matched.sort(key=lambda r: (_priority(r), str(r.get("id") or "")))
    if not allow_unavailable:
        for route in matched:
            if route.get("available") is False:
                raise SystemExit(
                    f"unavailable who {route.get('id')!r} for shape {shape!r}"
                )
    return [human_warning(r) for r in matched]


_ADVISE_LINE = re.compile(
    r"^>\s*\*\*ADVISE:\*\*\s*(accept-with-nits|accept|send-back)\b",
    re.I,
)
_READER_LINE = re.compile(r"^>\s*\*\*READER:\*\*\s*(\S+)", re.I)
_TRAILING_SEQ = re.compile(r"^(.*)-(\d+)$")
_ACCEPTING = {"accept", "accept-with-nits"}
_HIGH_BLAST = {"high", "schema", "deletion", "protocol", "durability", "challenging"}


def _review_sort_key(path: Path) -> tuple[str, int]:
    stem = path.name[:-3] if path.name.endswith(".md") else path.name
    if stem.endswith("-sendback"):
        return (stem[: -len("-sendback")], 0)
    match = _TRAILING_SEQ.match(stem)
    if match:
        return (match.group(1), int(match.group(2)))
    return (stem, 1)


def _review_face(path: Path) -> tuple[str | None, str | None]:
    verdict = None
    reader = None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()[:40]
    except OSError:
        return None, None
    for line in lines:
        stripped = line.strip()
        advise = _ADVISE_LINE.match(stripped)
        if advise:
            verdict = advise.group(1).lower()
        named = _READER_LINE.match(stripped)
        if named:
            reader = named.group(1)
    if verdict in _ACCEPTING and not reader:
        return None, None
    return verdict, reader


def _latest_review(change_dir: Path) -> tuple[str | None, str | None]:
    reviews = change_dir / "reviews"
    if not reviews.is_dir():
        return None, None
    files = sorted(
        (p for p in reviews.iterdir() if p.is_file() and p.name.endswith(".md")),
        key=_review_sort_key,
    )
    if not files:
        return None, None
    return _review_face(files[-1])


def last_accepting_reader(openspec: Path, *, skip_change: str | None = None) -> str | None:
    """Latest accepting READER across inflight changes and the archive."""
    root = openspec / "changes"
    found: list[tuple[float, str, str]] = []
    if root.is_dir():
        for reviews in root.rglob("reviews"):
            if not reviews.is_dir():
                continue
            change_id = reviews.parent.name
            if skip_change and change_id == skip_change:
                continue
            for path in reviews.glob("*.md"):
                verdict, reader = _review_face(path)
                if verdict in _ACCEPTING and reader:
                    found.append((path.stat().st_mtime, str(path), reader))
    if not found:
        return None
    found.sort()
    return found[-1][2]


def vary_reader(
    data: dict,
    author_family: str | None = None,
    *,
    blast: str | None = None,
    last_reader: str | None = None,
    change_dir: Path | None = None,
    shape: str = "architecture-review",
) -> dict:
    """Gating architecture reader. Priority order stays the fallback list.

    High blast prefers Astra. A send-back on this change returns to that
    reader. Otherwise rotate to the next eligible reader after the last
    accept, skipping the author's vendor.
    """
    eligible = candidates(data, shape, author_family=author_family)
    if not eligible:
        raise SystemExit(f"no available route for shape {shape!r}")
    if change_dir is not None:
        verdict, reader = _latest_review(change_dir)
        if verdict == "send-back" and reader:
            same = next((route for route in eligible if route["id"] == reader), None)
            if same is not None:
                return {**same, "vary_reason": "send-back", "last_reader": last_reader}
    high = (blast or "").strip().lower() in _HIGH_BLAST
    if high:
        astra = next((route for route in eligible if route.get("family") == "astra"), None)
        chosen = astra or eligible[0]
        reason = "high-blast" if astra else "high-blast-author-skipped"
    else:
        ids = [route["id"] for route in eligible]
        if last_reader in ids and len(ids) > 1:
            chosen = eligible[(ids.index(last_reader) + 1) % len(ids)]
            reason = "rotate"
        else:
            chosen = eligible[0]
            reason = "first"
    return {**chosen, "vary_reason": reason, "last_reader": last_reader}


def assign(
    data: dict,
    shape: str,
    allow_unavailable: bool = False,
    route_id: str | None = None,
    not_harness: str | None = None,
    after: str | None = None,
    author_family: str | None = None,
    fallback_hops: int = 0,
) -> dict:
    hits = candidates(
        data,
        shape,
        allow_unavailable=allow_unavailable,
        route_id=route_id,
        not_harness=not_harness,
        after=after,
        author_family=author_family,
        fallback_hops=fallback_hops,
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
    a.add_argument("--who", action="append", help="nickname or id; comma list or repeatable")
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

    vary = sub.add_parser(
        "vary-reader",
        help="gating architecture reader: Astra on high blast, else rotate",
    )
    vary.add_argument("--shape", default="architecture-review")
    vary.add_argument("--blast", default="", help="high, schema, deletion, protocol, or durability")
    vary.add_argument("--last-reader", help="route id of the previous accepting reader")
    vary.add_argument("--openspec", type=Path, help="scan changes and archive for the last accept")
    vary.add_argument("--change-dir", type=Path, help="this change; a send-back returns to that reader")
    vary.set_defaults(cmd="vary-reader")

    for parser in (a, pan, vary):
        parser.add_argument("--permission", choices=["read", "write", "sensitive"], default="write")
        parser.add_argument("--author-family", help="deterministic author harness/family/vendor; automatic review skips it")
        parser.add_argument("--fallback-hops", type=int, default=0, help="completed hops; carried across handoffs")
    args = p.parse_args()
    data = load(args.file, getattr(args, "permission", "write"))
    if args.cmd == "show":
        print(json.dumps(data, indent=2))
        return 0
    if args.cmd == "panel":
        hits = candidates(data, args.shape, not_harness=getattr(args, "not_harness", None), author_family=args.author_family)
        print(json.dumps(hits, indent=2))
        return 0
    if args.cmd == "vary-reader":
        last = getattr(args, "last_reader", None)
        openspec = getattr(args, "openspec", None)
        if last is None and openspec is not None:
            skip = None
            change_dir = getattr(args, "change_dir", None)
            if change_dir is not None:
                skip = change_dir.name
            last = last_accepting_reader(openspec, skip_change=skip)
        try:
            route = vary_reader(
                data,
                args.author_family,
                blast=getattr(args, "blast", None),
                last_reader=last,
                change_dir=getattr(args, "change_dir", None),
                shape=args.shape,
            )
        except SystemExit as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps(route, indent=2))
        return 0
    who = parse_who(getattr(args, "who", None))
    if who and (getattr(args, "route_id", None) or getattr(args, "after", None)):
        print("--who does not combine with --id or --after", file=sys.stderr)
        return 2
    if who:
        try:
            hits = resolve_who(
                data,
                args.shape,
                who,
                not_harness=getattr(args, "not_harness", None),
                allow_unavailable=getattr(args, "include_unavailable", False),
            )
        except SystemExit as exc:
            print(str(exc), file=sys.stderr)
            return 2
        if not getattr(args, "all", False) and len(hits) == 1:
            print(json.dumps(hits[0], indent=2))
        else:
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
            author_family=args.author_family,
            fallback_hops=args.fallback_hops,
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
        author_family=args.author_family,
        fallback_hops=args.fallback_hops,
    )
    print(json.dumps(route, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
