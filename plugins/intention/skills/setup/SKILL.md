---
name: setup
description: >
  Make a repo ready for Intention: bd installed, beads initialized, the
  `node` issue type registered, OpenSpec-lite layout, scratch dirs
  (`.worktrees/`, `.spawns/`, `groups/`) gitignored, agent
  instructions pointed at openspec. Idempotent. Use in a new repository, when `bd create --type node` fails with an
  invalid type, when `.beads/` or `openspec/` is missing, or when asked
  to set up / init / install / doctor intention.
user-invocable: true
argument-hint: "[--check] [--install] [--prefix <p>] [--no-pointer]"
---

# setup

The script is `scripts/setup.py` **in this skill directory**. Run it
from anywhere inside the target repo:

```
python3 <this-skill-dir>/scripts/setup.py --check   # report, change nothing
python3 <this-skill-dir>/scripts/setup.py           # apply
```

Default is apply. Print the command output. That is the report.

## What it ensures

| Item | Fix |
|---|---|
| git repository | none — tell the user to `git init` |
| `bd` on PATH | `--install` runs `brew install beads`; otherwise print the hint |
| `.beads/` | `bd init --non-interactive -q` (`--prefix` if given) |
| `types.custom` includes `node` | `bd config set types.custom <existing>,node` |
| `openspec/{specs,changes,changes/archive}/`, `README.md`, `AGENTS.md`, `project.md`, `parked.md` | created only if absent |
| `.gitignore` has `.worktrees/`, `.spawns/`, `groups/` | appended |
| `AGENTS.md` / `CLAUDE.md` mention `openspec/` | short Intention section appended (`--no-pointer` skips) |

It never overwrites an existing file and never re-inits beads.

## When bd is missing

Ask once before installing (it touches the machine, not the repo). On
yes, rerun with `--install`. No Homebrew: point at
https://github.com/gastownhall/beads and stop.

## After

Exit 0 and `Ready` → commit the new files in the target repo
(`chore: set up intention`) and push per the repo's rules. Then
`/intend`. Exit 2 → report the MISSING / FAILED rows and stop. Do not
hand-create `.beads/` or edit `.beads/config.yaml` to work around a
failed `bd` call.
