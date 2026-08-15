#!/usr/bin/env python3
"""Focused verify for F1: five verbs exist, frontmatter matches, Grok links resolve."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"
AGENTS = PLUGIN.parents[1] / ".agents" / "skills"
VERBS = ("intend", "change", "act", "fold", "brief")

FM = re.compile(r"^---\n(.*?)\n---", re.S)


def name_from(text: str) -> str | None:
    m = FM.match(text)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def main() -> int:
    errors: list[str] = []
    for verb in VERBS:
        skill = SKILLS / verb / "SKILL.md"
        if not skill.is_file():
            errors.append(f"missing {skill.relative_to(PLUGIN.parent.parent)}")
            continue
        text = skill.read_text(encoding="utf-8")
        got = name_from(text)
        if got != verb:
            errors.append(f"{skill.name}: name {got!r} != {verb!r}")
        if "description:" not in text[:800]:
            errors.append(f"{verb}: missing description")
        link = AGENTS / verb
        if not link.exists():
            errors.append(f".agents/skills/{verb} missing")
        elif link.resolve() != skill.parent.resolve():
            errors.append(
                f".agents/skills/{verb} -> {link.resolve()} "
                f"!= {skill.parent.resolve()}"
            )
    if errors:
        for e in errors:
            print(e)
        print(f"FAIL {len(errors)}")
        return 1
    print(f"pass {len(VERBS)} verbs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
