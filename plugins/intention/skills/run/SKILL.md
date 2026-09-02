---
name: run
description: >
  Conduct a campaign over the ready-set until a stop predicate.
  Use when asked to run the loop, chain stages, go autonomous, or
  /run. Also when asked to work out a plan then run it by me, with
  optional plan / advise / ask gates (do not act until they say).
  Does not replace act (one node) or status (observe only).
user-invocable: true
argument-hint: "[<scope>] [--wait] [--tidy] [--no-fold] [--no-beads] [--plan] [--advise] [--ask] [--max-waves=<n>] [--pause-before=<id>] [--skip=<id,id>] [--punt=<id,id>]"
---

# run

You are the **campaign conductor**. You do not inline other verbs.
You do not invent a second packet.

The campaign script is `scripts/run.py` **in this skill directory**
(the folder that contains this SKILL.md — Grok lists that path).
Do **not** run `plugins/intention/scripts/run.py` from the current
repo; that file only exists in the bazaar clone.

```
python3 <this-skill-dir>/scripts/run.py [<scope>] [--wait] [--tidy] [--no-fold] [--no-beads]
```

`--max-waves` is conductor policy (default 12). The script does not
enforce it. Count waves yourself and stop when the cap hits.

It observes the *current project* via the sibling status skill
(`../status/scripts/status.py` + that project's `openspec/`). It never
launches a worker.

`stop: no-ready` means the **observe script** is missing — do not
invent a ready-set. A named `<scope>` with no `openspec/changes/<id>/`
is not `no-ready`; the card will say `next: change`. Stop only when
the card has `stop` set (empty / no-ready / pause-before / ask), or
`--max-waves` hits. `stop: empty` while `needs_advise` remains and
an other-family reader exists is **not** a stop — spawn advise.
A refused `next` is a skip, not a stop.

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
boxes. Same-family advise is **not** illegal. Follow `advise`:
spawn an other-family reader. ADR-005 forbids a sole-author
`accept`; it does not forbid the wave.

Split the refusal:

- **Fold / illegal act / no-op change:** `--skip` that id (do not
  fold/act/amend it this pick). Do **not** park it on ask. Do
  **not** `--punt` it. Re-observe. `--skip` still allows `advise`
  on that same id. Follow the new `next`.
- **Advise, any session:** do not inline `accept`. Do not write a
  fake send-back with no architecture boxes — that retriggers
  `change`. Assign `architecture-review --not-harness <author>`
  and **spawn** that reader (packet + `spawn.py`) even if this
  tab is the other family — fresh context. Wait this wave.
  `--punt` only when no spawnable other-family route exists, or
  the spawn is infra-red after `--after` handoff. No route →
  ASK, never inline. `--until ask` still stops on a true
  elicitation, not on same-family advise. `--until roll` never
  parks same-family advise as ASK.

Stop only when the new card has `stop` set, or `--max-waves` hits.
Refusing fold must not end the campaign. Same-family advise must
not end the campaign. `stop: empty` is not stuck while
`needs_advise` remains and an other-family route exists.

Conductor loop:

```
waves = 0
skip = []
punt = []
while waves < max_waves:
  card = run.py [--wait] [--tidy] [--no-fold] [--no-beads] [--skip …] [--punt …]
  print card
  if card.stop is empty and needs_advise remains and not all punted:
    # other-family spawn still owed — do not halt
    follow advise below on that id
  elif card.stop: halt
  if card.next is fold and illegal:     # fold + needs_advise
    skip += [focus]
    continue                            # re-observe → advise that id
  if card.next is act and illegal:      # act + needs_advise
    skip += [focus]
    continue
  if card.next is change and no-op:     # send-back, no open boxes
    skip += [focus]
    continue
  if by_me_ask and card.next is act:    # “run it by me”
    halt                                # present map; do not act
  if card.next is act and this host has workflow:
    write+lint packets for dispatchable  # write-set before pick
    wave = conductor.py wave            # whole-packet disjoint subset
    if len(wave) >= 2:
      take each wave node
      try:
        workflow name=run-wave args.nodes=[{id, packet}]
      except infra-red:
        release each taken node
        continue
      persist each node's paths sequentially on HEAD
      classify / close / repair / park per node
      waves += 1
      continue
    # else single act below
  if card.next is fold:
    assign ladder --shape fold          # opus-5-fold unless human picked Grok
    if this session is not that route:
      spawn designated folder in background (packet + spawn.py)
      waves += 1
      continue                          # tab keeps moving
    # else inline fold/SKILL.md below
  if card.next is advise:
    author = harness that wrote the change (this session if you wrote it)
    route = ladder assign --shape architecture-review --not-harness <author>
    if assign failed:                   # no spawnable other-family
      add owed box "ASK: second-family advise" on tasks.md if missing
      punt += [focus]
      continue                          # never inline accept
    spawn that reader always (packet + spawn.py); wait this wave
    # reader writes reviews/*-advise.md; this session never does
    if spawn infra-red after one retry:
      assign --after <route.id> and spawn; if none left: punt
    waves += 1
    continue
  follow sibling <next>/SKILL.md for one wave
  waves += 1
  re-read this skill
```

Illegal fold / illegal act / no-op change = continue into advise,
not halt. Same-family advise = spawn the other-family reader, not
punt, not a fake send-back. Punt is last-resort only.

## Native host

This session may have `spawn_subagent` and `workflow` (Grok). Python
`spawn.py` cannot call them.

- **`act` wave, two or more wholly disjoint packets:**
  `conductor.py wave`, `take` each, then
  `workflow` `run-wave` (`plugins/intention/workflows/run-wave.rhai`,
  also `.grok/workflows/run-wave.rhai` in this clone). Children stay
  on HEAD. Do not isolate (worktrees PARKED). Conductor persists
  sequentially after join. Not host `isolation_worktree`. Fileset
  organizer (shared-file split) is a later node, not this slice.
- **Single `act`, assignee grok:** `spawn_subagent`
  `general-purpose` with the packet path. Follow `act`.
- **Assignee claude / codex:** `spawn.py` as today.
- **Fold:** `subagent_type="intention:folder"` when the host has it;
  else `spawn.py`.

Packet is still the brief. Do not slash a foreign worker. Do not
replace this whole loop with Rhai — the workflow is one act fan-out.

## Policy

| Token | Means |
|---|---|
| (none) | **default = roll.** fold → send-back amend → advise → act → beads; park ASK/EYES; see `/status` for the pile; stop when empty |
| `--wait` | same walk; stop at the first elicitation (ASK, PENDING, EYES). Desk mode. |
| `--tidy` | fold-legal only |
| `--no-fold` | skip fold picks |
| `--no-beads` | skip bead landing / leftover intend. With `--no-fold` this is today's `--until empty` |
| `--advise` | walk owed reads; do not `act` |
| `--pause-before <id>` | hard stop before that node |
| `--plan` / `--ask` | “run it by me” gates. See below. `--ask` never acts (not `--wait`). |

`--until *`, `--interrupt`, and `--only fold` remain aliases for one release. `--autonomous` is ignored (warn). Mailbox is `/status`, not this card.

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
also gets **advise** unless they declined. `--wait` is
different: it may `act` until an elicitation appears. “Run it by
me” never `act`s.

Halting ≠ asking. `--wait` stops the campaign on the first
elicitation. Bare `/run` parks those ids and keeps unrelated nodes
moving. Look at the pile with `/status`.

A stage raises an elicitation by putting an id on the observe `ask`
list, leaving a PENDING banner, or an open owed box matching ASK /
EYES / by-eye / human-verify. No `/ask` verb. Architecture /
human-gate direction after that halt is `steer`.

Mailbox is `/status` (ASK / EYES / PUNT faces) — not a ninth verb. `/ready` is an alias.

## Must not

- Slash a foreign worker (`/run`, `/act`, `/intend`, `/meta-execute`)
- Flip PENDING or a by-eye box
- Vendor `@skills` / `.atskills` / `planctl/`
- Fold unless the walk is default/`--wait`/`--tidy` (or alias `roll`/`ask`/`fold`) and fold is legal
- Implement a node except by following `act` after a re-read
- `act` when `--ask` / “run it by me” is the stop
- Halt or `--punt` same-family advise while an other-family
  `architecture-review` route is available
- Write a fake send-back so you can skip the read
