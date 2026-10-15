#!/usr/bin/env python3
"""Base check for MODIFIED and REMOVED requirement pastes.

A base comment sits in the requirement block:

    ### Requirement: Name
    <!-- base: <blob> openspec/specs/<capability>/spec.md -->

The blob is `git hash-object -w` of the living spec file at paste time.
Fold compares that requirement's text in the blob with the same requirement
in the working tree now. A difference is stale: fold applies nothing, and
run routes the change to change for a union re-paste.

A missing comment is unstamped. It does not refuse. The folder diffs by
hand and stamps before applying. That soft case is one release.

    python3 fold_base.py check <change-dir>
    python3 fold_base.py stamp <change-dir>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^### Requirement:\s*(.+?)\s*$", re.M)
SECTION_RE = re.compile(r"^##\s+(MODIFIED|REMOVED)\s+Requirements\s*$", re.M)
NEXT_SECTION_RE = re.compile(r"^##\s+", re.M)
BASE_RE = re.compile(
    r"<!--\s*base:\s*([0-9a-fA-F]{7,40})\s+(\S+)\s*-->"
)
REQ_SPLIT_RE = re.compile(r"(?=^### Requirement:)", re.M)


def repo_root(start: Path) -> Path | None:
    for cand in [start, *start.parents]:
        if (cand / ".git").exists():
            return cand
    return None


def living_path_ok(rel: str) -> bool:
    path = Path(rel)
    if path.is_absolute() or ".." in path.parts:
        return False
    if not rel.startswith("openspec/specs/"):
        return False
    return rel.endswith("/spec.md")


def sections(text: str) -> list[tuple[str, str]]:
    """(kind, body) for MODIFIED and REMOVED sections only."""
    marks = list(SECTION_RE.finditer(text))
    out: list[tuple[str, str]] = []
    for index, mark in enumerate(marks):
        start = mark.end()
        end = len(text)
        nxt = NEXT_SECTION_RE.search(text, start)
        if nxt:
            end = nxt.start()
        if index + 1 < len(marks) and marks[index + 1].start() < end:
            end = marks[index + 1].start()
        out.append((mark.group(1), text[start:end]))
    return out


def requirement_blocks(text: str) -> dict[str, str]:
    """Map requirement name to its block, including the heading."""
    found: dict[str, str] = {}
    for chunk in REQ_SPLIT_RE.split(text):
        if not chunk.startswith("### Requirement:"):
            continue
        match = HEADING_RE.match(chunk)
        if not match:
            continue
        found[match.group(1).strip()] = chunk.strip() + "\n"
    return found


def normalize(block: str) -> str:
    lines = []
    for line in block.splitlines():
        if BASE_RE.search(line):
            continue
        lines.append(line.rstrip())
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def git_bytes(repo: Path, args: list[str]) -> bytes | None:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def blob_text(repo: Path, blob: str) -> str | None:
    raw = git_bytes(repo, ["cat-file", "-p", blob])
    if raw is None:
        return None
    return raw.decode("utf-8", errors="replace")


def hash_file(repo: Path, path: Path) -> str | None:
    raw = git_bytes(repo, ["hash-object", "-w", "--", str(path)])
    if raw is None:
        return None
    return raw.decode("utf-8", errors="replace").strip()


def classify(change_dir: Path) -> dict[str, list[dict[str, str]]]:
    """Return stale and unstamped requirement rows. Never raises for a dirty tree."""
    stale: list[dict[str, str]] = []
    unstamped: list[dict[str, str]] = []
    specs = change_dir / "specs"
    if not specs.is_dir():
        return {"stale": stale, "unstamped": unstamped}
    repo = repo_root(change_dir)
    for spec in sorted(specs.glob("*/spec.md")):
        capability = spec.parent.name
        text = spec.read_text(encoding="utf-8")
        for kind, body in sections(text):
            for chunk in REQ_SPLIT_RE.split(body):
                if not chunk.startswith("### Requirement:"):
                    continue
                match = HEADING_RE.match(chunk)
                if not match:
                    continue
                name = match.group(1).strip()
                row = {
                    "requirement": name,
                    "capability": capability,
                    "kind": kind,
                    "path": "",
                }
                base = BASE_RE.search(chunk)
                if base is None:
                    unstamped.append(row)
                    continue
                blob, rel = base.group(1), base.group(2)
                row["path"] = rel
                row["base"] = blob
                if repo is None or not living_path_ok(rel):
                    row["why"] = "unresolvable-base"
                    stale.append(row)
                    continue
                past = blob_text(repo, blob)
                current_file = repo / rel
                if past is None or not current_file.is_file():
                    row["why"] = "unresolvable-base"
                    stale.append(row)
                    continue
                old_blocks = requirement_blocks(past)
                new_blocks = requirement_blocks(
                    current_file.read_text(encoding="utf-8")
                )
                old = old_blocks.get(name)
                new = new_blocks.get(name)
                if kind == "REMOVED" and old is not None and new is None:
                    continue
                if old is None or new is None or normalize(old) != normalize(new):
                    row["why"] = "living-requirement-changed"
                    stale.append(row)
    return {"stale": stale, "unstamped": unstamped}


def stamp(change_dir: Path) -> dict[str, list[str]]:
    """Write a base blob onto each MODIFIED or REMOVED block that lacks one."""
    repo = repo_root(change_dir)
    if repo is None:
        raise SystemExit(f"no git repo above {change_dir}")
    specs = change_dir / "specs"
    stamped: list[str] = []
    skipped: list[str] = []
    if not specs.is_dir():
        return {"stamped": stamped, "skipped": skipped}
    for spec in sorted(specs.glob("*/spec.md")):
        capability = spec.parent.name
        rel = f"openspec/specs/{capability}/spec.md"
        living = repo / rel
        text = spec.read_text(encoding="utf-8")
        if not living.is_file():
            for _, body in sections(text):
                for name in requirement_blocks(body):
                    skipped.append(f"{capability}:{name}")
            continue
        blob = hash_file(repo, living)
        if not blob:
            raise SystemExit(f"git hash-object failed for {rel}")
        pieces: list[str] = []
        cursor = 0
        for mark in SECTION_RE.finditer(text):
            pieces.append(text[cursor:mark.end()])
            rest_start = mark.end()
            nxt = NEXT_SECTION_RE.search(text, rest_start)
            rest_end = nxt.start() if nxt else len(text)
            body = text[rest_start:rest_end]
            rewritten: list[str] = []
            last = 0
            for chunk in REQ_SPLIT_RE.split(body):
                if not chunk.startswith("### Requirement:"):
                    rewritten.append(chunk)
                    continue
                if BASE_RE.search(chunk):
                    rewritten.append(chunk)
                    continue
                heading, _, remainder = chunk.partition("\n")
                comment = f"<!-- base: {blob} {rel} -->\n"
                rewritten.append(heading + "\n" + comment + remainder)
                match = HEADING_RE.match(chunk)
                if match:
                    stamped.append(f"{capability}:{match.group(1).strip()}")
                last = 1
            pieces.append("".join(rewritten) if last else body)
            cursor = rest_end
        pieces.append(text[cursor:])
        updated = "".join(pieces)
        if updated != text:
            spec.write_text(updated, encoding="utf-8")
    return {"stamped": stamped, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "stamp"))
    parser.add_argument("change_dir", type=Path)
    args = parser.parse_args()
    change = args.change_dir.resolve()
    if not change.is_dir():
        print(f"no change dir {change}", file=sys.stderr)
        return 2
    if args.command == "stamp":
        print(json.dumps(stamp(change), indent=2))
        return 0
    report = classify(change)
    print(json.dumps(report, indent=2))
    return 2 if report["stale"] else 0


if __name__ == "__main__":
    sys.exit(main())
