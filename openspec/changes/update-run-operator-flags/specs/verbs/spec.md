## ADDED Requirements

### Requirement: run operator flags

Bare `/run` SHALL use the roll walk. `--interrupt` SHALL use that
same walk and SHALL stop at the first elicitation (ASK box, PENDING,
EYES / by-eye / human-verify). `--only fold` SHALL scan fold-legal
inflight and SHALL not `act`. `--no-fold` SHALL skip fold picks.
`--no-beads` SHALL skip bead landing and leftover intend. Combined
`--no-fold --no-beads` SHALL match `--until empty`. `--until` tokens
SHALL remain aliases for one release (`roll` is a no-op for the
default). `--autonomous` SHALL NOT change the walk. `--until
activation` SHALL NOT be required; PENDING is an elicitation.

#### Scenario: Interrupt stops while work remains

- GIVEN `--interrupt`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask`
- AND `next` is not `act`

#### Scenario: Only fold

- GIVEN `--only fold`, no scope, and fold-legal `add-x`
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`

#### Scenario: No-fold no-beads is empty walk

- GIVEN `--no-fold --no-beads` and fold-legal `add-x` with no other
  dispatchable work
- WHEN `run.py` observes
- THEN `next` is not `fold`
