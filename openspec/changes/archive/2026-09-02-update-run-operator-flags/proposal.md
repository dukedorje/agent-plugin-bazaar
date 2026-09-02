# update-run-operator-flags

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-09-02 (steer: mailbox on ready; collapse until;
kill autonomous).

## Why

`--until` mixed walk and stop. The morning ASK/EYES pile only
appeared as a side effect of picking a campaign walk. `--until ask`
and the `--ask` gate share a word and mean opposites. `--autonomous`
was manners that used to change the walk.

Steer 2026-09-02: pile on `/ready`; operator flags `--interrupt` /
`--only fold` / `--no-fold`; kill `--autonomous`.

## What

- `ready` grows ASK / EYES / PUNT faces. EYES boxes are not READY.
- `/run --interrupt` = today's `--until ask` (roll walk, halt at
  first elicitation).
- `/run --only fold` = `--until fold`.
- `/run --no-fold --no-beads` = `--until empty`.
- `--until *` stays as aliases for one release (`roll` is a no-op).
- `--autonomous` is accepted and ignored (warn). Desk vs walk-away
  is `--interrupt` vs bare `/run`.
- `--advise` gate walks all owed reads, never acts.

## Impact

- Capabilities: MODIFIED `verbs` · `living-specs` (ready list)
- ADRs: none

## User journey & surfaces

Duke, from chat.

1. `/ready` — morning pile including ASK / EYES / PUNT.
2. `/run` — walk away (roll).
3. `/run --interrupt` — at the desk; halt at first ASK/PENDING/EYES.
4. **Off** — `/run --until roll` to *look* at the pile.

`No new UI because` `/ready`, `/run`, and the two skill scripts.

## Out of scope

- Persisting `--punt` to a fourth store (`openspec/punted.md`)
- `--no-deploy` as its own flag (never-deploy stays must-not)
- Flipping PENDING
