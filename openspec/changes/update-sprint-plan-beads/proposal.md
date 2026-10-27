# update-sprint-plan-beads

> **ACTIVE BUILD**

## Preparation

2026-10-27. Outcome: still valid. Authority: "activate and run" on
`bazaar-8hs`. Upstream `update-sprint-plan-openspec` is archived in
`242e5ce`. The living default-loop spec now stores factory plans in
the change directory. This node adds story beads on that store. No
`design.md`. ADRs: none.

## Why

Intake still decomposes work into story markdown. The user chose the
scrum shape that this repo already uses: a bead holds the story, and
`tasks.md` holds the acceptance checkboxes.

## What

- After epic split, create beads instead of `stories/*.md`.
- Mirror each story's acceptance as a checkbox in the parent change's
  `tasks.md`.
- `sprint-to-beads` is the normal end of intake, not an optional flag.
- Depends on `update-sprint-plan-openspec` for the change directory.

## Impact

- Capabilities: ADDED default-loop (a story is a bead).
- ADRs: none.

## User journey & surfaces

No new UI because the surfaces are `bd ready` and the change's
`tasks.md`.

Working: the factory finishes decomposition and `bd ready` lists the
stories. Empty: no stories yet, so no beads are minted. Failed: a phase
writes `stories/*.md`. Off: a one-node `intend` that never asked for
the factory.

## Out of scope

- Where the change directory lives (`update-sprint-plan-openspec`).
- PRD and vision paths (`update-prd-vision-openspec`).
- Choosing story points or sprint calendars.
