---
name: ready
description: >
  List ready unblocked work from OpenSpec and beads, plus everything
  parked. Use when asked what's ready, what's unblocked, what's parked,
  the ready-set, or "what's on deck".
user-invocable: true
argument-hint: "[--parked|--ready]"
---

# ready

The observe script is `scripts/ready.py` **in this skill directory**
(the folder that contains this SKILL.md). Do **not** run
`scripts/ready.py` from the current repo unless that file exists —
it is not required. The skill script finds `openspec/` by walking up
from cwd, and unblocked beads via `bd list --ready` in cwd.

```
python3 <this-skill-dir>/scripts/ready.py
python3 <this-skill-dir>/scripts/ready.py --json
python3 <this-skill-dir>/scripts/ready.py --parked
python3 <this-skill-dir>/scripts/ready.py --ready
```

Print the command output. That is the report. Do not re-derive the
ready-set by grepping banners yourself. Do not run `bd ready` as a
second report — beads are already on this card.

Sources (union, labeled, not collapsed):

- **READY (OpenSpec)** — `ACTIVE BUILD` changes with open owed
  checkboxes (unblocked). JSON `ready` is this list only — `/run`
  `--until empty` acts these, not beads.
- **NEEDS ACTIVATION (OpenSpec)** — `PENDING` drafts. Not ready until
  a human activates.
- **NEEDS ADVISE (OpenSpec)** — `ACTIVE BUILD` architecture/instrument
  with no accepting `reviews/*-advise.md` (or last verdict `send-back`).
- **BEADS (bd ready)** — unblocked beads (briefs, tasks, features,
  epics). JSON `beads`. Bare `/run` (default `--until roll`) already walks this list
  (landing → `change`, leftover task → `intend`). An empty OpenSpec
  lens is not an empty board.
- **PARKED (OpenSpec)** — in-flight `PARKED` banners plus
  `openspec/parked.md`.

If the script prints `no openspec/` and beads are also empty, it is
not a guessed ready-set. If beads are present, the OpenSpec lens is
empty and beads still count.

Do not implement. Do not unpark. If they want to start something, hand
off to `act` (OpenSpec ready), `intend --extract-from` (orphan bead),
or wait for activation (pending).
