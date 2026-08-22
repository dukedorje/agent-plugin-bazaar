# add-run-roll

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-22 (chat: go for it / direct enough).

## Why

`--until empty` only sees openspec READY. Unscoped `--until fold`
does not scan fold-legal changes. Send-back still looks like `act`.
Open beads with landings never enter the card. A “keep rolling
while unblocked” pass needs one observe upgrade, not a second
catalog.

## What

- `--until roll`: after each wave, pick the first of: fold-legal
  (scan inflight), send-back → `change`, `needs_advise` → `advise`,
  READY → `act`, unblocked bead with a verb-led landing and no
  change dir → `change`, unblocked task/feature with no landing
  (not epic, not `nod-`) → `intend --extract-from` that bead.
- Unscoped `--until fold` scans fold-legal the same way.
- Do not intend epics. Do not flip PENDING. `run.py` still
  launches zero workers.
- `--max-waves` is conductor policy on the skill, not a second
  executor.
- Capability: MODIFIED `verbs` (gate defaults + campaign observe).

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat.

1. Says `/run --until roll` (optional `--autonomous`).
2. **Working** — card names the next stage and focus; conductor
   re-reads that skill; re-observes.
3. **Empty** — nothing dispatchable except PENDING / PARKED /
   blocked.
4. **Off** — `--until empty` still ignores beads and fold-legal.

`No new UI because` the surfaces are `/run` and
`plugins/intention/skills/run/scripts/run.py`.

## Out of scope

- Making `debrief` a default wave
- Flipping PENDING
- Path B / `planctl`
- Raising `max_inflight` as a second tracker
