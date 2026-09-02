## MODIFIED Requirements

### Requirement: run gate defaults

`--until roll` SHALL be the default walk: fold-legal inflight →
send-back amend → advise → act → bead landing/`change` → leftover
task/`intend`. It SHALL park ASK / EYES / PENDING on the card `ask`
list and SHALL continue unrelated dispatchable work. It SHALL NOT
stop on elicitation. It SHALL NOT flip PENDING or by-eye boxes.

`--until empty` SHALL be the cautious walk: `change` → `advise` →
`act`. It SHALL stop at PENDING, ASK, and fold. It SHALL NOT emit
`next: fold`. It SHALL NOT emit `next: intend` unless the scope
fails the verb-led change-id detector named by `update-run-ooda`
(`^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$`).

`--until fold` SHALL use that same change's legal-fold predicate
(ACTIVE BUILD, no open owed checkbox, not PARKED). It SHALL NOT
define a second fold rule. Unscoped `--until fold` SHALL scan
inflight for that predicate. `--until advise`, `--until activation`,
and `--until ask` SHALL keep their existing stop meanings.

`--autonomous` SHALL suppress mid-run questions and SHALL NOT flip
PENDING or by-eye boxes. Alone it SHALL use the default walk
(`--until roll`). Combined with an explicit `--until` it SHALL use
that walk. It SHALL NOT deploy.

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

#### Scenario: Until fold cites ooda's legal-fold predicate

- GIVEN `--until fold` and a change that is ACTIVE BUILD, has no
  open owed checkbox, and is not PARKED
- WHEN `run.py` observes
- THEN fold is legal under the predicate `update-run-ooda` named
- AND this requirement does not invent a second predicate

#### Scenario: Autonomous does not flip PENDING

- GIVEN `--autonomous` and a PENDING change
- WHEN `run` would next owe activation
- THEN the banner stays PENDING
- AND `next` is not `act`

#### Scenario: Bare run uses the roll table

- GIVEN no `--until` and `openspec/changes/add-x/` is fold-legal
- WHEN `run.py` observes unscoped
- THEN `next` is `fold` and `focus` is `add-x`
