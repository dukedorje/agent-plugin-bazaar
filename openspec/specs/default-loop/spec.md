# default-loop

What a stranger is offered first. Folded from `park-sprint-plan` on
2026-08-15 (D1).

## Purpose

The default path from intention to running software is the loop
`intend` → `steer` → `change` → `advise` → `act` → `demo` → `fold` (plus
`brief` / `ready`). `run` is the campaign that walks that loop until
a stop predicate. `steer` is not a campaign wave. The 10-phase
factory exists but is not available work.

## ADDED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`steer`, `change`, `advise`, `act`, `demo`, `fold`, `brief`, `debrief`,
`map`, `status`, and `run` as the default planning loop. `run` is
the campaign; `map` and `status` are observe; `brief` / `debrief`
are disposable decide; `steer` is human-gated guidance (not a
campaign wave); `demo` is the human trying the iteration after
`act` and before `fold`; the rest are stages. `ready` SHALL be listed only
as an alias of `status`. `run-wave` SHALL be listed as the act
fan-out, not a default-loop stage.

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `steer` and `demo`

#### Scenario: Stranger asks how to chain

- GIVEN the default-loop presentation
- WHEN they want more than one stage without typing each
- THEN they are pointed at `run`, not at a second catalog of execute
  verbs

### Requirement: sprint-plan is parked

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

### Requirement: Catalogs list only skills that exist

`CLAUDE.md` Skills Reference and marketplace plugin versions SHALL match
the skill directories on disk and `plugin.json` versions. Dropped skill
names SHALL NOT appear as if they were invocable.

#### Scenario: Stranger reads CLAUDE.md

- GIVEN the Skills Reference
- WHEN they look for `backlog` or `status`
- THEN those names are absent (they live only in CONVENTIONS as dropped)

#### Scenario: validate.sh versions

- GIVEN `./validate.sh`
- WHEN it checks morphist-tools
- THEN marketplace.json version equals plugin.json version

### Requirement: run may enter any loop stage

`run` SHALL be allowed to enter `intend`, `change`, `advise`,
`act`, or `fold` as a campaign wave. It SHALL NOT be presented as
only `change` → `advise` → `act`. `ready`, `map`, `brief`, `debrief`, and `steer` SHALL stay
outside that wave set.

#### Scenario: Stranger asks if run can intend

- GIVEN the default-loop presentation
- WHEN they have a goal and no change-id
- THEN they are pointed at `/run` with that goal, which owes
  `next: intend`, not only at typing `/intend` first

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
