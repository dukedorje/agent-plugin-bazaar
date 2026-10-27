## MODIFIED Requirements

### Requirement: sprint-plan is parked
<!-- base: 459f6878d71d86bd1942d5da911655decc864828 openspec/specs/default-loop/spec.md -->

`plugins/morphist-tools/skills/sprint-plan/SKILL.md` SHALL be the
intake factory when the user asks for a planning session or for
`/sprint-plan`. It SHALL write only under
`openspec/changes/<change-id>/`: `proposal.md`, `tasks.md`, optional
`design.md`, and `specs/<capability>/spec.md` deltas. It SHALL NOT
create `docs/sprints/` or `.omc/sprint-plan/`. It SHALL keep
`disable-model-invocation: true` so an unrelated task does not
auto-start Phase 0. Its description SHALL name the OpenSpec change
directory as the plan, not a parked side path and not `intend`.

The phase files stay on disk. Phase progress SHALL be checkboxes in
that change's `tasks.md`.

#### Scenario: Model considers sprint-plan unprompted

- GIVEN no user request for the factory or a planning session
- WHEN the skill description is read
- THEN it does not auto-invoke
- AND it does not tell the agent to start Phase 0

#### Scenario: Explicit intake

- GIVEN the user asks for `/sprint-plan` or a planning session that uses the factory
- WHEN the factory starts
- THEN it creates or edits one `openspec/changes/<change-id>/`
- AND it does not write `docs/sprints/` or `.omc/sprint-plan/`

## ADDED Requirements

### Requirement: Plan documents are the change directory

A planning session SHALL store its documents only as the OpenSpec
change: `proposal.md`, `tasks.md`, optional `design.md`, and spec
deltas. Discovery, requirements, scope, UX, and architecture narrative
SHALL map onto those files. A sprint number, `docs/sprints/` path, or
`phase-state.json` SHALL NOT be a plan document.

#### Scenario: Phase finishes

- GIVEN an active `sprint-plan` intake
- WHEN a phase completes
- THEN its narrative is in the change directory
- AND the matching `tasks.md` box is the record that the phase finished
