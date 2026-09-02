# add-run-wave-workflow

> **ACTIVE BUILD**

**Rigor:** architecture

Activated 2026-09-02 (steer: Grok-native dispatch in skills plus a
`/run-wave` workflow; first slice is parallel disjoint `act`).

## Why

Intention never calls Grok `spawn_subagent` or `workflow`. The
campaign inlines one `act` per wave. Disjoint write nodes wait in
line. `spawn.py` cannot reach those host tools.

## What

- `conductor.py wave`: mutually disjoint subset of `dispatchable`.
- When this host has `workflow` and the wave has two or more nodes,
  `/run` launches `.grok/workflows/run-wave.rhai`.
- Each child follows `act` in an isolate worktree; conductor already
  `take`s. No `isolation_worktree` (host worktrees do not merge).
- One node, or no workflow tool: existing single `act` path.
- Claude/Sol assignees still use `spawn.py`.
- Packet remains the brief.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: amends ADR-001 consequences (dispatch may use the host's
  native spawn when the conductor is that host). Packet schema
  unchanged.

## User journey & surfaces

Duke, from a Grok tab.

1. `/run` — card `next: act`, two disjoint dispatchable nodes.
2. **Working** — `run-wave` fans them out; `/workflows` shows the
   wave.
3. **Empty** — one dispatchable: single `act`, no workflow.
4. **Off** — still one `act` at a time on every host.

`No new UI because` `/run` and `/workflows`.

## Out of scope

- Advise/consult/fold native spawn (later slice)
- Replacing the whole `/run` loop with Rhai
- `isolation_worktree` as the persist path
