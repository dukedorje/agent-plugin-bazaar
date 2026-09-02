## ADDED Requirements

### Requirement: wait and tidy are the operator names

`--wait` SHALL be desk mode: the roll walk, stopping at the first
elicitation. `--tidy` SHALL scan fold-legal inflight and SHALL not
`act`. `--interrupt` SHALL be an alias of `--wait`. `--only fold`
SHALL be an alias of `--tidy`. The observe verb SHALL be `status`.
`ready` SHALL remain an alias of `status`.

#### Scenario: Wait stops while work remains

- GIVEN `--wait`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask`
- AND `next` is not `act`

#### Scenario: Tidy is fold-only

- GIVEN `--tidy`, no scope, and fold-legal `add-x`
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`
