## MODIFIED Requirements

### Requirement: Ready-set is queryable

`python3 scripts/status.py` (or `scripts/ready.py`, a shim) SHALL list
ACTIVE BUILD changes whose open owed boxes are implement work as
ready, PENDING as needs-activation, PARKED (in-flight banners plus
`openspec/parked.md`) as parked, and the morning mailbox as ASK /
EYES / PUNT. An open owed box matching EYES / by-eye / human-verify
SHALL appear under EYES and SHALL NOT by itself make the change
READY.

#### Scenario: Ask what is ready

- GIVEN one ACTIVE BUILD change with an open owed checkbox that is
  not ASK / EYES / PUNT
- WHEN `scripts/status.py --json` runs
- THEN that change-id is in `ready` and not in `parked`

#### Scenario: Eyes is not ready

- GIVEN one ACTIVE BUILD change whose only open owed box matches
  EYES
- WHEN `scripts/status.py --json` runs
- THEN that change-id is in `eyes` and not in `ready`
