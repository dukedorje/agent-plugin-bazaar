## MODIFIED Requirements

### Requirement: run conducts a campaign

`run` SHALL walk the ready-set under a stop policy (`--until`,
`--autonomous`, `--pause-before`, `--max-inflight`) and SHALL invoke
stage verbs by reading `plugins/intention/skills/<stage>/SKILL.md` at
the wave it enters that stage. It SHALL accept an optional scope.
It SHALL set `next` from this decision table (not a preference
order). A **verb-led change-id** is a kebab matching
`^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$`. Any
other scope SHALL be a **goal**.

- `intend` when the scope is a goal, or when a surprise needs a
  new Observe
- `change` when the scope is a verb-led change-id that has no
  `openspec/changes/<id>/` directory
- `advise` when that change is ACTIVE BUILD architecture/instrument
  with no accepting review
- `act` when the change is dispatchable write work
- `fold` when `--until fold` (or equivalent) is set and fold is
  legal: banner `ACTIVE BUILD`, no open owed checkbox, not
  `PARKED`

`ready` SHALL remain the card's observe, not a `next` stage.
`brief` SHALL remain disposable and SHALL NOT be a campaign stage.

It SHALL NOT inline those skill bodies into `run/SKILL.md`. It SHALL
NOT implement a node except by dispatching `act`. It SHALL NOT fold
except when `--until fold` (or equivalent) is set and fold is legal.
It SHALL NOT flip a PENDING banner. Foreign harnesses SHALL receive
a task packet and SHALL NOT receive `/run`. `workers_launched` SHALL
stay 0.

`stop: no-ready` SHALL mean the observe script is missing. A missing
`openspec/` tree with a named verb-led change-id SHALL be
`next: change`, not `no-ready`. A missing `openspec/` tree with a
goal that is not a change-id SHALL be `next: intend`, not
`no-ready`.

`--until advise` SHALL dispatch `next: advise` when a read is owed
and SHALL NOT dispatch `act`. `--until activation` SHALL stop on
PENDING. `--until empty` SHALL walk change → advise → act until
nothing is dispatchable.

`--autonomous` SHALL suppress mid-run questions, route judgment
through consult-before-ask, defer by-eye gates to an EYES list, and
SHALL NOT flip a human-verify box or perform deploy / force-push /
secret-exposing work. A veto or true blocker SHALL park that subject
and SHALL NOT stop unrelated dispatchable nodes unless `--until ask`.

#### Scenario: Named landing has no change directory

- GIVEN `/run add-sheaf-type` and no `openspec/changes/add-sheaf-type/`
- WHEN `run.py` observes
- THEN the card has `next: change` and `focus: add-sheaf-type`
- AND `stop` is not `no-ready`

#### Scenario: Goal is not a change-id

- GIVEN `/run we need extract-from on intend` and that string is
  not a verb-led change-id
- WHEN `run.py` observes
- THEN the card has `next: intend`
- AND `workers_launched` is 0

#### Scenario: Until fold when fold is legal

- GIVEN `--until fold` and an ACTIVE BUILD change whose owed boxes
  are checked
- WHEN `run.py` observes
- THEN the card has `next: fold`
- AND no worker is launched

#### Scenario: Architecture owes a read before a write

- GIVEN `add-x` is ACTIVE BUILD, in `needs_advise`, and also has
  open owed boxes
- WHEN `run` observes with `--until empty`
- THEN `next` is `advise`, not `act`

#### Scenario: Until advise runs the read and not the write

- GIVEN dispatchable write nodes and `--until advise`
- WHEN a read is owed
- THEN `next` is `advise` and no PENDING banner is flipped
- AND `act` is not dispatched

#### Scenario: Until advise with no read owed

- GIVEN ready write nodes, no `needs_advise`, and `--until advise`
- WHEN `run` observes
- THEN it stops and does not set `next: act`

#### Scenario: Autonomous does not forge eyes

- GIVEN `--autonomous` and a node whose acceptance is by-eye
- WHEN that node is reached
- THEN the box stays unchecked, the item is listed under EYES, and
  the run continues elsewhere if anything else is dispatchable

#### Scenario: Foreign worker never sees /run

- GIVEN `run` assigns a node to Codex
- WHEN it dispatches
- THEN Codex is given a packet, not `/run` or `/act`
