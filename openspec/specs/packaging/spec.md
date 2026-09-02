# packaging

How the default-loop verbs are hosted. Folded from `add-skills-packaging` on
2026-08-14 (F1) and `add-advise-verb` on 2026-08-17. Path A won. Path B is
parked — see ADR-003.

## Purpose

`intend`, `steer`, `change`, `advise`, `act`, `fold`, `brief`, `ready`,
and `run` load on Grok and Claude from one set of files.

## ADDED Requirements

### Requirement: One skill tree

The system SHALL keep canonical skill files at
`plugins/intention/skills/<verb>/SKILL.md` for
`intend`, `steer`, `change`, `advise`, `act`, `fold`, `brief`, `debrief`,
`map`, `status`, `consult`, and `run`. `ready` SHALL remain as an alias skill
that points at `status`. Each `SKILL.md` SHALL have YAML frontmatter whose `name`
matches the directory.

`.agents/skills/<verb>` SHALL resolve to that same directory (symlink
in this repo) so Grok, Hermes, and Prime load the files without a
plugin install.

#### Scenario: Grok sees the verbs in-repo

- GIVEN a clone of this repo
- WHEN Grok starts in the repo root
- THEN it discovers `intend`, `steer`, `change`, `advise`, `act`,
  `fold`, `brief`, `debrief`, `map`, `status`, `consult`, and `run`
  from `.agents/skills/`

#### Scenario: Claude installs the same files

- GIVEN marketplace entry `intention` → `./plugins/intention`
- WHEN Claude loads the plugin
- THEN it reads `plugins/intention/skills/*/SKILL.md`, which are the
  symlink targets

### Requirement: Marketplaces point at the plugin

`.claude-plugin/marketplace.json` and `.grok-plugin/marketplace.json`
SHALL list plugin `intention` with source `./plugins/intention`.

#### Scenario: Either marketplace index names intention

- GIVEN either index file
- WHEN a reader looks up `intention`
- THEN the source path is `./plugins/intention`

### Requirement: Foreign harnesses get packets

Skill bodies SHALL instruct that Codex, Grok-as-worker, Hermes, and Prime
receive a task packet, never a Claude slash command.

#### Scenario: act on a foreign worker

- GIVEN `act` assigns a node to Codex
- WHEN it dispatches
- THEN the worker is given a packet JSON, not `/act` or `/meta-execute`

### Requirement: MetaDev fork is parked

Forking or extending MetaDev as the *home* of these verbs SHALL NOT be
done until the revive condition in ADR-003 fires. A future overlay SHALL
consume packets from this tree and SHALL NOT grow a second skill tree.

#### Scenario: Someone proposes vendoring MetaDev commands

- GIVEN ADR-003 is accepted
- WHEN a change would copy `plugins/meta-dev/commands/` into this repo
  as the verb surface
- THEN that change is Path B and remains PARKED
