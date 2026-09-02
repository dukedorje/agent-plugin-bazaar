---
name: status
description: >
  Board status: READY, PENDING, ASK, EYES, PUNT, beads, parked.
  Use when asked for status, what's ready, what's unblocked, what's
  parked, the ready-set, the morning pile, or "what's on deck".
user-invocable: true
argument-hint: "[--parked|--ready]"
---

# status

The observe script is `scripts/status.py` **in this skill directory**
(the folder that contains this SKILL.md). Do **not** run
`scripts/ready.py` from the current repo unless that file exists —
it is a shim. The skill script finds `openspec/` by walking up
from cwd, and unblocked beads via `bd list --ready` in cwd.

```
python3 <this-skill-dir>/scripts/status.py
python3 <this-skill-dir>/scripts/status.py --json
python3 <this-skill-dir>/scripts/status.py --parked
python3 <this-skill-dir>/scripts/status.py --ready
```

Print the command output. That is the report. Do not re-derive the
ready-set by grepping banners yourself. Do not run `bd ready` as a
second report — beads are already on this card.

Sources (union, labeled, not collapsed):

- **READY (OpenSpec)** — `ACTIVE BUILD` with open *implement* boxes
  (not ASK / EYES / PUNT). JSON `ready` is this list only.
- **NEEDS ACTIVATION (OpenSpec)** — `PENDING` drafts.
- **NEEDS ADVISE (OpenSpec)** — `ACTIVE BUILD` architecture/instrument
  with no accepting `reviews/*-advise.md` (or last verdict `send-back`).
- **ASK** — open owed boxes matching ASK (a decision). Next is `steer`.
- **EYES** — open owed boxes matching EYES / by-eye / human-verify.
  Look, then check the box. These are not READY. Print **YOUR EYES**
  and a **Next:** command (`Next: /run-wave` on the box, else
  `/status`). `/run` halt on this face is `stop: eyes`.
- **PUNT** — open owed boxes matching PUNT (last-resort second-family
  advise).
- **BEADS (bd ready)** — unblocked beads. Bare `/run` walks this list
  (landing → `change`, leftover task → `intend`) unless `--no-beads`.
- **PARKED (OpenSpec)** — in-flight `PARKED` banners plus
  `openspec/parked.md`.

The morning pile is this card (`/status`), not `/run`. `/ready` is an alias.

If the script prints `no openspec/` and beads are also empty, it is
not a guessed ready-set. If beads are present, the OpenSpec lens is
empty and beads still count.

Do not implement. Do not unpark. If they want to start something, hand
off to `act` (OpenSpec ready), `intend --extract-from` (orphan bead),
or wait for activation (pending).
