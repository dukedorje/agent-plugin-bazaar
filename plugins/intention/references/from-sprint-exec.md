# Kept from sprint-exec

Extracted 2026-10-27 when morphist-tools `sprint-exec` was removed.
That skill dispatched `oh-my-claudecode` executors over story files in
`.omc/sprint-plan/` and `docs/sprints/`. OMC is uninstalled. Intention
`act` / `run` and `bd ready` already execute beads. Do not rebuild a
second dispatcher, a phase-state file, or a Dev Agent Record beside the bead.

## Spike before landing an unvalidated hypothesis

An ultraresearch synthesis can read like a prescription while its
hypothesis is still `confidence` below `high` or `verification` other
than `empirically-tested`. Landing that recipe in product code is the
expensive way to find out.

Before `act` on a bead whose decision cites such a hypothesis, run
`spike`. On **go**, the synthesis records `spike-artifact` and the bead
can proceed. On **no-go**, leave the decision open
(`bd update {id} --status open` plus a note that names the finding) and
do not land the recipe. An explicit human override is a `bd note` on
that decision, not a silent proceed.

`act` does not call `spike` by itself. The caller does.

## Beads is the only status record

- Work list is `bd ready`. Re-query it after a unit closes so newly
  unblocked children show up. Do not keep a private manifest.
- Start: `bd update {id} --status in_progress`.
- Success: `bd close {id} --reason "{one line}"`. File list and problems
  go on `bd note`. That note is the record.
- Blocker: leave the bead open, label it blocked, and note the type and
  detail. It then drops out of `bd ready`. Surface the blocker. Do not
  invent a workaround and close the bead.
- An epic is done when its child task beads are closed.
- Do not also write a story file, a Dev Agent Record, or
  `phase-state.json`.

## What a wave can and cannot see

Parallel units cannot read each other's notes while they run. A later
unit can. When `run` moves to the next sequential unit, put the prior
unit's hard-won fact in that unit's prompt (from the bead note or
`debrief`). Do not expect a parallel sibling to have it.

## Dry-run and resume

A dry-run prints the beads that would be picked up and stops. Resume
skips beads that are already closed. Re-running a closed bead takes an
explicit id.

## Do not port

Stop-threshold menus, huddle menus, ralph persistence, OMC `state_write`,
team fan-out, and story-file enrichment. Steer already does decision
menus. `run` already persists a campaign. `debrief` already expands one
finished unit. `retro` (morphist-tools) is the write-up for a whole body
of work.
