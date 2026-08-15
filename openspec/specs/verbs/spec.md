# verbs

What each dispatcher must produce. Folded from `deepen-verbs` on
2026-08-15 (S1–S4). Hosting is `packaging`. The agent surface is
`docs/contracts/`. This spec does not duplicate either.

## Purpose

`intend`, `change`, `act`, and `fold` are complementary. They share
`plugins/intention/references/shared.md`. None redefines the packet.

## ADDED Requirements

### Requirement: intend emits a DAG

`intend` SHALL observe living specs, in-flight changes, and learnings,
orient (load class × blast × lifecycle), and emit a DAG of nodes whose
landings are a verb-led change-id, `brief`, or `direct fix`. It SHALL NOT
implement, write SHALLs, or create `docs/sprints/`. Restore-only work
SHALL stop at `direct fix`.

#### Scenario: A goal becomes named landings

- GIVEN an intention that needs new behavior
- WHEN `intend` finishes
- THEN the ready-set names change-ids (or brief / direct fix), each with
  one acceptance surface, and no code has been written for architecture
  nodes that still need activation

### Requirement: change scaffolds OpenSpec-lite

`change` SHALL write `openspec/changes/<id>/{proposal,tasks}.md` and
delta specs. `proposal.md` SHALL start with `PENDING` or `ACTIVE BUILD`
and SHALL include a journey or `No new UI because <reason>`. It SHALL
skip scaffolding for restore-only work. It SHALL NOT fold.

#### Scenario: New behavior gets a PENDING change

- GIVEN a change-id from `intend`
- WHEN `change` runs and the human has not activated
- THEN `openspec/changes/<id>/proposal.md` exists with `> **PENDING**`
  and a journey section

### Requirement: act uses packets

`act` SHALL write a task packet and a signed result (solo under
`.omc/act/`, groups under `groups/<id>/`). Foreign harnesses SHALL
receive that packet, never a slash command. Edits SHALL commit-on-red
on exact paths. Focused verify SHALL be the only task gate.

#### Scenario: Codex is assigned a node

- GIVEN `act` routes a node to Codex
- WHEN it dispatches
- THEN Codex is given `.omc/act/<node>.packet.json` or
  `groups/<id>/packet.json`, not `/act`

### Requirement: fold archives

`fold` SHALL apply deltas to `openspec/specs/`, move the change to
`openspec/changes/archive/YYYY-MM-DD-<id>/`, amend `ARCHITECTURE.md`
when shape changed, and append surprises to `docs/LEARNINGS.md`. It
SHALL refuse PENDING and PARKED.

#### Scenario: Active change after act

- GIVEN `openspec/changes/<id>/` is ACTIVE BUILD and owed tasks are done
- WHEN `fold` finishes
- THEN `openspec/changes/<id>/` is gone, the archive directory exists,
  and every SHALL from the deltas appears in `openspec/specs/`

### Requirement: Shared references, not four surfaces

The four skills SHALL load `plugins/intention/references/shared.md` and
SHALL NOT restate packet fields or topology wirings. Adding a tenth law
to a skill body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a second
  field table inside `act/SKILL.md`
