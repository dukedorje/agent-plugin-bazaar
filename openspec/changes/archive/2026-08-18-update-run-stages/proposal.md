# update-run-stages

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-18 (chat: update meta-dev `run` so a named
landing can dispatch `change`).

## Why

`/run add-sheaf-type` halted on `stop: no-ready` and never said
`next: change`. The skill prose already walks stages; `run.py` only
emits `next: act` or `next: null`. A named landing with no
`openspec/changes/<id>/` is an owed `change` wave, not a missing
observer. Architecture that needs a read is an owed `advise` wave,
not an `act`.

## What

- Accept a positional scope id (`/run add-x`)
- Emit `next: change` → `next: advise` → `next: act` in that order
- `stop: no-ready` only when the observe script is missing
- Missing `openspec/` + a named scope → `change`, not halt
- `--until advise` runs the advise stage and does not proceed to `act`
- PENDING still never flips
- Capability: MODIFIED `verbs`

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat, names a landing.

1. Says `/run add-sheaf-type`.
2. **Working (no directory)** — card `next: change`, focus
   `add-sheaf-type`. Conductor re-reads `change/SKILL.md` for one
   wave.
3. **Working (architecture, no accept)** — card `next: advise`.
   Conductor re-reads `advise/SKILL.md`. Does not `act`.
4. **Working (ready write, advise accept or no advise owed)** —
   card `next: act`.
5. **Empty** — no scope, no ready, no advise: card stop empty.
6. **Failed** — PENDING scope: stop activation, banner unchanged.
7. **Off** — `ready.py` missing: stop `no-ready`. Stages still
   work one at a time.

`No new UI because` the surfaces are `/run` and
`plugins/intention/skills/run/scripts/run.py`.

## Out of scope

- Leftover `openspec/changes/add-run-verb/` fold-debt
- `--until fold` dispatch (still a stop gate)
- `@skills` / Path B / foreign spawn adapters
- Flipping PENDING or by-eye boxes
