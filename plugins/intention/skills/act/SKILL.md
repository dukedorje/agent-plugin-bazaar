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

1. **Prepare, then admit.** Load `../../references/preparation.md`.
   Verify current preparation even for a directly invoked or previously
   activated node. Follow change/brief if missing or stale; re-observe after
   amendments. Do not take a lease or emit a packet for an unreconciled
   contract. Resolve `campaign_id` explicitly: use the pinned intention/root
   id when this act belongs to a campaign, or the node id for a direct
   one-node act. Then **admit:** `python3 plugins/intention/scripts/conductor.py
   ready --campaign <campaign_id>`.
   Dispatch only a `dispatchable` id. Overlap is deferred. `capped`
   means `max_inflight` is full (`ACT_MAX_INFLIGHT` or
   `ladder.json`). If rigor is `change` / `architecture` /
   `instrument` and this is a write, the change banner is
   `ACTIVE BUILD` (or the human just activated it). Architecture and
   instrument writes are not `dispatchable` while that change is in
   `needs_advise`.
2. **Assign.** `ladder.py assign --shape <shape>`. Human pick wins.
   Complementary → weave. Architecture advise uses `vary-reader`
   (`references/reviewers.md`): Astra on high blast, otherwise rotate,
   skip the author's vendor. Foreign harness → packet file, never a slash command.
3. **Spike gate.** Load `../../references/from-sprint-exec.md`. If
   this node still has an open unverified hypothesis (a `- Spike:`
   line that is not `go` or `skipped`, or `design.md` `## Unverified
   hypotheses`), do not take and do not spawn. Spike is the option:
   run the morphist `spike` skill, or record a skip as a `bd note`
   and set the line to `skipped`. A `go` finding clears the gate.
4. **Take.** `conductor.py take --campaign <campaign_id> --node <id>
   --holder <route-id>`.
   That is the mutex: `in_progress` + lease + write-set. A second
   take fails. Do not spawn without a take.
5. **Write the packet** to the path in `act-io.md`. Lint:
   `python3 plugins/intention/scripts/conductor.py lint-packet <packet>`.
   `capability` required at change+. Anchors, not file bodies. Never a
   commit exemption.
6. **Isolate** is PARKED (`add-act-worktree-land`). Wave children
   stay on HEAD and write only `constraints.paths`. Single `act`
   may still stay on HEAD (the default). Do not call
   `conductor.py isolate` until that park is revived.
7. **Launch.** If this host has `spawn_subagent` and the assignee
   harness is `grok`, spawn `general-purpose` with the packet path
   (the worker reads `act` and the packet). If the host has
   `workflow` and this node is one of a disjoint wave, the
   conductor already launched `run-wave` — do not launch again.
   Otherwise stage a unique prompt (`spawn.py stage --packet
   <packet>`) and `spawn.py run --adapter claude` or `codex`.
   Empty/missing prompt is a hard fail. Stall → `infra-red`. On
   infra-red / park, `release` the node.
8. **Do the work** only on `constraints.paths` (owned fileset on
   HEAD). Workers edit and stop.
9. **Persist** as conductor: `conductor.py persist --paths … -m …`
   on **current HEAD**. After a wave, persist each owned set
   sequentially. Current HEAD is the default, not an absolute restriction:
   switch or create a branch when the user requests it, the task explicitly
   targets one, or the workflow requires a known transition. Resolve the exact
   target and protect dirty worktree changes first. Before persist, determine
   whether the current branch backs an open PR. Unless this task is explicitly
   follow-up work for that PR, do not append commits there; move the work to an
   appropriate task branch after protecting the worktree. Never invent a branch
   solely for this act when the current branch is otherwise appropriate.
   `--worktree` is PARKED. Persistence ≠
   acceptance. Uncommitted writes are not a reason to skip the
   next wave (`fold` / `demo`).
10. **Focused verify** once. Distill. Classify with
   `conductor.py classify <result>`. `repair` parks the implicated
   branch (`conductor.py implicated --node <id>`) and keeps unrelated
   dispatchable nodes moving. `baseline-red` completes. Spawn stall
   is already `infra-red` — retry once, then report.
11. **Write the result** after persist. Hash + distill. Conductor reads
    the face; `raw_ref` keeps the full report. Beads are the status
    record (`../../references/from-sprint-exec.md`): close with a
    one-line reason, file list on `bd note`. A blocker stays open,
    labeled, and noted. Do not close it by working around it.
12. **Stop.** Do not fold. Self-check does not promote. Handoff: `fold`
    when the change's owed work has landed; `intend` if surprise splits
    a new node.

If the packet contradicts the laws in `docs/contracts/agent-surface.md`,
quote both instructions. Do not silently keep the narrower one.
