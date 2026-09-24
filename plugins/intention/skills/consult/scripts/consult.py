#!/usr/bin/env python3
"""Run plugin spawn.py consult. Cwd stays the current project.

Do not call plugins/intention/scripts/spawn.py from the repo cwd —
that path only exists in the bazaar clone.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def find_spawn() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    if len(here.parents) >= 4:
        candidates.append(here.parents[3] / "scripts" / "spawn.py")
    for env in ("GROK_PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT", "CODEX_PLUGIN_ROOT"):
        root = os.environ.get(env)
        if root:
            candidates.append(Path(root) / "scripts" / "spawn.py")
    home = Path.home()
    candidates.extend(home.glob(".grok/installed-plugins/intention-*/scripts/spawn.py"))
    candidates.extend(
        home.glob(".claude/plugins/cache/*/intention/*/scripts/spawn.py")
    )
    cwd = Path.cwd()
    for root in [cwd, *cwd.parents]:
        candidates.append(root / "plugins" / "intention" / "scripts" / "spawn.py")
        if (root / ".git").exists():
            break
    seen: set[Path] = set()
    for cand in candidates:
        try:
            resolved = cand.resolve()
        except OSError:
            continue
        if resolved in seen or not resolved.is_file():
            continue
        seen.add(resolved)
        return resolved
    raise SystemExit(
        "spawn.py not found. Install the intention plugin bundle "
        "(grok/claude/codex plugin), not a skills-only copy."
    )


def main() -> None:
    spawn = find_spawn()
    os.execv(sys.executable, [sys.executable, str(spawn), "consult", *sys.argv[1:]])


if __name__ == "__main__":
    main()
