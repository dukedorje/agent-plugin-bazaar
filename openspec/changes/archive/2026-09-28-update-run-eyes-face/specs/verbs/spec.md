## MODIFIED Requirements

### Requirement: until ask is a roll that stops on elicitation

`--until ask` SHALL use the same observe table as `--until roll`.
It SHALL stop (`next` null) on the first elicitation: PENDING →
`stop: ask`; an ASK box → `stop: ask`; an open owed box matching
EYES / by-eye / human-verify → `stop: eyes`. A stage SHALL raise
an elicitation on that face (JSON `ask` / `eyes`, or such an owed
box). The `eyes` halt SHALL print YOUR EYES and a Next command
taken from `Next: …` on the box (else `/status`). It SHALL NOT
invent an `/ask` verb or a fourth store.

`--until roll` SHALL not stop on ASK or PENDING. It SHALL keep
those ids on the card and SHALL continue unrelated dispatchable
work. It SHALL halt with `stop: eyes` when the pick is an EYES
id, leftover beads would skip past a look, or the board is
otherwise empty with EYES still open. It SHALL NOT flip PENDING
or by-eye boxes.

#### Scenario: Ask stops while work remains

- GIVEN `--until ask`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask` (or activation-class)
- AND `next` is not `act`

#### Scenario: Ask without elicitation rolls

- GIVEN `--until ask`, no PENDING, no ask ids, and an unblocked
  bead titled `add-tatastu-host: …` with no change dir
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-tatastu-host`

#### Scenario: Roll keeps the morning list

- GIVEN `--until roll`, PENDING `add-y`, and READY `add-x`
- WHEN `run.py` observes
- THEN `next` is `act` and `focus` is `add-x`
- AND `add-y` is listed under `ask` or `waiting`

#### Scenario: Wait on EYES is stop eyes

- GIVEN `--until ask` and an open EYES box on `add-x`, no PENDING
- WHEN `run.py` observes
- THEN `stop` is `eyes` and `next` is null
- AND the card names YOUR EYES and a Next command

#### Scenario: Roll does not skip past EYES into leftover beads

- GIVEN `--until roll`, an open EYES box on `add-x`, and an
  unblocked leftover task bead
- WHEN `run.py` observes
- THEN `stop` is `eyes` and `next` is not `intend`
