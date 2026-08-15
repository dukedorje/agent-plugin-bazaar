## ADDED Requirements

### Requirement: intend emits a DAG

`intend` SHALL emit a DAG of change-id / brief / direct-fix nodes and
SHALL NOT implement or write SHALLs.

#### Scenario: A goal becomes named landings

- GIVEN an intention that needs new behavior
- WHEN `intend` finishes
- THEN the ready-set names landings and architecture nodes are not
  implemented before activation

### Requirement: change scaffolds OpenSpec-lite

`change` SHALL write a bannered proposal, tasks, and deltas, and SHALL
NOT fold.

#### Scenario: New behavior gets a PENDING change

- GIVEN a change-id and no activation
- WHEN `change` runs
- THEN `proposal.md` has `> **PENDING**` and a journey

### Requirement: act uses packets

`act` SHALL write a packet and signed result. Foreign harnesses SHALL
get the packet, never a slash command.

#### Scenario: Codex is assigned a node

- GIVEN a Codex assignee
- WHEN `act` dispatches
- THEN the worker receives packet JSON

### Requirement: fold archives

`fold` SHALL fold deltas, archive the change, and refuse PENDING/PARKED.

#### Scenario: Active change after act

- GIVEN an ACTIVE BUILD change with owed work done
- WHEN `fold` finishes
- THEN the live change dir is gone and specs carry the SHALLs

### Requirement: Shared references, not four surfaces

The four skills SHALL load `shared.md` and SHALL NOT restate the packet.

#### Scenario: Packet field lookup

- GIVEN `act` needs `capability`
- WHEN the skill is followed
- THEN the reader is sent to `docs/contracts/agent-surface.md`
