---
name: run
description: >
  Conduct a campaign over the ready-set until a stop predicate.
  Use when asked to run the loop, chain stages, go autonomous, or
  /run. Also when asked to work out a plan then run it by me, with
  optional plan / advise / ask gates (do not act until they say).
  Does not replace act (one node) or ready (observe only).
user-invocable: true
argument-hint: "[<scope>] [--until=empty|advise|activation|ask|fold|roll] [--plan] [--advise] [--ask] [--autonomous] [--max-waves=<n>] [--pause-before=<id>] [--skip=<id,id>] [--punt=<id,id>]"
---

# run

You are the **campaign conductor**. You do not inline other verbs.
You do not invent a second packet.

The campaign script is `scripts/run.py` **in this skill directory**
(the folder that contains this SKILL.md — Grok lists that path).
Do **not** run `plugins/intention/scripts/run.py` from the current
repo; that file only exists in the bazaar clone.

```
python3 <this-skill-dir>/scripts/run.py [<scope>] [--until …] [--autonomous] [--skip id,id] [--punt id,id]
```

`--max-waves` is conductor policy (default 12). The script does not
enforce it. Count waves yourself and stop when the cap hits.

It observes the *current project* via the sibling ready skill
(`../ready/scripts/ready.py` + that project's `openspec/`). It never
launches a worker.

`stop: no-ready` means the **observe script** is missing — do not
invent a ready-set. A named `<scope>` with no `openspec/changes/<id>/`
is not `no-ready`; the card will say `next: change`. Stop only when
the card has `stop` set (empty / no-ready / pause-before / ask), or
`--max-waves` hits. A refused `next` is a skip, not a stop.

If `../../references/shared.md` exists next to this plugin, load it.
Otherwise the Must not section below is enough.

## Attention

When the card says `next` is a stage (`intend`, `change`, `advise`,
`act`, `fold`), **Read** that stage's SKILL.md from the **same
skills tree as this file** (sibling directory, e.g.
`../change/SKILL.md`), not from `plugins/intention/skills/` in the
current repo. Follow that skill for one wave only when the pick is
legal for that focus. Re-read this skill and re-run the script at
the next wave.

Decision table, not a preference order: a verb-led kebab
(`add-` / `update-` / `remove-` / `refactor-` + rest) is a
change-id. Any other scope is a goal → `intend`. Named change-id
with no directory → `change`. `--until fold` / `--until roll` / `--until ask` and
fold is legal (ACTIVE BUILD, no open owed box, not PARKED, **not**
`needs_advise`) → `fold` (unscoped scans inflight). Then `advise`
before `act`. `--until roll` and `--until ask` then: send-back
**with open owed boxes** → `change`; send-back with **no** open
boxes → `needs_advise` (re-advise or park), not `change`, not
`fold`; unblocked bead with a landing and no dir → `change`;
unblocked task/feature with no landing (not epic, not `nod-`) →
`intend --extract-from` that bead. `--until ask` stops first if
there is an elicitation. Do not intend epics. Do not `act` an
architecture / instrument change that still `needs_advise`. Do not
`fold` a `needs_advise` id. `--until fold` with nothing fold-legal
is `stop: empty`.

A refused pick is a skip, not a stop. Fold refusal is “not fold
yet,” not stuck — more advise loops often unstick it.

Illegal for `focus`: `fold` + `needs_advise`; `act` +
`needs_advise`; `change` + last advise send-back + no open owed
boxes; `advise` you cannot promote (same-family / ADR-005).

Split the refusal:

- **Fold / illegal act / no-op change:** `--skip` that id (do not
  fold/act/amend it this pick). Do **not** park it on ask. Do
  **not** `--punt` it. Re-observe. `--skip` still allows `advise`
  on that same id. Follow the new `next`.
- **Advise cannot promote (same-family / ADR-005):** do not write a
  fake send-back with no architecture boxes — that retriggers
  `change`. Park the id on ask (“second-family advise”), `--punt`
  it (mailbox already names PUNT — not a ninth verb). `--until ask`
  stops here; `--until roll` continues **other** nodes.

Stop only when the new card has `stop` set, or `--max-waves` hits.
Refusing fold must not end the campaign.

Conductor loop:

```
waves = 0
skip = []
punt = []
while waves < max_waves:
  card = run.py --until <until> [--skip …] [--punt …]
  print card
  if card.stop: halt
  if card.next is fold and illegal:     # fold + needs_advise
    skip += [focus]
    continue                            # re-observe → advise that id
  if card.next is act and illegal:      # act + needs_advise
    skip += [focus]
    continue
  if card.next is change and no-op:     # send-back, no open boxes
    skip += [focus]
    continue
  if card.next is advise and cannot promote:  # ADR-005 same-family
    park focus on ask/punt
    punt += [focus]
    continue                            # do not halt; do not re-advise
  if by_me_ask and card.next is act:    # “run it by me”
    halt                                # present map; do not act
  follow sibling <next>/SKILL.md for one wave
  waves += 1
  re-read this skill
```

Illegal fold / illegal act / no-op change = continue into advise,
not halt. Same-family advise = punt, not another fake send-back.

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
| `--plan` / `--advise` / `--ask` | “run it by me” gates. See below. |

### Run it by me

When they want a plan shown before any implement — “work out a
plan then run it by me”, “show me first”, optional `--plan`
`--advise` `--ask`:

| Gate | Do | Do not |
|---|---|---|
| `--plan` | `intend` if there is no current DAG, or they asked to re-plan. Pin `map --current`. | Skip if current already is the DAG and they did not ask to re-plan. |
| `--advise` | Walk `--until advise` (scaffold `change`, then `advise`). | `act` |
| `--ask` | Present `map` of current. Stop. Wait. Next is `steer` if they want to give direction. | `act`, `--until roll`, `--until empty` |

Default for that phrase: **plan + ask**. Architecture / instrument
also gets **advise** unless they declined. `--until ask` is
different: it may `act` until an elicitation appears. “Run it by
me” never `act`s.

Halting ≠ asking. `--until ask` stops the campaign on the first
elicitation. `--until roll` parks that id on the card `ask` list
(morning review) and keeps unrelated nodes moving.

A stage raises an elicitation by putting an id on the observe `ask`
list, leaving a PENDING banner, or an open owed box matching ASK /
EYES / by-eye / human-verify. No `/ask` verb. Architecture /
human-gate direction after that halt is `steer`.

Mailbox is `/ready` faces plus ASK / EYES / PUNT on the card — not a
ninth verb.

## Must not

- Slash a foreign worker (`/run`, `/act`, `/intend`, `/meta-execute`)
- Flip PENDING or a by-eye box
- Vendor `@skills` / `.atskills` / `planctl/`
- Fold unless `--until fold`, `--until roll`, or `--until ask` and fold is legal
- Implement a node except by following `act` after a re-read
- `act` when `--ask` / “run it by me” is the stop
