## MODIFIED Requirements

### Requirement: sprint-plan is parked
<!-- base: a5ecd2c5cdc727e61324e73076c47853c20f1215 openspec/specs/default-loop/spec.md -->

`plugins/morphist-tools/skills/sprint-plan/SKILL.md` SHALL be the
intake factory only when the user asks for `/sprint-plan` or for a
planning session that names the factory. A generic planning request
SHALL start at `intend` and SHALL NOT start Phase 0. Plan narrative
and phase progress SHALL be written only under
`openspec/changes/<change-id>/`: `proposal.md`, `tasks.md`, optional
`design.md`, and `specs/<capability>/spec.md` deltas. An ADR in
`ARCHITECTURE.md` is a bounded non-plan output when the shape
changes. The factory phases SHALL be only Phase 0 Discovery, Phase 1
Requirements, Phase 1B Scoping, Phase 1.5 UX, and Phase 2A
Architecture. The factory SHALL NOT create an intake epic, a child
epic, a story bead, or a per-acceptance checkbox, and SHALL NOT run
`sprint-to-beads`. The skill SHALL NOT create `docs/sprints/` or
`.omc/sprint-plan/`. It SHALL keep `disable-model-invocation: true`.
Its description SHALL name the OpenSpec change directory as the plan
and SHALL point planning that does not name the factory at `intend`.

Instruction files for Phases 2B, 3, 4, and 5 SHALL NOT remain on disk.
Phase progress for the phases that remain SHALL be checkboxes in that
change's `tasks.md`.

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
- AND it does not create an intake epic or a story bead

### Requirement: Plan documents are the change directory
<!-- base: a5ecd2c5cdc727e61324e73076c47853c20f1215 openspec/specs/default-loop/spec.md -->

A factory intake SHALL store its plan narrative and phase progress
only as the OpenSpec change: `proposal.md`, `tasks.md`, optional
`design.md`, and spec deltas. Discovery, requirements, scope, UX, and
architecture narrative SHALL map onto those files. An ADR in
`ARCHITECTURE.md` SHALL be a non-plan output, not a second plan. The
factory SHALL NOT emit a child epic, a child change, or a story list
as the breakdown of the intake. A sprint number, `docs/sprints/`
path, or `phase-state.json` SHALL NOT be a plan document.

#### Scenario: Phase finishes

- GIVEN an active `sprint-plan` intake
- WHEN a phase in 0, 1, 1B, 1.5, or 2A completes
- THEN its narrative is in the change directory
- AND the matching `tasks.md` box is the record that the phase finished
- AND no story bead is created

## REMOVED Requirements

### Requirement: A story is a bead and a checkbox
<!-- base: a5ecd2c5cdc727e61324e73076c47853c20f1215 openspec/specs/default-loop/spec.md -->

## ADDED Requirements

### Requirement: Intake ends at architecture

When Phase 2A is checked, `sprint-plan` SHALL stop. Its completion
report SHALL name the change id and SHALL give `intend` on that
change id as the next command. It SHALL NOT open Phase 2B, Phase 3,
Phase 4, or Phase 5.

#### Scenario: Architecture is checked

- GIVEN an intake whose tasks include a checked Phase 2A
- WHEN the factory reports completion
- THEN the next command is `intend` with that change id
- AND the change directory has no story beads and no intake epic

### Requirement: Decomposition is an intend node

The unit of split after a plan exists SHALL be an intend node: one
acceptance surface, one landing (`add-<id>`, brief, or direct fix),
and an edge only where the later node needs a committed artifact.
The bead type SHALL be `node`. Intake SHALL NOT record that split.
`bd ready` SHALL be the queue of unblocked nodes, not of story tasks
parented to an intake epic.

#### Scenario: Finished intake is split

- GIVEN a change that has finished Phase 2A and has no story beads
- WHEN someone asks how the work splits
- THEN the split is an intend DAG of nodes
- AND no intake epic is created to hold it

### Requirement: A beads corpus proposes nodes

`sprint-from-beads` SHALL write `proposal.md`, `design.md`, and
`tasks.md` under one `openspec/changes/<change-id>/` from an existing
beads corpus. The split it proposes SHALL be intend nodes for cuts
that are real artifact dependencies. It SHALL NOT create epic beads
or task beads as that split, and SHALL NOT backfill story acceptance
as the work list. Rewrites of non-empty bead fields SHALL stay gated.

#### Scenario: Beads already exist

- GIVEN a beads corpus and no request for the factory
- WHEN `sprint-from-beads` runs
- THEN one change directory holds the narrative
- AND the proposed breakdown is intend nodes
- AND no new epic bead is created

### Requirement: sprint-to-beads is dropped

`plugins/morphist-tools/skills/sprint-to-beads/` SHALL NOT exist.
`CONVENTIONS.md` SHALL list `sprint-to-beads` as dropped.
`CLAUDE.md` SHALL NOT present it as an invocable skill. A request to
materialize stories from an intake SHALL be answered with `intend`
on that change id.

#### Scenario: Someone asks to materialize stories

- GIVEN a change that finished architecture
- WHEN someone asks for `sprint-to-beads`
- THEN the skill file is not there to run
- AND the reply points at `intend` on that change id
