## ADDED Requirements

### Requirement: run conducts a campaign

`run` SHALL walk the ready-set under a stop policy (`--until`,
`--autonomous`, `--pause-before`, `--max-inflight`) and SHALL invoke
stage verbs by reading `plugins/intention/skills/<stage>/SKILL.md` at
the wave it enters that stage. It SHALL NOT inline those skill bodies
into `run/SKILL.md`. It SHALL NOT implement a node except by
dispatching `act`. It SHALL NOT fold except when `--until fold` (or
equivalent) is set and fold is legal. Foreign harnesses SHALL receive
a task packet and SHALL NOT receive `/run`.

`--autonomous` SHALL suppress mid-run questions, route judgment
through consult-before-ask, defer by-eye gates to an EYES list, and
SHALL NOT flip a human-verify box or perform deploy / force-push /
secret-exposing work. A veto or true blocker SHALL park that subject
and SHALL NOT stop unrelated dispatchable nodes unless `--until ask`.

#### Scenario: Until advise

- GIVEN dispatchable write nodes and `--until advise`
- WHEN `run` would next owe a read (`advise`) or an activation
- THEN it stops and reports, and does not flip a PENDING banner

#### Scenario: Autonomous does not forge eyes

- GIVEN `--autonomous` and a node whose acceptance is by-eye
- WHEN that node is reached
- THEN the box stays unchecked, the item is listed under EYES, and
  the run continues elsewhere if anything else is dispatchable

#### Scenario: Foreign worker never sees /run

- GIVEN `run` assigns a node to Codex
- WHEN it dispatches
- THEN Codex is given a packet, not `/run` or `/act`

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`,
`ready`, and `run` SHALL load `plugins/intention/references/shared.md`
and SHALL NOT restate packet fields or topology wirings. Adding a
tenth law to a skill body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`

### Requirement: packet-only gets no slash command

A `surface: packet-only` (or cloud `interface`) prompt SHALL contain
the inlined packet and SHALL NOT contain `/act`, `/intend`,
`/meta-execute`, or `/run`.

#### Scenario: Codex-shaped stage

- GIVEN a packet with `surface: packet-only`
- WHEN `spawn.py stage` writes the prompt
- THEN the prompt has no `/act` and names the packet path
