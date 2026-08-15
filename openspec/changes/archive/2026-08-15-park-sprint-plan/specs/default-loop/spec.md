## ADDED Requirements

### Requirement: Default verbs

Orientation SHALL present intend/change/act/fold/brief as the default loop.

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install intention, not sprint-plan

### Requirement: sprint-plan is parked

sprint-plan SKILL.md SHALL be PARKED with disable-model-invocation.
Revive: explicit 10-phase / --thorough request.

#### Scenario: Model considers sprint-plan unprompted

- GIVEN no factory request
- WHEN the description is read
- THEN it says PARKED and points at intend

#### Scenario: Explicit revive

- GIVEN an explicit factory request
- WHEN the skill runs
- THEN the body below the banner may run
