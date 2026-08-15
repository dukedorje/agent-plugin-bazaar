# living-specs

Living truth for how this repo stores what **is** built and what **should**
change. Folded from `add-living-spec-layout` on 2026-08-14 (C2).

A `SHALL` in this file is evidence of intended current behavior of the
process. A `SHALL` in `openspec/changes/` (including `archive/`) is not.

## Purpose

Agents and humans can tell current from in-flight without a call, and can
cite a capability from a task packet.

## ADDED Requirements

### Requirement: Two-layer tree

The project SHALL keep process memory in this tree:

```
openspec/
  project.md
  AGENTS.md
  specs/<capability>/spec.md
  changes/<change-id>/
    proposal.md
    tasks.md
    design.md          # optional
    specs/<capability>/spec.md   # deltas
  changes/archive/YYYY-MM-DD-<change-id>/
```

Capability ids SHALL be kebab-case directory names. Change ids SHALL be
verb-led kebab-case (`add-`, `update-`, `remove-`, `refactor-`).

#### Scenario: A stranger finds what is built

- GIVEN the repo at HEAD
- WHEN they open `openspec/specs/`
- THEN each subdirectory is a capability that claims to be true of the
  current system, and `spec.md` is the only file they must read for that
  claim

#### Scenario: A stranger finds what is in flight

- GIVEN one or more directories under `openspec/changes/` other than `archive/`
- WHEN they open each `proposal.md`
- THEN the first banner line is `PENDING`, `ACTIVE BUILD`, or `PARKED`, and
  they do not treat the directory name as status

### Requirement: Specs are truth, changes are not

The system SHALL treat `openspec/specs/<capability>/spec.md` as the only
source of truth for that capability's behavior. Presence of a matching
filename under `changes/` SHALL NOT be treated as evidence the behavior
exists.

#### Scenario: Search hits a SHALL in a delta

- GIVEN a `SHALL` sentence in `openspec/changes/**/spec.md`
- WHEN an agent cites it as current behavior
- THEN that citation is wrong; the agent MUST open the living spec (or
  report that the requirement is not yet folded)

### Requirement: Deltas, not rewrites

A change that affects a capability SHALL record the effect as `ADDED`,
`MODIFIED`, or `REMOVED` requirements. Each requirement SHALL include at
least one `#### Scenario:`. A `MODIFIED` requirement SHALL paste the entire
requirement block; fold replaces that block wholesale.

#### Scenario: Fold does not drop clauses

- GIVEN a living requirement with two scenarios
- WHEN a change MODIFIES it and omits one scenario
- THEN fold leaves only what the change pasted — so the change MUST paste
  both unless the omitted scenario is intentionally gone

### Requirement: In-file disposition

Every in-flight `proposal.md` SHALL begin its body with a disposition
banner: `> **PENDING**`, `> **ACTIVE BUILD**`, or
`> **PARKED** — revive when <condition>`.

Agents SHALL draft at `PENDING`. Humans SHALL set `ACTIVE BUILD` to
activate (including by saying "activate <id>" in chat). A `PARKED` change
SHALL NOT be implemented, extended, or counted in the ready-set.

#### Scenario: Path-stripped retrieval still shows status

- GIVEN a chunker that returns `proposal.md` body without the directory path
- WHEN a reader sees the first banner
- THEN they can tell whether the change is draft, active, or parked

### Requirement: Skip ceremony for restore-only

The system SHALL NOT require a change directory for work that only restores
already-specced behavior, or that is a typo, formatting, comment, non-breaking
pin, or a test for existing behavior.

#### Scenario: Typo in a living spec

- GIVEN a misspelling in `openspec/specs/living-specs/spec.md`
- WHEN an agent fixes it
- THEN they edit the file directly and do not scaffold `changes/`

### Requirement: Journey or no-new-UI

Every `PENDING` or `ACTIVE BUILD` proposal SHALL contain
`## User journey & surfaces` describing who, from which existing surface,
working / empty / failed / off — or the explicit sentence
`No new UI because <reason>` naming the surface the outcome already reaches.

#### Scenario: This capability itself

- GIVEN C2 adds no product screen
- WHEN the proposal is written
- THEN it says `No new UI because` the surfaces are `openspec/specs/` and
  `openspec/changes/*/proposal.md`

### Requirement: Done is fold plus archive

A change SHALL NOT be called done when its code or docs have landed but its
deltas remain unfolder or its directory remains under `changes/` outside
`archive/`. Fold SHALL write the resulting requirements into
`openspec/specs/<capability>/spec.md`. Archive SHALL move the change to
`openspec/changes/archive/YYYY-MM-DD-<change-id>/`.

Checkboxes SHALL represent work this change owes. Out-of-scope, findings,
and handoffs SHALL be bullets.

#### Scenario: Shipped-looking change still in changes/

- GIVEN every task checkbox is checked and the living spec already contains
  the new requirements
- WHEN the change directory is still `openspec/changes/<id>/`
- THEN the change is not done; it MUST be moved to `archive/`

### Requirement: Packets cite capabilities

A task packet with rigor `change`, `architecture`, or `instrument` SHALL set
`capability` to a kebab-case id that is either an existing
`openspec/specs/<id>/` directory or an id the packet's change is ADDing.
Packets at `vibe` or `brief` rigor MAY omit `capability`.

The living spec for `agent-surface` SHALL remain a pointer to
`docs/contracts/`; process SHALLs SHALL NOT duplicate that schema.

#### Scenario: Architecture packet without a capability

- GIVEN a packet with `rigor: architecture` and no `capability` field
- WHEN `docs/contracts/validate.py` runs against it
- THEN validation fails

#### Scenario: C1 schema is not recopied

- GIVEN `openspec/specs/agent-surface/spec.md`
- WHEN a reader wants the packet field list
- THEN they are sent to `docs/contracts/agent-surface.md` and the JSON schema,
  not to a second field table in this tree

### Requirement: Reasoning docs name change-ids

`docs/`, `ARCHITECTURE.md`, and `openspec/project.md` SHALL NOT introduce a
requirement. If they imply work, they SHALL name the landing change-id (or
`direct fix`).

#### Scenario: Founding DAG

- GIVEN `docs/from-intention-to-running.md` lists C2
- WHEN C2 is activated
- THEN the landing zone is `add-living-spec-layout`, not new SHALLs in that
  founding file
