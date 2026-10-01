#!/usr/bin/env python3
"""Make a repo ready for Intention: bd, beads, the node type, OpenSpec-lite.

Idempotent. Never overwrites a file that exists. `--check` reports only.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# bd issue types Intention writes (`bd create --type node`).
CUSTOM_TYPES = ("node",)
# Scratch dirs Intention writes at the repo root: conductor isolate
# worktrees, spawn stage prompts and leases, per-node group packets/results.
GITIGNORE = (".worktrees/", ".spawns/", "groups/")
GITIGNORE_HEADER = "# Intention scratch (conductor isolate, spawn stage, group packets)"
POINTER = (
    "## Intention\n\n"
    "Work loop: intend → steer → change → advise → act → fold.\n"
    "Tracker is beads (`bd`; DAG nodes are `--type node`). Living specs are\n"
    "`openspec/specs/`; in-flight work is `openspec/changes/`. Read\n"
    "[`openspec/AGENTS.md`](openspec/AGENTS.md) before changing behavior.\n"
)

OPENSPEC_README = """# openspec

Two-layer process memory. Living truth is `specs/`. In-flight work is
`changes/`. Status is a banner in the file.

Read [`AGENTS.md`](AGENTS.md). The `openspec` CLI is optional.
"""

OPENSPEC_AGENTS = """# OpenSpec-lite

Instructions for agents working with the Intention plugin.

## Before any task

- [ ] Living truth is `openspec/specs/<capability>/spec.md`, not a SHALL in
      `changes/` or `docs/`.
- [ ] `changes/` is not a mandate. Read the disposition banner. PENDING is
      a draft. PARKED is not work. Archived means folded — do not implement it.
- [ ] Restore-only, typo, pin, comment, test-for-existing-spec: fix directly.
      Do not scaffold a change.
- [ ] New behavior: verb-led `change-id`, `proposal.md` + `tasks.md` + deltas.
      `design.md` only when cross-cutting.
- [ ] Do not start write work on PENDING or PARKED. Wait for ACTIVE BUILD.

## Deltas, not rewrites

```
## ADDED Requirements
### Requirement: <name>
The system SHALL …
#### Scenario: <name>
- GIVEN …
- WHEN …
- THEN …
```

`MODIFIED` pastes the entire living requirement, then edits. `REMOVED`
names the requirement only. `fold` applies deltas to `specs/` and moves the
change to `changes/archive/YYYY-MM-DD-<id>/`.
"""

OPENSPEC_PROJECT = """# Project context

This file is conventions. It is not a requirements store. Requirements live
in `openspec/specs/` (what is built) and `openspec/changes/` (what should
change).

## Where work lands

| Kind of work | Lands in |
|---|---|
| New or changed behavior | `openspec/changes/<verb-led-id>/` |
| Restore intended behavior, typo, pin, comment, test for existing spec | Direct fix. No change. |
| Hard-won fact | `docs/LEARNINGS.md` |
| Work-graph state | beads (`bd`) |
"""

OPENSPEC_PARKED = """# Parked

> **PARKED** — register of parks that are not in-flight OpenSpec changes.

| id | kind | revive | where |
|---|---|---|---|
"""

OPENSPEC_FILES = {
    "README.md": OPENSPEC_README,
    "AGENTS.md": OPENSPEC_AGENTS,
    "project.md": OPENSPEC_PROJECT,
    "parked.md": OPENSPEC_PARKED,
}
OPENSPEC_DIRS = ("specs", "changes", "changes/archive")


class Report:
    def __init__(self, check: bool) -> None:
        self.check = check
        self.rows: list[dict[str, str]] = []

    def add(self, item: str, state: str, detail: str = "") -> None:
        # state: ok | fixed | would-fix | missing | failed
        self.rows.append({"item": item, "state": state, "detail": detail})

    def fix(self, item: str, detail: str) -> bool:
        """Record a fix; return True when the caller should apply it."""
        self.add(item, "would-fix" if self.check else "fixed", detail)
        return not self.check

    @property
    def blocked(self) -> bool:
        return any(r["state"] in ("missing", "failed") for r in self.rows)


def git_root(start: Path) -> Path | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return Path(out.strip())


def bd(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bd", *args],
        cwd=root,
        text=True,
        capture_output=True,
    )


def merge_types(current: str, want: tuple[str, ...]) -> str:
    have = [t.strip() for t in current.split(",") if t.strip()]
    for t in want:
        if t not in have:
            have.append(t)
    return ",".join(have)


def step_bd(root: Path, rep: Report, install: bool) -> bool:
    if shutil.which("bd"):
        proc = subprocess.run(["bd", "--version"], text=True, capture_output=True)
        rep.add("bd installed", "ok", proc.stdout.strip())
        return True
    brew = shutil.which("brew")
    if install and brew and not rep.check:
        proc = subprocess.run([brew, "install", "beads"], text=True, capture_output=True)
        if proc.returncode == 0 and shutil.which("bd"):
            rep.add("bd installed", "fixed", "brew install beads")
            return True
        rep.add("bd installed", "failed", (proc.stderr or proc.stdout).strip()[-400:])
        return False
    hint = "brew install beads" if brew else "see https://github.com/gastownhall/beads"
    rep.add("bd installed", "missing", f"install with: {hint} (or rerun with --install)")
    return False


def step_beads(root: Path, rep: Report, prefix: str | None) -> bool:
    if (root / ".beads").is_dir():
        rep.add("beads initialized", "ok", ".beads/")
        return True
    args = ["init", "--non-interactive", "-q"]
    if prefix:
        args += ["--prefix", prefix]
    if not rep.fix("beads initialized", "bd " + " ".join(args)):
        rep.add("bd custom types", "would-fix", "types.custom = " + ",".join(CUSTOM_TYPES))
        return False
    proc = bd(root, *args)
    if proc.returncode != 0:
        rep.rows[-1].update(state="failed", detail=(proc.stderr or proc.stdout).strip()[-400:])
        return False
    return True


def step_types(root: Path, rep: Report) -> None:
    proc = bd(root, "config", "get", "types.custom")
    if proc.returncode != 0:
        rep.add("bd custom types", "failed", (proc.stderr or proc.stdout).strip()[-400:])
        return
    # `bd config get` may print warnings after the value; the value is line one.
    lines = proc.stdout.strip().splitlines()
    current = lines[0].strip() if lines else ""
    if current.endswith("(not set)"):
        current = ""
    merged = merge_types(current, CUSTOM_TYPES)
    if merged == current:
        rep.add("bd custom types", "ok", f"types.custom = {current}")
        return
    if not rep.fix("bd custom types", f"types.custom = {merged}"):
        return
    proc = bd(root, "config", "set", "types.custom", merged)
    if proc.returncode != 0:
        rep.rows[-1].update(state="failed", detail=(proc.stderr or proc.stdout).strip()[-400:])


def step_openspec(root: Path, rep: Report) -> None:
    base = root / "openspec"
    made: list[str] = []
    for d in OPENSPEC_DIRS:
        path = base / d
        if not path.is_dir():
            made.append(f"openspec/{d}/")
            if not rep.check:
                path.mkdir(parents=True, exist_ok=True)
                (path / ".gitkeep").touch()
    for name, body in OPENSPEC_FILES.items():
        path = base / name
        if not path.exists():
            made.append(f"openspec/{name}")
            if not rep.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding="utf-8")
    if made:
        rep.fix("openspec layout", ", ".join(made))
    else:
        rep.add("openspec layout", "ok", "openspec/")


def step_gitignore(root: Path, rep: Report) -> None:
    path = root / ".gitignore"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    have = {line.strip() for line in text.splitlines()}
    need = [g for g in GITIGNORE if g not in have and g.rstrip("/") not in have]
    if not need:
        rep.add(".gitignore", "ok", ", ".join(GITIGNORE))
        return
    if not rep.fix(".gitignore", "add " + ", ".join(need)):
        return
    sep = "" if not text else ("\n" if text.endswith("\n") else "\n\n")
    block = sep + GITIGNORE_HEADER + "\n" + "\n".join(need) + "\n"
    path.write_text(text + block, encoding="utf-8")


def step_pointer(root: Path, rep: Report) -> None:
    """Point the repo's agent instructions at Intention's layout."""
    targets = [root / n for n in ("AGENTS.md", "CLAUDE.md") if (root / n).exists()]
    if not targets:
        targets = [root / "AGENTS.md"]
    missing = [
        p for p in targets
        if not p.exists() or "openspec/" not in p.read_text(encoding="utf-8")
    ]
    if not missing:
        rep.add("agent instructions", "ok", ", ".join(p.name for p in targets))
        return
    if not rep.fix("agent instructions", "append Intention section to " + ", ".join(p.name for p in missing)):
        return
    for p in missing:
        text = p.read_text(encoding="utf-8") if p.exists() else ""
        sep = "" if not text else ("\n" if text.endswith("\n") else "\n\n")
        p.write_text(text + sep + POINTER, encoding="utf-8")


def print_report(root: Path, rep: Report) -> None:
    mark = {"ok": "ok", "fixed": "FIXED", "would-fix": "TODO", "missing": "MISSING", "failed": "FAILED"}
    print(f"Intention setup · {root}" + (" · check only" if rep.check else ""))
    print()
    for r in rep.rows:
        line = f"- {mark[r['state']]:<7} {r['item']}"
        if r["detail"]:
            line += f" — {r['detail']}"
        print(line)
    print()
    if rep.blocked:
        print("Not ready. Resolve MISSING / FAILED, then rerun setup.")
    elif any(r["state"] == "would-fix" for r in rep.rows):
        print("Not ready. Rerun without --check to apply.")
    else:
        print("Ready. Next: /intend")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only; change nothing")
    ap.add_argument("--install", action="store_true", help="install bd with brew if missing")
    ap.add_argument("--prefix", help="beads issue prefix for bd init (default: bd's choice)")
    ap.add_argument("--no-pointer", action="store_true", help="do not touch AGENTS.md / CLAUDE.md")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--root", type=Path, default=None, help="repo root (default: git toplevel of cwd)")
    args = ap.parse_args(argv)

    root = (args.root or git_root(Path.cwd()) or Path()).resolve()
    rep = Report(args.check)
    if git_root(root) is None:
        rep.add("git repository", "missing", f"{root} is not in a git repo; run `git init` first")
    else:
        rep.add("git repository", "ok", str(root))
        if step_bd(root, rep, args.install) and step_beads(root, rep, args.prefix):
            step_types(root, rep)
        step_openspec(root, rep)
        step_gitignore(root, rep)
        if not args.no_pointer:
            step_pointer(root, rep)

    if args.json:
        print(json.dumps({"root": str(root), "check": rep.check, "rows": rep.rows}, indent=2))
    else:
        print_report(root, rep)
    if rep.blocked:
        return 2
    return 1 if args.check and any(r["state"] == "would-fix" for r in rep.rows) else 0


if __name__ == "__main__":
    sys.exit(main())
