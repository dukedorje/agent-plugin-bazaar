## ADDED Requirements

### Requirement: A host sources edges from an export and states their age

A host of the agent surface SHALL obtain its edge set from an exported
snapshot of the kernel tracker, taken at deploy time. It SHALL NOT depend on
a live kernel service to render its ready set, and SHALL NOT hold
authoritative work state of its own.

Wherever a host presents a ready set, it SHALL state when the snapshot it is
deriving from was taken. A host SHALL NOT present a derived ready set whose
age it cannot state.

If the snapshot is absent, unparseable, or carries no generation time, the
host SHALL render the ready set empty and say why. It SHALL NOT fall back to
a seeded, vendored, or previously-cached graph.

#### Scenario: The snapshot is old

- GIVEN the exported snapshot was taken some hours ago
- WHEN a reader loads the ready set
- THEN the derived ready set is shown
- AND the page states the time the snapshot was taken
- AND the host does not describe the graph as current

#### Scenario: The snapshot is missing or unreadable

- GIVEN the export is absent, malformed, or has no generation time
- WHEN the host renders
- THEN the ready set is empty and the reason is stated
- AND no seeded or stale graph is presented in its place

#### Scenario: A host wants fresher data

- GIVEN someone wants the ready set to update without a deploy
- WHEN that is proposed
- THEN it is a change to the delivery of the same exported document
- AND it does not move authoritative work state into the host
- AND it does not introduce a `ready` field into the exchanged document

#### Scenario: The export references work it did not include

- GIVEN a node depends on an id that is not in the exported node set
- WHEN the export is produced
- THEN that edge is omitted rather than exported dangling
- AND the host's derivation therefore never resolves against a missing node
