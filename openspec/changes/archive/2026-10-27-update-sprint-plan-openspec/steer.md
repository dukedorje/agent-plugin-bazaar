# steer update-sprint-plan-openspec

**When.** 2026-10-27
**Depth.** standard

## Decided

- Plan store: OpenSpec change directory only (user)
  Why: a second tree in `docs/sprints/` or `.omc/sprint-plan/` drifts from the living specs.
- Factory: retarget and revive (user)
  Why: the 10-phase intake stays, and it writes the change directory.
- Stories: bead plus `tasks.md` checkbox (user)
  Why: recorded here because the factory must not grow `stories/*.md`. The bead work is `update-sprint-plan-beads`.

## Skipped

None.

## Feeds change

Revive `sprint-plan` as an OpenSpec writer. One verb-led change id.
Phases fill `proposal.md`, optional `design.md`, spec deltas, and
`tasks.md`. No sprint folders, no `.omc/` state, no story markdown.
Models still do not auto-start the factory.
