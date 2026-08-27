# update-run-ask

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-27 (chat: make --until ask a roll that stops).

## Why

`--until ask` is a stop face with no walk and no ASK source, so it
never stops for a question and never rolls. Duke wants two
campaigns, one walk: stop at the first elicitation, or keep going
and keep a morning list.

## What

- `--until ask` uses the `--until roll` table.
- Stop on the first elicitation: raised ASK, PENDING, or by-eye /
  EYES / human-verify open box.
- `--until roll` does not stop; it keeps those ids on the card
  `ask` list and continues siblings.
- A stage raises ASK by listing it on the observe JSON `ask`
  field, or by an open owed box matching ASK / EYES / by-eye /
  human-verify. No new verb. No fourth store.
- `run.py` still launches zero workers.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat.

1. `/run --until ask` — roll until something needs him; halt.
2. `/run --until roll` — roll as long as possible; morning list
   on the card.
3. **Empty** — nothing dispatchable and nothing to ask.
4. **Off** — ask never fires (today’s hole).

`No new UI because` `/run` and `run.py`.

## Out of scope

- `/ask` or `/inbox` as a verb
- Flipping PENDING
- Making debrief a wave
