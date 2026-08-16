# add-dispatch-density

> **ACTIVE BUILD** → folded and archived 2026-08-15.

## Why

Fan-out needs a measuring stick before a scheduler. The conductor must
read one small face, packets must name how much to say and what surface
the assignee speaks, and persist must belong to the isolation boundary
— not to every subprocess.

## What

Instrument-grade amendment of the agent surface:

- Packet fields: `density`, `surface`, `consult`
- Identity: optional `interface` (cloud / other hosts)
- Result: `distilled` + `raw_ref`
- Six-role tree vocabulary in `docs/contracts/dispatch.md`
- Persist law: conductor of a worktree commits; workers edit
- `distill-result.py` projects the conductor face; full report stays

## Impact

- Capabilities: MODIFIED `agent-surface`, MODIFIED `verbs`
- ADRs: ADR-004 (dispatch density + persist-at-boundary)

## User journey & surfaces

No new UI because the surfaces are `intend` (writes density), `act`
(reads distilled), and `python3 docs/contracts/validate.py`. Working:
a lean packet validates; a distiller prints one face and keeps
`raw_ref`. Empty: old packets without the new fields still validate.
Failed: distilled disposition disagrees with the result. Off: do not
invoke `act`; schema stays additive.

## Out of scope

- Ready-set scheduler / disjoint-path dispatch (`add-act-conductor`)
- Creating worktrees (`add-act-conductor`)
- Spawn runners, prompt-file staging, stall watchdog (`add-act-runners`)
- Vendoring MetaDev `planctl` or headless-exec (ADR-003 / F1-path-b)
