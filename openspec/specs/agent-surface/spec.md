# agent-surface

What **is** built: the agent surface from C1 (ADR-001).

This file is a pointer. It does not restate the schema. If a packet, result,
identity, or topology question arises, the living contract is:

- [`docs/contracts/agent-surface.md`](../../../docs/contracts/agent-surface.md)
- [`docs/contracts/dispatch.md`](../../../docs/contracts/dispatch.md)
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

### Requirement: Dispatch vocabulary lives next to the surface

The system SHALL treat `docs/contracts/dispatch.md` as the vocabulary
for conductor, worker, consultant, reader, human, and group; for
`density` / `surface` / `consult`; and for persist-at-boundary. This
spec SHALL NOT copy those tables.

#### Scenario: Density lookup

- GIVEN an agent writing a packet
- WHEN they need `lean` vs `explicit`
- THEN they open `docs/contracts/dispatch.md`, not a second table in
  this file

### Requirement: Additive dispatch fields

A task packet MAY set `density` (`lean` · `standard` · `explicit`),
`surface` (`skill-host` · `packet-only`), and `consult`. A signed
result MAY set `distilled` and `raw_ref`. Identity MAY set `interface`.
Absent fields remain valid. Capability order is the inverse of density.

#### Scenario: Old packet still validates

- GIVEN `docs/contracts/examples/solo.packet.json` (no density)
- WHEN `python3 docs/contracts/validate.py` runs
- THEN it passes

#### Scenario: Distilled face disagrees

- GIVEN a result whose `distilled.disposition` differs from
  `disposition`
- WHEN validate runs
- THEN it fails
