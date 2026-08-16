# update-act-ladder

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

Subscriptions are Grok + Claude Code (CC has the high limits). The
ladder still talks as if Grok is the default coder and Codex is in
the pool. Known work should go to Sonnet 5, thought to Opus 5,
planning consult to Fable 5, design to Opus 5 (low/medium) with CC
designer skills, and real architecture must be read by Grok or Sol.

## What

- `plugins/intention/references/ladder.json` — the ONE assignment table
- `ladder.py assign --shape …` so intend/act do not improvise
- Update `dispatch.md`, `act-io.md`, intend-dag, founding assignment
- ADR-005

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: ADR-005

## User journey & surfaces

No new UI because the surfaces are `intend` (writes assignee) and
`act` (resolves the ladder). Working: `ladder.py assign --shape known`
prints Sonnet 5; `--shape architecture-review` prints Grok; Sol is
listed but `available: false`. Empty: unknown shape exits non-zero.
Failed: a node assigned to Grok for a rename. Off: human `--assignee`
still wins.

## Out of scope

- Wiring live `claude -p` / `codex exec` adapters
- Buying or assuming a Codex subscription
- Changing persist / spawn
