#!/usr/bin/env python3
"""G1 — process hygiene. Properties, not path names.

Properties (a green that still lets the repo lie is a failed check):

1. Disposition lives in the file. Every in-flight proposal.md has a
   banner PENDING | ACTIVE BUILD | PARKED. Directory name is not status.
2. Fold-debt is empty. An ACTIVE BUILD change with no *open owed*
   checkbox (all [x], missing tasks.md, or prose-only tasks) must have
   been archived. PENDING fails only if owed boxes exist and are all [x].
   Empty allowlist.
3. Journey or no-new-UI. PENDING and ACTIVE BUILD proposals contain
   "## User journey & surfaces" or "No new UI because".
4. Checkboxes are owed work. A box whose text or heading is out-of-scope /
   handoff / not-in-this-change fails, checked or not.

How to fake these (and why the check still bites):
- Banner on line 1 of a file that is not proposal.md → ignored; we only
  read proposal.md.
- Banner after a long preamble with no quote-banner → fail (we require a
  banner in the first 40 lines).
- Leave one eternal "[ ] verify in prod someday" to dodge fold-debt →
  fail if the text looks like a non-owed stall (see STALL_RE).
- Journey heading with empty body → we require the heading *or* the
  no-new-UI sentence; empty heading still matches. G1 does not grade
  journey quality (that is a human). A heading-only dodge is a known
  hole; do not "fix" it with a word-count gate.

Usage:
  python3 scripts/check-hygiene.py
  python3 scripts/check-hygiene.py --root path/to/openspec
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNER_RE = re.compile(
    r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b",
    re.M,
)
JOURNEY_HEADING_RE = re.compile(
    r"^##\s+User journey\b",
    re.M | re.I,
)
NO_NEW_UI_RE = re.compile(r"No new UI because\b", re.I)
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")
SCOPE_HEADING_RE = re.compile(
    r"^#+\s+(out[ -]of[ -]scope|not in this change|deliberately not|handoffs?|findings|deferred)\b",
    re.I,
)
SCOPE_ITEM_RE = re.compile(
    r"(not in this change|out of scope|handoff|deliberately not)",
    re.I,
)
STALL_RE = re.compile(
    r"\b(someday|eventually|nice to have|follow-?up later|optional later)\b",
    re.I,
)
# Empty on purpose. Adding a name is a visible, argued edit.
FOLD_DEBT_ALLOWLIST: set[str] = set()


def iter_inflight(openspec: Path) -> list[Path]:
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    out: list[Path] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        out.append(child)
    return out


def first_banner(text: str) -> str | None:
    for i, line in enumerate(text.splitlines()):
        if i >= 40:
            break
        m = BANNER_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def checkboxes(tasks: str) -> list[tuple[str, bool, str]]:
    """Return (heading, checked, text) for each box."""
    heading = ""
    rows: list[tuple[str, bool, str]] = []
    for line in tasks.splitlines():
        if re.match(r"^#+\s+", line):
            heading = line
        m = CHECKBOX_RE.match(line)
        if m:
            rows.append((heading, m.group(2).lower() == "x", m.group(3).strip()))
    return rows


def check_change(path: Path) -> list[str]:
    errors: list[str] = []
    name = path.name
    proposal = path / "proposal.md"
    if not proposal.is_file():
        errors.append(f"{name}: missing proposal.md")
        return errors
    text = proposal.read_text(encoding="utf-8")
    banner = first_banner(text)
    if banner is None:
        errors.append(f"{name}: proposal.md has no PENDING|ACTIVE BUILD|PARKED banner in the first 40 lines")
        return errors

    if banner in {"PENDING", "ACTIVE BUILD"}:
        if not (JOURNEY_HEADING_RE.search(text) or NO_NEW_UI_RE.search(text)):
            errors.append(
                f"{name}: {banner} proposal needs '## User journey' or 'No new UI because'"
            )

    tasks_path = path / "tasks.md"
    rows: list[tuple[str, bool, str]] = []
    if tasks_path.is_file():
        rows = checkboxes(tasks_path.read_text(encoding="utf-8"))
        for heading, _checked, item in rows:
            if SCOPE_HEADING_RE.match(heading) or SCOPE_ITEM_RE.search(item):
                errors.append(
                    f"{name}: checkbox is not owed work ({item!r} under {heading!r})"
                )
            if STALL_RE.search(item):
                errors.append(f"{name}: stall checkbox {item!r} (use a PARKED revive, not a box)")

    owed = [
        (h, c, t)
        for h, c, t in rows
        if not SCOPE_HEADING_RE.match(h) and not SCOPE_ITEM_RE.search(t)
    ]
    open_owed = [r for r in owed if not r[1]]
    if name not in FOLD_DEBT_ALLOWLIST:
        if banner == "ACTIVE BUILD" and not open_owed:
            errors.append(
                f"{name}: fold-debt — ACTIVE BUILD with no open owed checkbox "
                "(missing tasks, prose-only, or all [x]) still in changes/"
            )
        elif banner == "PENDING" and owed and not open_owed:
            errors.append(
                f"{name}: fold-debt — all owed checkboxes are [x] but the change is still in changes/"
            )
    return errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=None, help="openspec/ directory")
    args = p.parse_args()
    repo = Path(__file__).resolve().parents[1]
    openspec = args.root.resolve() if args.root else (repo / "openspec")
    if not openspec.is_dir():
        print(f"no openspec at {openspec}")
        return 1

    errors: list[str] = []
    for change in iter_inflight(openspec):
        errors.extend(check_change(change))

    if errors:
        for e in errors:
            print(e)
        print(f"FAIL {len(errors)}")
        return 1
    n = len(iter_inflight(openspec))
    print(f"pass {n} in-flight change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
