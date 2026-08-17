## ADDED Requirements

### Requirement: The kernel emits the snapshot the host consumes

This marketplace SHALL produce the exported snapshot named by
`A host sources edges from an export and states their age`. The
document SHALL include `generated_at` (ISO-8601 UTC) and SHALL NOT
include a `ready` field. Closed work SHALL be `landed`; deferred and
parked work SHALL be omitted. A `needs` id that is not in `nodes`
SHALL be omitted.

The snapshot shape is the contract in
`openspec/changes/archive/2026-08-16-add-taskmaster-edge-source/design.md`.

#### Scenario: Export after a close

- GIVEN bead `bazaar-lgr.3` is closed in `bd`
- WHEN the export script runs
- THEN that id appears as `state: landed` or is absent if omitted as
  non-open
- AND no `ready` key exists on the document or any node

#### Scenario: Dangling dependency

- GIVEN an open node needs an id that was omitted (parked or missing)
- WHEN the export is produced
- THEN that need is not present in `needs`
- AND `generated_at` is still set
