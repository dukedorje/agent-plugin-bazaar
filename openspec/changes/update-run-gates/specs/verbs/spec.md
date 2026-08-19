## ADDED Requirements

### Requirement: run gate defaults

`--until empty` SHALL be the default walk: `change` → `advise` →
`act`. It SHALL stop at PENDING, ASK, and fold. It SHALL NOT emit
`next: fold`. It SHALL NOT emit `next: intend` unless the scope is
a goal (not a verb-led change-id).

`--until fold` SHALL emit `next: fold` after writes when fold is
legal. `--until advise`, `--until activation`, and `--until ask`
SHALL keep their existing stop meanings.

`--autonomous` SHALL use the same walk as `--until empty`. It SHALL
NOT flip a PENDING banner or a by-eye box. It SHALL NOT deploy.

#### Scenario: Empty does not fold

- GIVEN `--until empty` and an ACTIVE BUILD change whose owed boxes
  are checked
- WHEN `run.py` observes
- THEN `next` is not `fold`
- AND the card stops empty if nothing else is dispatchable

#### Scenario: Empty does not intend a change-id

- GIVEN `--until empty` and scope `add-x` which is a verb-led
  change-id
- WHEN `run.py` observes
- THEN `next` is not `intend`

#### Scenario: Until fold emits fold when legal

- GIVEN `--until fold` and fold is legal
- WHEN `run.py` observes
- THEN the card has `next: fold`

#### Scenario: Autonomous does not flip PENDING

- GIVEN `--autonomous` and a PENDING change
- WHEN `run` would next owe activation
- THEN the banner stays PENDING
- AND `next` is not `act`
