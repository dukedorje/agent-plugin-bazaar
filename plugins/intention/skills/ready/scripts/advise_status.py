"""Parse whether an OpenSpec change still needs advise.

Canonical copy — travels with the ready skill. Conductor imports via
plugins/intention/scripts/advise_status.py (loader).
"""

from __future__ import annotations

import re
from pathlib import Path

ADVISE_RE = re.compile(
    r"^>\s*\*\*ADVISE:\*\*\s*(accept-with-nits|accept|send-back)\b",
    re.I,
)
RIGOR_RE = re.compile(
    r"\*\*Rigor:\*\*\s*(architecture|instrument|change|brief|vibe)\b",
    re.I,
)
ACCEPTING = {"accept", "accept-with-nits"}
NEEDS_RIGOR = {"architecture", "instrument"}


def change_rigor(change_dir: Path) -> str | None:
    proposal = change_dir / "proposal.md"
    if not proposal.is_file():
        return None
    text = proposal.read_text(encoding="utf-8")
    m = RIGOR_RE.search(text)
    if m:
        return m.group(1).lower()
    if (change_dir / "design.md").is_file() and re.search(r"\bADR", text, re.I):
        return "architecture"
    return None


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


def needs_advise(change_dir: Path) -> bool:
    proposal = change_dir / "proposal.md"
    if not proposal.is_file():
        return False
    banner = None
    for i, line in enumerate(proposal.read_text(encoding="utf-8").splitlines()):
        if i >= 40:
            break
        m = re.match(r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b", line.strip())
        if m:
            banner = m.group(1)
            break
    if banner != "ACTIVE BUILD":
        return False
    rigor = change_rigor(change_dir)
    if rigor not in NEEDS_RIGOR:
        return False
    return last_advise_verdict(change_dir) not in ACCEPTING


def needs_advise_ids(openspec: Path) -> list[str]:
    changes = openspec / "changes"
    if not changes.is_dir():
        return []
    ids: list[str] = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        if needs_advise(child):
            ids.append(child.name)
    return ids


def write_node_blocked(node: dict, blocked_ids: set[str]) -> bool:
    """True if this is a write/implement node of a change that needs advise."""
    cid = node.get("change_id")
    if not cid or str(cid) not in blocked_ids:
        return False
    if str(node.get("kind") or "").lower() == "advise":
        return False
    if str(node.get("permission") or "write").lower() == "read":
        return False
    return True
