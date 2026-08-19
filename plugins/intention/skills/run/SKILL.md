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

You are the **campaign conductor**. You do not inline other verbs.
You do not invent a second packet.

The campaign script is `scripts/run.py` **in this skill directory**
(the folder that contains this SKILL.md — Grok lists that path).
Do **not** run `plugins/intention/scripts/run.py` from the current
repo; that file only exists in the bazaar clone.

```
python3 <this-skill-dir>/scripts/run.py [<scope>] [--until …] [--autonomous]
```

It observes the *current project* via the sibling ready skill
(`../ready/scripts/ready.py` + that project's `openspec/`). It never
launches a worker.

`stop: no-ready` means the **observe script** is missing — do not
invent a ready-set. A named `<scope>` with no `openspec/changes/<id>/`
is not `no-ready`; the card will say `next: change`. If `stop` is
set, print the card and halt.

If `../../references/shared.md` exists next to this plugin, load it.
Otherwise the Must not section below is enough.

## Attention

When the card says `next` is a stage (`change`, `advise`, `act`),
**Read** that stage's SKILL.md from the **same skills tree as this
file** (sibling directory, e.g. `../change/SKILL.md`), not from
`plugins/intention/skills/` in the current repo. Follow that skill
for one wave. Re-read this skill and re-run the script at the next
wave.

Order is `change` → `advise` → `act`. Do not `act` an
architecture / instrument change that still `needs_advise`.

## Policy

| Token | Means |
|---|---|
| `--until empty` | walk change → advise → act until nothing is dispatchable (default) |
| `--until advise` | dispatch `advise` when a read is owed; do not `act` |
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
