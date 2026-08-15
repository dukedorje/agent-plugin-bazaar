# Topologies

Face 2 of C1. A topology is a wiring, not a ceremony. More can be added
without changing the agent surface. Adding one is an architecture amendment.

Every topology implements the same reduce: **N member results → one signed
result** in the group's identity. If it cannot produce that, it is not a
topology.

## Shared rules

1. Members receive ordinary packets. They do not need to know they are inside
   a group, except when the topology attaches another member's artifacts as
   input (pipeline, some weaves).
2. Members are agents. A member may itself be a group.
3. Write-sets are declared on the member packet (`constraints.paths`). A
   topology that allows overlapping write-sets must say so. Default: **disjoint**.
4. The group signs exactly one reduced result. Interior results stay on disk
   under `groups/<id>/results/`.
5. The group's `disposition` is a function of member dispositions, defined
   per topology. Do not invent a seventh failure class.
6. Promotion (the result may close a write node) is stricter than disposition.
   A `pass` that cannot promote stays a `pass` with `promoted: false`.
7. Same-family review of one's own work cannot promote. Self-check is free.

## Catalog

`min` / `max` count **direct** members, not nested ones.

### `solo`

| | |
|---|---|
| Members | 1 / 1 |
| Parallel | n/a |
| Write-set | the member's |
| Packet | the group packet *is* the member packet |
| Reduce | member result, re-signed by the group identity (or the member identity if no group wrapper) |
| Disposition | the member's |
| Promotes | if the member would promote |

Exists so “assign to Grok” and “assign to a group” are the same operation.

### `weave`

| | |
|---|---|
| Members | 2 / unbounded |
| Parallel | yes, after packets are split |
| Write-set | **disjoint**, or explicitly cited (B's packet lists A's artifact as an anchor, not as a shared write) |
| Packet | **split**. Each member gets a different goal/role. Shared: acceptance of the *group*, requester, load class, rigor. Not shared: paths, member goal |
| Reduce | all members `pass` (or `baseline-red`, which counts as complete) **and** each artifact the reduce claims is cited by at least one member result. Missing citation → `blocked` |
| Disposition | all complete → `pass`; any `task-red` → `task-red` on the implicated member's branch; any `blocked`/`infra-red` after retry → that class; mix of terminal failures → `blocked` with member ids in evidence |
| Promotes | reduce is `pass` and, if rigor is `architecture` or `instrument` or permission is `sensitive`, a human-gate ancestor has activated |

Default complementary group. Members do different jobs. Fork is the exception.

### `pipeline`

| | |
|---|---|
| Members | 2 / unbounded, **ordered** |
| Parallel | no |
| Write-set | may accumulate; later members may write paths earlier members wrote only if the earlier result has committed |
| Packet | sequential. Member *k+1* receives the group packet plus member *k*'s signed result as input (`input_result_id`) |
| Reduce | last member's result, re-signed; earlier results remain interior |
| Disposition | first non-complete member's class; else last member's |
| Promotes | last member promotes |

Three agents and two edges. Not a sprint.

### `fan-out`

| | |
|---|---|
| Members | 2 / unbounded |
| Parallel | yes |
| Write-set | **disjoint** (hard) |
| Packet | same goal and acceptance; paths and harness differ |
| Reduce | a matrix or summary artifact, not a rewrite of member work. The reduce itself is a small write (one file) owned by the group identity |
| Disposition | all complete → `pass`; else same mix rule as weave |
| Promotes | reduce `pass` |

Use when pieces do not share a write-set. Harness adapters are the type case.

### `fork`

| | |
|---|---|
| Members | 2 / unbounded |
| Parallel | yes |
| Write-set | **disjoint implementations** of the same acceptance (separate trees, worktrees, or path prefixes). Shared acceptance, not shared code |
| Packet | **same** goal, acceptance, load class, rigor. Implementation path differs |
| Reduce | pick one member by discriminating evidence. Losers are `parked` with a revive condition, not deleted |
| Disposition | winner's class; losers `parked` |
| Promotes | winner would promote **and** the evidence would look different if the other side were chosen |

Open only when at least two of: schema/auth/money/protocol blast; load class
`intention-critical` or `ambiguous`; two designs survived Orient; cost of
being wrong exceeds two short acts.

### `review-pair`

| | |
|---|---|
| Members | 2 / 2 — `builder`, `reader` |
| Parallel | no. Reader starts after builder's result exists |
| Write-set | builder writes; **reader writes nothing** in the builder's paths. Reader may write only a result file |
| Packet | builder gets the group packet. Reader gets the group packet plus the builder's result, with `constraints.permission: read` |
| Reduce | builder's artifacts + reader's disposition |
| Disposition | builder `task-red` / `infra-red` / `blocked` wins (nothing to read). Else the reader's class |
| Promotes | reader `pass`, or reader dissent plus a human member accepting the dissent |

The reader asks, at instrument rigor: *how would I fake this?* and *would
this evidence look the same if the claim were false?*

### `human-gate`

| | |
|---|---|
| Members | 1+ agents and **exactly one** `kind: human` |
| Parallel | agent(s) may draft before the human acts |
| Write-set | drafts may write only under `changes/` or `groups/` until activation. Source trees and living `specs/` wait |
| Packet | agents get `permission: read` (they may draft). Human gets the activation packet |
| Reduce | cannot sign a `write` or `sensitive` result until the human result exists with `disposition: pass` and `activation: true` |
| Disposition | no human yet → `blocked`; human rejects → `parked`; else the draft member's class |
| Promotes | human activated |

This is PENDING → ACTIVE. The human is a member, not an external exception.

### `conductor-workers`

| | |
|---|---|
| Members | 1 `conductor` + 1+ `worker` |
| Parallel | workers yes, on the ready-set the conductor exposes |
| Write-set | workers: declared paths only, commit-on-red, never `git add -A`. Conductor: the graph write door (checkboxes, beads, reduce), never workers' source paths |
| Packet | workers receive an **inlined** packet (goal, anchors, acceptance, paths). Never “go read the plan.” Conductor receives the group packet |
| Reduce | conductor signs after workers' results and the graph update |
| Disposition | conductor's classification of worker results (same failure classes) |
| Promotes | conductor `pass` |

MetaDev's execution tree, named so it can nest. The conductor owns remote
push if any; workers do not push.

### `quorum`

| | |
|---|---|
| Members | `n` ≥ 2, parameter `k` with `1 < k ≤ n` |
| Parallel | yes |
| Write-set | usually none (promotion of someone else's artifacts). If writing, disjoint |
| Packet | same packet to all |
| Reduce | `k` member `pass` results → group `pass`. Otherwise `blocked` |
| Disposition | as reduce |
| Promotes | `k` passes. Use for contested promotions and releases, not typos |

## Adding a topology

Amend this file. Add a row set in the same shape. Do not change packet or
result schemas unless a shared rule is wrong. A new topology that needs a
new failure class is probably two topologies.

Reserved names must not be reused for a different wiring.
