## ADDED Requirements

### Requirement: run roll walks while unblocked

`--until roll` SHALL observe openspec banners and unblocked beads
and SHALL set `next` from this table, first match wins:

1. fold-legal inflight change (no scope required) → `fold`
2. last advise is `send-back` on an ACTIVE BUILD change → `change`
3. `needs_advise` → `advise`
4. READY write → `act`
5. unblocked bead whose title names a verb-led change-id and that
   directory does not exist → `change`
6. unblocked task or feature bead with no verb-led landing, that
   is not an epic and whose title does not start with `nod-` →
   `intend` (focus is that bead id)
7. else stop empty

It SHALL NOT intend epics. It SHALL NOT flip PENDING. Epics and
`nod-` titles SHALL NOT auto-intend. `workers_launched` SHALL stay 0.

Unscoped `--until fold` SHALL scan inflight for fold-legal and
SHALL set `next: fold` on the first hit.

#### Scenario: Unscoped fold finds a legal change

- GIVEN `--until fold` or `--until roll`, no scope, and
  `openspec/changes/add-x/` is fold-legal
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`

#### Scenario: Send-back is amend not act

- GIVEN `--until roll` and `add-x` is ACTIVE BUILD whose last
  advise is `send-back`, and `add-x` is also READY
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-x`

#### Scenario: Bead landing with no change dir

- GIVEN `--until roll`, no READY writes, and an unblocked bead
  titled `add-tatastu-host: …` with no `openspec/changes/add-tatastu-host/`
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-tatastu-host`

#### Scenario: Epic does not auto-intend

- GIVEN `--until roll` and the only unblocked bead is an epic
- WHEN `run.py` observes
- THEN `next` is not `intend`

## MODIFIED Requirements

### Requirement: run gate defaults

`--until empty` SHALL be the default walk: `change` → `advise` →
`act`. It SHALL stop at PENDING, ASK, and fold. It SHALL NOT emit
`next: fold`. It SHALL NOT emit `next: intend` unless the scope
fails the verb-led change-id detector named by `update-run-ooda`
(`^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$`).

`--until fold` SHALL use that same change's legal-fold predicate
(ACTIVE BUILD, no open owed checkbox, not PARKED). It SHALL NOT
define a second fold rule. Unscoped `--until fold` SHALL scan
inflight for that predicate. `--until roll` SHALL use the roll
table. `--until advise`, `--until activation`, and `--until ask`
SHALL keep their existing stop meanings.

`--autonomous` SHALL suppress mid-run questions and SHALL NOT flip
PENDING or by-eye boxes. Combined with `--until roll` it SHALL use
the roll table. Alone it SHALL use the same walk as `--until empty`.
It SHALL NOT deploy.

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
