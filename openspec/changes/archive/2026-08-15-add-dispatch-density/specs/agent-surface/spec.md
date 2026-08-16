## ADDED Requirements

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
