## ADDED Requirements

### Requirement: In-flight banners

The hygiene check SHALL fail a change whose proposal.md has no
PENDING|ACTIVE BUILD|PARKED banner in the first 40 lines.

#### Scenario: Path is not status

- GIVEN no banner
- WHEN the check runs
- THEN non-zero exit

### Requirement: Fold-debt is empty

ACTIVE BUILD with no open owed checkbox (including missing or prose-only
tasks.md) SHALL fail. PENDING fails only when owed boxes exist and are
all [x]. Allowlist empty.

#### Scenario: Shipped-looking change

- GIVEN all owed boxes checked in-flight
- WHEN the check runs
- THEN non-zero exit

#### Scenario: Lie by omission

- GIVEN ACTIVE BUILD and no tasks.md
- WHEN the check runs
- THEN non-zero exit

### Requirement: Journey or no-new-UI

PENDING/ACTIVE SHALL fail without a journey heading or No new UI because.

#### Scenario: Active proposal with neither

- GIVEN ACTIVE BUILD and no journey
- WHEN the check runs
- THEN non-zero exit

### Requirement: Checkboxes are owed

Out-of-scope / handoff / stall boxes SHALL fail.

#### Scenario: Out-of-scope as a box

- GIVEN a box under Out of scope
- WHEN the check runs
- THEN non-zero exit

### Requirement: Discriminating fixtures

test-hygiene.sh SHALL fail the bad fixtures and pass the live tree.

#### Scenario: A broken check still greens the live tree

- GIVEN a fold-debt regression
- WHEN test-hygiene.sh runs
- THEN the fold-debt fixture fails
