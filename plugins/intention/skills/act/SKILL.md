---
name: act
description: >
  Execute a ready work node: assign, emit a task packet, spawn a unique
  prompt, focused verify. Foreign harnesses get a packet, never a slash
  command. Use when implementing an activated change (after advise
  accept when required), a brief, or a ready-set node.
user-invocable: true
argument-hint: "<node-id or packet path>"
---

# act

Load `../../references/shared.md` and `../../references/act-io.md`.
The packet is the only interface. Schema:
`docs/contracts/agent-surface.schema.json`.

## Procedure

1. **Admit.** `python3 plugins/intention/scripts/conductor.py ready`.
   Dispatch only a `dispatchable` id. Overlap is deferred. `capped`
   means `max_inflight` is full (`ACT_MAX_INFLIGHT` or
   `ladder.json`). If rigor is `change` / `architecture` /
   `instrument` and this is a write, the change banner is
   `ACTIVE BUILD` (or the human just activated it). Architecture and
   instrument writes are not `dispatchable` while that change is in
   `needs_advise`.
2. **Assign.** `ladder.py assign --shape <shape>`. Human pick wins.
   Complementary → weave. Architecture → review-pair with a Grok
   reader. Foreign harness → packet file, never a slash command.
3. **Take.** `conductor.py take --node <id> --holder <route-id>`.
   That is the mutex: `in_progress` + lease + write-set. A second
   take fails. Do not spawn without a take.
4. **Write the packet** to the path in `act-io.md`. Lint:
   `python3 plugins/intention/scripts/conductor.py lint-packet <packet>`.
   `capability` required at change+. Anchors, not file bodies. Never a
   commit exemption.
5. **Isolate** is PARKED (`add-act-worktree-land`). Wave children
   stay on HEAD and write only `constraints.paths`. Single `act`
   may still stay on HEAD (the default). Do not call
   `conductor.py isolate` until that park is revived.
6. **Launch.** If this host has `spawn_subagent` and the assignee
   harness is `grok`, spawn `general-purpose` with the packet path
   (the worker reads `act` and the packet). If the host has
   `workflow` and this node is one of a disjoint wave, the
   conductor already launched `run-wave` — do not launch again.
   Otherwise stage a unique prompt (`spawn.py stage --packet
   <packet>`) and `spawn.py run --adapter claude` or `codex`.
   Empty/missing prompt is a hard fail. Stall → `infra-red`. On
   infra-red / park, `release` the node.
7. **Do the work** only on `constraints.paths` (owned fileset on
   HEAD). Workers edit and stop.
8. **Persist** as conductor: `conductor.py persist --paths … -m …`
   on HEAD. After a wave, persist each owned set sequentially.
   `--worktree` is PARKED. Persistence ≠ acceptance.
9. **Focused verify** once. Distill. Classify with
   `conductor.py classify <result>`. `repair` parks the implicated
   branch (`conductor.py implicated --node <id>`) and keeps unrelated
   dispatchable nodes moving. `baseline-red` completes. Spawn stall
   is already `infra-red` — retry once, then report.
10. **Write the result** after persist. Hash + distill. Conductor reads
    the face; `raw_ref` keeps the full report.
11. **Stop.** Do not fold. Self-check does not promote. Handoff: `fold`
    when the change's owed work has landed; `intend` if surprise splits
    a new node.

If the packet contradicts the laws in `docs/contracts/agent-surface.md`,
quote both instructions. Do not silently keep the narrower one.
