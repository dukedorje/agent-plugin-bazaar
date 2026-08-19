# default-loop

What a stranger is offered first. Folded from `park-sprint-plan` on
2026-08-15 (D1).

## Purpose

The default path from intention to running software is the loop
`intend` → `change` → `advise` → `act` → `fold` (plus `brief` /
`ready`). `run` is the campaign that walks that loop until a stop
predicate. The 10-phase factory exists but is not available work.

## ADDED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`change`, `advise`, `act`, `fold`, `brief`, `ready`, and `run` as
the default planning loop. `run` is the campaign; the others are
stages (or observe / disposable decide).

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `advise` and `run`

#### Scenario: Stranger asks how to chain

- GIVEN the default-loop presentation
- WHEN they want more than one stage without typing each
- THEN they are pointed at `run`, not at a second catalog of execute
  verbs

### Requirement: sprint-plan is parked

`plugins/morphist-tools/skills/sprint-plan/SKILL.md` SHALL carry an
in-file `PARKED` banner and `disable-model-invocation: true`. Its
description SHALL tell agents not to auto-invoke and to use `intend`.

Revive when the user explicitly asks for the 10-phase factory or
`--thorough` multi-week batch planning. The phase files stay on disk.

#### Scenario: Model considers sprint-plan unprompted

- GIVEN no user request for the factory
- WHEN the skill description is read
- THEN it says PARKED and points at `intend`

#### Scenario: Explicit revive

- GIVEN the user asks for `/sprint-plan --thorough` or “the 10-phase factory”
- WHEN the skill runs
- THEN the parked banner does not prevent following the body below it

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
only `change` → `advise` → `act`. `ready` and `brief` SHALL stay
outside that wave set.

#### Scenario: Stranger asks if run can intend

- GIVEN the default-loop presentation
- WHEN they have a goal and no change-id
- THEN they are pointed at `/run` with that goal, which owes
  `next: intend`, not only at typing `/intend` first
