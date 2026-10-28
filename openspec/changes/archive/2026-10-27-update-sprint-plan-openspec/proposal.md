# update-sprint-plan-openspec

> **ACTIVE BUILD**

## Preparation

2026-10-27. Outcome: still valid. Authority: user said "activate and run"
on `bazaar-8hs` (grant plus `--go`). Bounds: this intention's three
nodes, the recorded non-goals, and the plan-store commitment. Blocked
descendants stay PENDING.

Upstream: no prior act result. Park fold is
`openspec/changes/archive/2026-08-15-park-sprint-plan`. Living file
`openspec/specs/default-loop/spec.md` blob
`459f6878d71d86bd1942d5da911655decc864828` matches the stamped
requirement "sprint-plan is parked".

Revised 2026-10-27 after `astra-arch-review` send-back. Outcome:
revised wording, same commitment. The factory starts only when named.
An ADR and a child bead are non-plan outputs.

Act landed 2026-10-27. Outcome: still valid. Authority unchanged.
Implementation `b288406` retargets
`plugins/morphist-tools/skills/sprint-plan/SKILL.md` onto the change
directory and keeps `disable-model-invocation: true`. Result
`21e8656` records that commit. Living blob
`459f6878d71d86bd1942d5da911655decc864828` still matches. Fold applies
the delta.

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

Working: the user asks for `/sprint-plan` or names the factory. The
factory writes one change directory. Empty: no product input yet, so it
asks and still does not create a sprint folder. Failed: a phase tries to
write `docs/sprints/` or `.omc/`. Off: a generic planning request stays
on `intend`, and models still do not auto-start the factory.

## Out of scope

- Story beads and `tasks.md` checkboxes (`update-sprint-plan-beads`).
- PRD and vision file paths (`update-prd-vision-openspec`).
- Migrating old `docs/sprints/` trees in other repos.
- Deleting the phase files.
- Implementing the retarget before this change is activated.
