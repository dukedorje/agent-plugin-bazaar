# update-run-second-family

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-09-02 (chat: run until roll should spawn advise, not halt).

## Why

`--until roll` treats same-family advise (ADR-005) as illegal, `--punt`s
the id, and then halts as “stuck” once siblings are PENDING. The
default `architecture-review` route is already Claude Fable — a
second family versus a Grok author — but the conductor never follows
`advise` because `run` parks first. `--punt` also blocks later `act`.
Sol being off is not “no second family.”

## What

- Same-family advise is not a campaign stop and not an ASK park.
- Assign `architecture-review --not-harness <author>` and spawn that
  reader (packet + `spawn.py`). Wait this wave so the review lands.
- `--punt` only when no other-family route exists, or spawn is
  infra-red after one retry.
- Do not write a fake send-back. Do not inline a sole-author `accept`.
- `advise` second family is any other harness than the author, not
  “Grok or Sol” (Claude-author-centric). Grok author → Fable/Opus.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none (ADR-005 already forbids sole-author accept)

## User journey & surfaces

Duke, from chat.

1. `/run --until roll` on a DAG whose architecture node Grok authored.
2. **Working** — card `next: advise`; conductor spawns Fable (or Grok
   if Claude authored); waits; re-observes; `act` when accept lands.
3. **Empty** — nothing dispatchable and no spawnable advise.
4. **Off** — park as ASK / PUNT and halt while Fable is on the ladder.

`No new UI because` `/run` and `plugins/intention/skills/{run,advise}/SKILL.md`.

## Out of scope

- Flipping PENDING
- Making Sol the default reader
- Leaving the current DAG for unrelated tracker beads
