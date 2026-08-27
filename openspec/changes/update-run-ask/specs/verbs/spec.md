## ADDED Requirements

### Requirement: until ask is a roll that stops on elicitation

`--until ask` SHALL use the same observe table as `--until roll`.
It SHALL stop (`stop: ask`, `next` null) on the first elicitation:
an `ask` id on the observe face, a PENDING change, or an open owed
box matching ASK / EYES / by-eye / human-verify. A stage SHALL
raise an elicitation on that face (JSON `ask`, or such an owed
box). It SHALL NOT invent an `/ask` verb or a fourth store.

`--until roll` SHALL not stop on elicitation. It SHALL keep those
ids on the card `ask` list and SHALL continue unrelated
dispatchable work. It SHALL NOT flip PENDING or by-eye boxes.

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
