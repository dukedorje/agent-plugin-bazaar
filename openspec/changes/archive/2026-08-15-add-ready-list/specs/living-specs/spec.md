## ADDED Requirements

### Requirement: Ready-set is queryable

`python3 scripts/ready.py` SHALL list ACTIVE BUILD + open owed work as
ready, PENDING as needs-activation, and PARKED banners plus
`openspec/parked.md` as parked.

#### Scenario: Ask what is ready

- GIVEN one ACTIVE BUILD change with an open owed checkbox
- WHEN `scripts/ready.py --json` runs
- THEN that id is in `ready` and not in `parked`
