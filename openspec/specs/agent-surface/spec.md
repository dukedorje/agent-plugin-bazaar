# agent-surface

What **is** built: the agent surface from C1 (ADR-001).

This file is a pointer. It does not restate the schema. If a packet, result,
identity, or topology question arises, the living contract is:

- [`docs/contracts/agent-surface.md`](../../../docs/contracts/agent-surface.md)
- [`docs/contracts/identity.md`](../../../docs/contracts/identity.md)
- [`docs/contracts/topologies.md`](../../../docs/contracts/topologies.md)
- [`docs/contracts/agent-surface.schema.json`](../../../docs/contracts/agent-surface.schema.json)

## Purpose

Every actor (human, model, group, later a VM) accepts a task packet and
returns a signed result. A group is an agent whose interior is a topology.

## Requirements

### Requirement: Pointer, not a fork

The system SHALL treat `docs/contracts/` as the normative agent-surface
contract. This spec SHALL NOT contain a second field table. Amendments to
the surface SHALL land as changes that edit `docs/contracts/` and, if
needed, add a one-line note here.

#### Scenario: Packet field lookup

- GIVEN an agent needs the `capability` rule
- WHEN they open this spec
- THEN they follow the link to `docs/contracts/agent-surface.md` rather than
  reading SHALLs copied into this file
