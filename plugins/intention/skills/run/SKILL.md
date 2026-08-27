---
name: run
description: >
  Conduct a campaign over the ready-set until a stop predicate.
  Use when asked to run the loop, chain stages, go autonomous, or
  /run. Does not replace act (one node) or ready (observe only).
user-invocable: true
argument-hint: "[<scope>] [--until=empty|advise|activation|ask|fold|roll] [--autonomous] [--max-waves=<n>] [--pause-before=<id>]"
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

`--max-waves` is conductor policy (default 12). The script does not
enforce it. Count waves yourself and stop when the cap hits.

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

When the card says `next` is a stage (`intend`, `change`, `advise`,
`act`, `fold`), **Read** that stage's SKILL.md from the **same
skills tree as this file** (sibling directory, e.g.
`../change/SKILL.md`), not from `plugins/intention/skills/` in the
current repo. Follow that skill for one wave. Re-read this skill
and re-run the script at the next wave.

Decision table, not a preference order: a verb-led kebab
(`add-` / `update-` / `remove-` / `refactor-` + rest) is a
change-id. Any other scope is a goal → `intend`. Named change-id
with no directory → `change`. `--until fold` / `--until roll` / `--until ask` and
fold is legal (ACTIVE BUILD, no open owed box, not PARKED) →
`fold` (unscoped scans inflight). Then `advise` before `act`.
`--until roll` and `--until ask` then: send-back → `change`;
unblocked bead with a landing and no dir → `change`; unblocked
task/feature with no landing (not epic, not `nod-`) → `intend
--extract-from` that bead. `--until ask` stops first if there is
an elicitation. Do not intend epics. Do not `act` an architecture /
instrument change that still `needs_advise`. Do not `fold` unless
`--until fold`, `--until roll`, or `--until ask` and fold is legal.

## Policy

| Token | Means |
|---|---|
| `--until empty` | default: change → advise → act. Stop at PENDING, ASK, and fold. Do not intend a verb-led change-id. Do not fold. |
| `--until advise` | dispatch `advise` when a read is owed; do not `act` |
| `--until activation` | stop on PENDING |
| `--until ask` | same walk as roll; stop at the first elicitation (ASK, PENDING, by-eye / EYES) |
| `--until fold` | `next: fold` when legal; unscoped scans inflight |
| `--until roll` | fold → send-back amend → advise → act → bead landing/change → intend leftover tasks; park ASK on the card; stop when stuck |
| `--autonomous` | no mid-run questions; EYES; never deploy; never flip PENDING. Pair with `--until roll` to keep walking |
| `--pause-before <id>` | hard stop before that node |

Halting ≠ asking. `--until ask` stops the campaign on the first
elicitation. `--until roll` parks that id on the card `ask` list
(morning review) and keeps unrelated nodes moving.

A stage raises an elicitation by putting an id on the observe `ask`
list, leaving a PENDING banner, or an open owed box matching ASK /
EYES / by-eye / human-verify. No `/ask` verb.

Mailbox is `/ready` faces plus ASK / EYES / PUNT on the card — not a
ninth verb.

## Must not

- Slash a foreign worker (`/run`, `/act`, `/intend`, `/meta-execute`)
- Flip PENDING or a by-eye box
- Vendor `@skills` / `.atskills` / `planctl/`
- Fold unless `--until fold`, `--until roll`, or `--until ask` and fold is legal
- Implement a node except by following `act` after a re-read
