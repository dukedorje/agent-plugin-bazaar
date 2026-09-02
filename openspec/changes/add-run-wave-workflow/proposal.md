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

- Slice one: whole-packet disjoint waves on HEAD. Empty `paths`
  overlap everything. `max_inflight` after disjointness.
- When this host has `workflow` and the wave has two or more nodes,
  the run campaign launches `.grok/workflows/run-wave.rhai`.
  Children stay on HEAD. Conductor already `take`s; persist is
  sequential after join.
- Fileset organizer (ultrapilot-shaped exclusive/shared/boundary)
  is the **next** node (`bazaar-7kb.1`), not this slice. Sol
  dissented on stripping shared files before the mutex and close
  see the same projection.
- One node, or no workflow tool: existing single `act` path.
- Claude/Sol assignees still use `spawn.py`.
- Packet remains the brief.

## Impact

- Capabilities: MODIFIED `verbs`, MODIFIED `packaging`
- ADRs: amends ADR-001 consequences (dispatch may use the host's
  native spawn when the conductor is that host). Packet schema
  unchanged.

## User journey & surfaces

Duke, from a Grok tab.

1. `/run` — card `next: act`, two nodes whose packet paths do not
   overlap.
2. **Working** — `run-wave` fans them on HEAD; `/workflows` shows
   the wave. Overlap waits for the next wave.
3. **Empty** — one dispatchable: single `act`, no workflow.
4. **Off** — still one `act` at a time on every host.

`No new UI because` `/run` and `/workflows`.

## Out of scope

- Advise/consult/fold native spawn (later slice)
- Replacing the whole `/run` loop with Rhai
- `isolation_worktree` as the persist path
- Worktree isolate / land / merge (`add-act-worktree-land`, PARKED)
- Fileset organizer / shared-file extraction (`bazaar-7kb.1`)
- Slice one runs from the bazaar clone only (rhai paths are
  `plugins/intention/...`; do not invent a skill-dir arg yet)
