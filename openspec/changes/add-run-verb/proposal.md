# add-run-verb

> **ACTIVE BUILD**

**Rigor:** change

## Why

The seven stage verbs only move when someone types the next one.
Chaining is prose (“roll through beads”). That cannot sleep, cannot
stop at a named seam, and cannot punt a branch while the tree
continues. MetaDev solved this with `/auto-execute` plus forty other
names. We need the campaign object, not the catalog.

`/run` is that object: a policy around the stages we already have.

## What

- Add verb **`run`**: campaign conductor. Invokes `intend` / `change` /
  `advise` / `act` / `fold` / `brief` / `ready` by **re-reading** each
  stage skill at the wave it enters (attention: inject next to the
  task; do not inline those bodies).
- Policy on the run, not new verbs: `--until <stop>`,
  `--autonomous`, consult-before-ask, `--pause-before <id>`,
  `--max-inflight`.
- Mailbox is `/ready` faces plus ASK / EYES / PUNT in the run
  report — not a ninth verb.
- Foreign workers still get a packet. Never `/run`.
- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`.

## Impact

- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`
- ADRs: will amend `ARCHITECTURE.md` (loop table) when this folds
- Attention paper (arXiv:2608.12610): law only — re-read per wave.
  No `@skills` protocol in this change.

## User journey & surfaces

Duke, from chat, on a ready-set or an epic.

1. Says `/run` or `/run bazaar-crj --until advise`.
2. Skill loads policy, then `ready`. YOUR MOVE first if anything
   needs him.
3. **Working** — dispatchable writes: take → act (re-read `act`) →
   persist → next node until the stop predicate.
4. **Empty** — no dispatchable writes; print the run card and stop.
5. **Failed / ASK** — veto, send-back, or activation: park that
   subject, continue siblings, or stop if `--until ask`.
6. **Off** — skill missing; stages still work one at a time.
7. **Autonomous** — no mid-run questions. Consult before ASK.
   By-eye deferred to EYES. Morning card: LANDED / DECIDED /
   PARKED / YOUR EYES / RESIDUAL.

`No new UI because` the surfaces are chat (`/run`) and
`python3 scripts/ready.py`.

## Out of scope

- `@skills` protocol, hub, `.atskills/`, `.autotrigger` — later delivery
- Grok/Codex spawn adapters — `bazaar-crj.3` / `add-act-headless`
- Path B overlay ADR — `bazaar-crj.1` / `update-path-b-overlay`
- `/inbox` as a ninth verb — alias of ready if ever
- `planctl/`, MetaDev command surface, `/unpark`, `/execute`
- Flipping by-eye boxes under `--autonomous`
