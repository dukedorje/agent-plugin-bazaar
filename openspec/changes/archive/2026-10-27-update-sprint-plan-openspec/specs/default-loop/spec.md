## MODIFIED Requirements

### Requirement: sprint-plan is parked
<!-- base: 459f6878d71d86bd1942d5da911655decc864828 openspec/specs/default-loop/spec.md -->

`plugins/morphist-tools/skills/sprint-plan/SKILL.md` SHALL be the
intake factory only when the user asks for `/sprint-plan` or for a
planning session that names the factory. A generic planning request
SHALL start at `intend` and SHALL NOT start Phase 0. Plan narrative
and phase progress SHALL be written only under
`openspec/changes/<change-id>/`: `proposal.md`, `tasks.md`, optional
`design.md`, and `specs/<capability>/spec.md` deltas. An ADR in
`ARCHITECTURE.md` is a bounded non-plan output when the shape
changes. A child bead or a child change id is a handoff, not a plan
document. Story beads belong to `update-sprint-plan-beads`. The
skill SHALL NOT create `docs/sprints/` or `.omc/sprint-plan/`. It
SHALL keep `disable-model-invocation: true`. Its description SHALL
name the OpenSpec change directory as the plan and SHALL point
planning that does not name the factory at `intend`.

The phase files stay on disk. Phase progress SHALL be checkboxes in
that change's `tasks.md`.

#### Scenario: Model considers sprint-plan unprompted

- GIVEN no user request for `/sprint-plan` or for a planning session that names the factory
- WHEN the skill description is read
- THEN it does not auto-invoke
- AND it does not tell the agent to start Phase 0
- AND a generic planning request still starts at `intend`

#### Scenario: Explicit intake

- GIVEN the user asks for `/sprint-plan` or a planning session that names the factory
- WHEN the factory starts
- THEN it creates or edits one `openspec/changes/<change-id>/`
- AND it does not write `docs/sprints/` or `.omc/sprint-plan/`

## ADDED Requirements

### Requirement: Plan documents are the change directory

A factory intake SHALL store its plan narrative and phase progress
only as the OpenSpec change: `proposal.md`, `tasks.md`, optional
`design.md`, and spec deltas. Discovery, requirements, scope, UX, and
architecture narrative SHALL map onto those files. An ADR in
`ARCHITECTURE.md` and a child bead or child change id SHALL be
non-plan outputs, not a second plan. A sprint number, `docs/sprints/`
path, or `phase-state.json` SHALL NOT be a plan document.

#### Scenario: Phase finishes

- GIVEN an active `sprint-plan` intake
- WHEN a phase completes
- THEN its narrative is in the change directory
- AND the matching `tasks.md` box is the record that the phase finished
