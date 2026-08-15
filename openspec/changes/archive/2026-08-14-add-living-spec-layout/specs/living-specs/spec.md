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
    design.md
    specs/<capability>/spec.md
  changes/archive/YYYY-MM-DD-<change-id>/
```

#### Scenario: A stranger finds what is built

- GIVEN the repo at HEAD
- WHEN they open `openspec/specs/`
- THEN each subdirectory is a capability that claims to be true of the
  current system

### Requirement: Specs are truth, changes are not

The system SHALL treat `openspec/specs/<capability>/spec.md` as the only
source of truth for that capability's behavior.

#### Scenario: Search hits a SHALL in a delta

- GIVEN a `SHALL` in `openspec/changes/**/spec.md`
- WHEN an agent cites it as current behavior
- THEN that citation is wrong

### Requirement: Deltas, not rewrites

A change that affects a capability SHALL record `ADDED`, `MODIFIED`, or
`REMOVED` requirements, each with at least one `#### Scenario:`.

#### Scenario: Fold does not drop clauses

- GIVEN a MODIFIED requirement
- WHEN it is folded
- THEN the living spec contains exactly the pasted block

### Requirement: In-file disposition

Every in-flight `proposal.md` SHALL begin with `PENDING`, `ACTIVE BUILD`,
or `PARKED`.

#### Scenario: Path-stripped retrieval still shows status

- GIVEN `proposal.md` without its directory path
- WHEN a reader sees the first banner
- THEN they know draft vs active vs parked

### Requirement: Skip ceremony for restore-only

The system SHALL NOT require a change directory for restore-only, typo,
pin, comment, or tests of existing behavior.

#### Scenario: Typo in a living spec

- GIVEN a misspelling in a living spec
- WHEN an agent fixes it
- THEN they edit the file and do not scaffold `changes/`

### Requirement: Journey or no-new-UI

Every PENDING or ACTIVE BUILD proposal SHALL contain
`## User journey & surfaces` or `No new UI because <reason>`.

#### Scenario: This capability itself

- GIVEN C2 adds no product screen
- WHEN the proposal is written
- THEN it names the file surfaces

### Requirement: Done is fold plus archive

A change SHALL NOT be called done until deltas are folded and the directory
is under `changes/archive/`.

#### Scenario: Shipped-looking change still in changes/

- GIVEN all checkboxes checked and specs updated
- WHEN the change is still in `openspec/changes/<id>/`
- THEN it is not done

### Requirement: Packets cite capabilities

Packets at change, architecture, or instrument rigor SHALL set `capability`
to a living spec id or an id the change is ADDing.

#### Scenario: Architecture packet without a capability

- GIVEN `rigor: architecture` and no `capability`
- WHEN schema validation runs
- THEN it fails

### Requirement: Reasoning docs name change-ids

Reasoning documents SHALL NOT introduce a requirement. Implied work SHALL
name a change-id or `direct fix`.

#### Scenario: Founding DAG

- GIVEN the founding file lists C2
- WHEN C2 is activated
- THEN the landing zone is this change-id
