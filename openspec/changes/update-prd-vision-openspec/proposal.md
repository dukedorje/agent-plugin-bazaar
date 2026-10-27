# update-prd-vision-openspec

> **PENDING**

## Why

`/prd` and `/vision` still save `docs/prd-{slug}.md` and
`docs/products/{name}/`, then tell the user to run `/sprint-plan` on
that path. The plan store is the OpenSpec change directory, so the
front door has to seed that directory.

## What

- A PRD workshop writes or updates `openspec/changes/<change-id>/proposal.md`
  and, when it has requirements, spec deltas.
- A vision workshop writes the same change's Why and What, and
  `design.md` when the vision changes the architecture.
- The handoff is `/sprint-plan <change-id>`, not a path under `docs/`.
- Depends on `update-sprint-plan-openspec`.

## Impact

- Capabilities: ADDED default-loop (PRD and vision seed a change).
- ADRs: none.

## User journey & surfaces

No new UI because the surfaces are `/prd`, `/vision`, and the change
directory they leave behind.

Working: the workshop ends on a PENDING change id. Empty: the user
stops before there is enough to write a proposal, and no `docs/` file
is created. Failed: the skill writes `docs/prd-*.md` or
`docs/products/`. Off: the user never runs `/prd` or `/vision`.

## Out of scope

- Migrating existing `docs/prd-*.md` and `docs/products/` trees.
- The factory's phase map (`update-sprint-plan-openspec`).
- Story beads (`update-sprint-plan-beads`).
