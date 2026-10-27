# update-sprint-plan-openspec

> **PENDING**

## Why

A planning session still wants the 10-phase intake, and the documents it
produces have to be the OpenSpec change itself. `docs/sprints/` and
`.omc/sprint-plan/` are a second plan store. The user chose to revive
`sprint-plan` and point it at `openspec/changes/<change-id>/` only.

## What

- Take the PARKED banner off `sprint-plan` when this change is activated
  and implemented. Until then the living spec stays parked.
- The factory's spec directory is `openspec/changes/<change-id>/`.
- Phase narrative lands in `proposal.md`, optional `design.md`, and
  `specs/<capability>/spec.md` deltas.
- Phase progress is the checkboxes in `tasks.md`. No `phase-state.json`
  and no `.omc/sprint-plan/`.
- Do not create `docs/sprints/`.

## Impact

- Capabilities: MODIFIED default-loop (`sprint-plan is parked`); ADDED
  default-loop (plan documents are the change directory).
- ADRs: none. The two-layer tree in living-specs already names this layout.

## User journey & surfaces

No new UI because the surfaces are `/sprint-plan`, the change directory,
and `intend` for work that is not a factory intake.

Working: the user asks for a planning session or `/sprint-plan`. The
factory writes one change directory. Empty: no product input yet, so it
asks and still does not create a sprint folder. Failed: a phase tries to
write `docs/sprints/` or `.omc/`. Off: the user does not ask for the
factory, and models still do not auto-start it.

## Out of scope

- Story beads and `tasks.md` checkboxes (`update-sprint-plan-beads`).
- PRD and vision file paths (`update-prd-vision-openspec`).
- Migrating old `docs/sprints/` trees in other repos.
- Deleting the phase files.
- Implementing the retarget before this change is activated.
