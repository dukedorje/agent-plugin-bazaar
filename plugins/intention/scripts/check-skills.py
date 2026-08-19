#!/usr/bin/env python3
"""Focused verify: nine verbs exist, frontmatter matches, Grok links resolve."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
SKILLS = PLUGIN / "skills"
REFS = PLUGIN / "references"
AGENTS = PLUGIN.parents[1] / ".agents" / "skills"
VERBS = ("intend", "change", "advise", "act", "fold", "brief", "debrief", "ready", "run")
REQUIRED_REFS = (
    "shared.md",
    "intend-dag.md",
    "change-templates.md",
    "act-io.md",
    "fold-steps.md",
    "harness.md",
    "ladder.json",
)

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
    for ref in REQUIRED_REFS:
        if not (REFS / ref).is_file():
            errors.append(f"missing references/{ref}")
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
    cli = shutil.which("skills")
    if cli:
        listed = subprocess.run(
            [cli, "add", str(SKILLS.parent), "--list", "-y"],
            check=False,
            capture_output=True,
            text=True,
        )
        text = listed.stdout + listed.stderr
        for verb in VERBS:
            if not re.search(rf"(?:^|[^A-Za-z0-9_-]){re.escape(verb)}(?:[^A-Za-z0-9_-]|$)", text):
                errors.append(f"skills add --list missed {verb}")
    if errors:
        for e in errors:
            print(e)
        print(f"FAIL {len(errors)}")
        return 1
    print(f"pass {len(VERBS)} verbs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
