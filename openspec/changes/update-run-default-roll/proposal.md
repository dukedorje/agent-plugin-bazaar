# update-run-default-roll

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-09-02 (chat: make --until roll the default).

## Why

`--until empty` is the default walk, so `/run` will not fold, will not
pick leftover beads, and stops at ASK. Duke’s actual campaign is
`--until roll`. An operator should not have to name the long walk
every morning. `--autonomous` alone still used the empty walk, so
“go autonomous” was *less* of a campaign than a named roll.

## What

- `run.py` default `--until` is `roll`.
- `--autonomous` with no `--until` uses that same default walk
  (roll), not empty. Explicit `--until empty --autonomous` stays
  the cautious pair.
- `--until empty` remains the short OpenSpec write loop (no fold,
  no beads).
- Mailbox-on-ready is out of this change (review in chat).

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat.

1. Says `/run` or `/run --autonomous`.
2. **Working** — card uses the roll table (fold / advise / act / beads).
3. **Empty** — nothing dispatchable and no spawnable advise.
4. **Off** — bare `/run` still means empty (today).

`No new UI because` `/run` and `plugins/intention/skills/run/scripts/run.py`.

## Out of scope

- Moving ASK/EYES/PUNT onto `ready`
- Killing `--until` tokens
- Flipping PENDING
