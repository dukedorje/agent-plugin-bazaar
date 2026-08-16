# add-claude-spawn

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

Spawn can stage a prompt but cannot launch Claude Code. Fan-out has no
cap. “Claim is advisory” left no mutex when a worker actually takes a
node — two conductors could stage the same bead.

## What

- `spawn.py --adapter claude` runs live `claude -p` (model/effort from
  the ladder interface). Tests use a stub binary.
- `ladder.json` `max_inflight` (override `ACT_MAX_INFLIGHT` or
  `--max-inflight`)
- `conductor.py take` / `release`: node mutex = `in_progress` + lease
  + write-set. Overlap still defers. Slots cap background workers.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none (ADR-004 persist, ADR-005 ladder still hold)

## User journey & surfaces

No new UI because the surfaces are `act` and the two scripts. Working:
`take` then `spawn.py run --adapter claude` on a staged spec. Empty:
`max_inflight` reached → ready lists `capped`, nothing new launches.
Failed: second `take` on the same node is rejected. Off: `--adapter
exec` still works; no Claude CLI required for tests.

## Out of scope

- Codex / Grok headless adapters
- Auto-merge of worktrees
- Changing persist-at-boundary
