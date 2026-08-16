# add-act-conductor

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

Dispatch has a measuring stick (D2) but no scheduler. `act` still admits
a node by vibe. Fan-out needs a ready-set that is beads + disjoint
write-sets, persist that belongs to the conductor of a worktree, and a
lint that keeps “don’t commit” out of packets.

## What

- `plugins/intention/scripts/conductor.py` — ready / lint / isolate /
  persist / classify / implicated
- `act` admits only what the conductor says is dispatchable
- Isolation MAY be a worktree; conductor commits inside it
- Focused tests over inventory fixtures + a temp worktree

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none (ADR-004 already named persist-at-boundary)

## User journey & surfaces

No new UI because the surfaces are `act` and
`python3 plugins/intention/scripts/conductor.py`. Working: `ready`
prints dispatchable beads whose paths do not overlap in-flight;
`lint-packet` rejects a don’t-commit exemption; `persist` commits
exact paths in a worktree. Empty: no open beads → empty dispatchable.
Failed: two in-flight overlapping paths → the second is deferred, not
stopped. Off: do not invoke `act`; `intend` still only writes a DAG.

## Out of scope

- Spawn, prompt-file staging, stall watchdog (`add-act-runners` / `bazaar-aw7`)
- Vendoring MetaDev `planctl` or headless-exec
- Auto-merge of worktree branches to `main`
