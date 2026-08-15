## ADDED Requirements

### Requirement: One skill tree

The system SHALL keep canonical skill files at
`plugins/intention/skills/<verb>/SKILL.md` for intend, change, act, fold,
and brief. `.agents/skills/<verb>` SHALL resolve to the same directory.

#### Scenario: Grok sees the verbs in-repo

- GIVEN a clone of this repo
- WHEN Grok starts in the repo root
- THEN it discovers the five verbs from `.agents/skills/`

### Requirement: Marketplaces point at the plugin

Both marketplace indexes SHALL list `intention` → `./plugins/intention`.

#### Scenario: Either marketplace index names intention

- GIVEN either index
- WHEN a reader looks up `intention`
- THEN the source path is `./plugins/intention`

### Requirement: Foreign harnesses get packets

Skill bodies SHALL say foreign workers receive a packet, never a slash
command.

#### Scenario: act on a foreign worker

- GIVEN `act` assigns Codex
- WHEN it dispatches
- THEN the worker gets packet JSON

### Requirement: MetaDev fork is parked

Extending MetaDev as the home of these verbs SHALL wait for ADR-003's
revive condition.

#### Scenario: Someone proposes vendoring MetaDev commands

- GIVEN ADR-003
- WHEN a change would copy MetaDev commands as the verb surface
- THEN that change is Path B and remains PARKED
