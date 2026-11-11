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
READER_RE = re.compile(r"^>\s*\*\*READER:\*\*\s*\S+", re.I)
RIGOR_RE = re.compile(
    r"\*\*Rigor:\*\*\s*(architecture|instrument|change|brief|vibe)\b",
    re.I,
)
ACCEPTING = {"accept", "accept-with-nits"}  # old alias still counts as accept
NEEDS_RIGOR = {"architecture", "instrument"}
# `…-re-advise-2.md` vs `…-re-advise.md`: '-' < '.', so lex sort picks
# the unnumbered send-back. Unnumbered is series 1; `-sendback` is 0.
_TRAILING_SEQ = re.compile(r"^(.*)-(\d+)$")


def review_sort_key(path: Path) -> tuple[str, int]:
    stem = path.name[:-3] if path.name.endswith(".md") else path.name
    if stem.endswith("-sendback"):
        return (stem[: -len("-sendback")], 0)
    m = _TRAILING_SEQ.match(stem)
    if m:
        return (m.group(1), int(m.group(2)))
    return (stem, 1)


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


def _verdict_in(text: str) -> tuple[str | None, bool]:
    verdict = None
    has_reader = False
    for line in text.splitlines()[:40]:
        stripped = line.strip()
        m = ADVISE_RE.match(stripped)
        if m:
            verdict = m.group(1).lower()
        if READER_RE.match(stripped):
            has_reader = True
    return verdict, has_reader


def latest_advise_review(change_dir: Path) -> tuple[str | None, Path | None]:
    """Newest review that carries an ADVISE line, and that verdict.

    An accept with no READER line does not count. The path is still
    returned so a caller can say the file was ignored.
    """
    reviews = change_dir / "reviews"
    if not reviews.is_dir():
        return None, None
    files = sorted(
        (p for p in reviews.iterdir() if p.is_file() and p.name.endswith(".md")),
        key=review_sort_key,
    )
    for path in reversed(files):
        local, reader = _verdict_in(path.read_text(encoding="utf-8"))
        if local is None:
            continue
        if local in ACCEPTING and not reader:
            return None, path
        return local, path
    return None, None


def last_advise_verdict(change_dir: Path) -> str | None:
    verdict, _path = latest_advise_review(change_dir)
    return verdict


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
    tasks = change_dir / "tasks.md"
    if tasks.is_file() and any(
        line.strip() == "- [ ] Fresh advise after preparation"
        for line in tasks.read_text(encoding="utf-8").splitlines()
    ):
        return True
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
