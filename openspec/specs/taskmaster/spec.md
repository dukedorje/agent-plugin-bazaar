# taskmaster

What **is** built: Taskmaster is a sibling host of the agent surface
(ADR-006). Folded from `add-taskmaster-host` on 2026-08-16.

This spec is stack-neutral. Framework, adapter, database, process
topology, and look tokens live in the sibling app
(`~/work/Taskmaster/taskmaster-web/docs/ARCHITECTURE.md`; hop:
[`docs/taskmaster/ARCHITECTURE.md`](../../../docs/taskmaster/ARCHITECTURE.md))
and are not requirements here.

## Purpose

`taskmaster.dev` hosts the agent surface. Node, assignment, and
evidence are a projection of packet-in / result-out. The ready set is
derived from edges.

## Requirements

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
SHALL live in the sibling app's architecture sketch
(`~/work/Taskmaster/taskmaster-web/docs/ARCHITECTURE.md`), which is
reasoning and therefore carries no `SHALL` (ADR-002). This marketplace
SHALL keep a hop at `docs/taskmaster/ARCHITECTURE.md`. Changing the
stack SHALL NOT require a living-spec edit.

#### Scenario: Framework is swapped

- GIVEN Taskmaster changes web framework or server adapter
- WHEN the change lands
- THEN the sibling app's `docs/ARCHITECTURE.md` is amended in place
- AND no file under `openspec/specs/` changes for that reason

#### Scenario: Reader greps the living specs for a framework

- GIVEN a reader searching `openspec/` for Taskmaster's stack
- WHEN they find nothing
- THEN they follow ADR-006 to `docs/taskmaster/ARCHITECTURE.md` and
  from there to the sibling sketch in one hop

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
