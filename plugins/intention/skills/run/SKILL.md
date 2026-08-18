---
name: run
description: >
  Conduct a campaign over the ready-set until a stop predicate.
  Use when asked to run the loop, chain stages, go autonomous, or
  /run. Does not replace act (one node) or ready (observe only).
user-invocable: true
argument-hint: "[<scope>] [--until=empty|advise|activation|ask|fold] [--autonomous] [--pause-before=<id>]"
---

# run

Load `../../references/shared.md`. You are the **campaign conductor**.
You do not inline other verbs. You do not invent a second packet.

```
python3 plugins/intention/scripts/run.py [--until …] [--autonomous]
```

That script **observes** (`scripts/ready.py`) and prints a card. It
never launches a worker. If the card `stop` is set, print it and halt.

## Attention

When the card says `next` is a stage, **Read**
`plugins/intention/skills/<stage>/SKILL.md` now, then follow that
skill for one wave. Do not paste those bodies here. Re-read at the
next wave.

## Policy

| Token | Means |
|---|---|
| `--until empty` | stop when nothing is dispatchable (default) |
| `--until advise` | stop when the next owed step is a read |
| `--until activation` | stop on PENDING |
| `--until ask` | stop at the first ASK |
| `--until fold` | after writes, fold if legal |
| `--autonomous` | asleep: until empty, consult-before-ask, EYES punch-list; never deploy; never flip by-eye |
| `--pause-before <id>` | hard stop before that node |

Halting ≠ asking. Park a veto subject; keep unrelated nodes moving
unless `--until ask`.

Mailbox is `/ready` faces plus ASK / EYES / PUNT on the card — not a
ninth verb.

## Must not

- Slash a foreign worker (`/run`, `/act`, `/intend`, `/meta-execute`)
- Flip PENDING or a by-eye box
- Vendor `@skills` / `.atskills` / `planctl/`
- Fold unless `--until fold` and fold is legal
- Implement a node except by following `act` after a re-read
