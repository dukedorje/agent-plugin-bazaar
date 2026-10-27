## ADDED Requirements

### Requirement: PRD and vision seed a change

`/prd` and `/vision` SHALL write or update one
`openspec/changes/<change-id>/`. A PRD SHALL land in `proposal.md`
and spec deltas. A vision SHALL land in that proposal's Why and What,
and in `design.md` when it changes the architecture. Neither skill
SHALL write `docs/prd-*.md` or `docs/products/`. The handoff SHALL be
`/sprint-plan <change-id>`.

#### Scenario: PRD workshop ends

- GIVEN a finished `/prd` interview
- WHEN the skill saves
- THEN the body is a PENDING change
- AND no file is created under `docs/prd-` or `docs/products/`

#### Scenario: Next step

- GIVEN that change id
- WHEN the skill tells the user what to run
- THEN the command is `/sprint-plan <change-id>`
