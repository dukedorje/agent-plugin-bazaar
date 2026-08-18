## ADDED Requirements

### Requirement: The host may persist a paste projection

A host of the agent surface MAY persist parsed paste records
(dossier, emerged intentions, work-node drafts) as a projection of
a successful parse. That projection SHALL NOT become the
authoritative work graph. The dated export remains the source of
work-node edges.

#### Scenario: A mixed paste is accepted

- GIVEN a valid mixed gathering + intend-dag paste
- WHEN the host persists it
- THEN a dossier record and citing intentions are stored
- AND the dated export is unchanged

#### Scenario: Persist proposed as the work graph

- GIVEN a change makes the paste tables the source of `/`
- WHEN it is reviewed
- THEN it is rejected against this requirement

### Requirement: A leftover task table is not the paste store

Persisting a paste SHALL NOT write the leftover `task` table.

#### Scenario: A paste is saved

- GIVEN the host accepts a paste
- WHEN rows are written
- THEN they are not rows of the scaffold `task` table
