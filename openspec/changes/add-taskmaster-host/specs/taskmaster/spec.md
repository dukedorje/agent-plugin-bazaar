## ADDED Requirements

### Requirement: Taskmaster is a host of the agent surface

`taskmaster.dev` SHALL be a sibling application that hosts the agent
surface of ADR-001. Its node, assignment, and evidence objects SHALL be
a projection of task-packet-in / signed-result-out. Taskmaster SHALL
NOT define a second object model for actors, packets, or results. If
the hosted product needs a field the surface lacks, the change SHALL
amend `docs/contracts/agent-surface.md` rather than add a parallel
kernel.

#### Scenario: The SaaS needs a field the packet lacks

- GIVEN Taskmaster needs to record something the packet does not carry
- WHEN the change is written
- THEN it edits `docs/contracts/agent-surface.md` and the `agent-surface`
  living spec pointer
- AND it does not introduce a Taskmaster-only packet or result shape

#### Scenario: A group assigns a node

- GIVEN a group is bound to a node in Taskmaster
- WHEN it splits and assigns work
- THEN it does so as an agent whose interior is a topology (ADR-001)
- AND "group" is not a distinct object type in the host

### Requirement: Ready is derived, never stored

The ready set SHALL be computed from edges as `open ∧ all dependencies
landed`. No host SHALL persist a `ready` column, flag, or cached
ready-set as the source of truth.

#### Scenario: Node's last dependency lands

- GIVEN a node is open and its last dependency lands
- WHEN the ready set is next computed
- THEN the node is ready without any write to that node

#### Scenario: Stored ready is proposed

- GIVEN a schema change adds a `ready` column
- WHEN it is reviewed
- THEN it is rejected against this requirement

### Requirement: The host's stack is not a living-spec requirement

Living specs under `openspec/specs/` SHALL NOT contain requirements
naming Taskmaster's web framework, server adapter, database driver,
process topology, deployment mode, or visual tokens. Those decisions
SHALL live in `docs/taskmaster/ARCHITECTURE.md`, which is reasoning and
therefore carries no `SHALL` (ADR-002). Changing the stack SHALL NOT
require a living-spec edit.

#### Scenario: Framework is swapped

- GIVEN Taskmaster changes web framework or server adapter
- WHEN the change lands
- THEN `docs/taskmaster/ARCHITECTURE.md` is amended in place
- AND no file under `openspec/specs/` changes for that reason

#### Scenario: Reader greps the living specs for a framework

- GIVEN a reader searching `openspec/` for Taskmaster's stack
- WHEN they find nothing
- THEN they follow ADR-006 to `docs/taskmaster/ARCHITECTURE.md` in one hop

### Requirement: The capability is materialized by fold

The `taskmaster` capability SHALL exist under `openspec/specs/` only
after `add-taskmaster-host` folds. Until then these requirements SHALL
remain a delta in `openspec/changes/`, describing what is decided, not
what is running.

#### Scenario: Change is still in flight

- GIVEN `add-taskmaster-host` has not been folded
- WHEN an agent resolves the `taskmaster` capability id
- THEN it resolves as a capability a change is ADDing, not as built
  behavior (ADR-002)
