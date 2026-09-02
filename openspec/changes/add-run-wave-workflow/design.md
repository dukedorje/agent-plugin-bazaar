# Design — run-wave

## Two dispatch paths

| Host / assignee | How |
|---|---|
| This session is Grok, wave size ≥ 2 | `workflow` `run-wave` |
| This session is Grok, wave size 1, assignee grok | `spawn_subagent` `general-purpose` |
| Assignee claude / codex | `spawn.py` adapter |

The packet is the brief in every path. Foreign hosts still never see
a slash command.

## HEAD, not worktrees

Wave children stay on HEAD. `conductor.py isolate` /
`persist --worktree` / land-merge is **PARKED**
(`openspec/parked.md` `add-act-worktree-land`). Host
`isolation_worktree` is still refused (opaque lifecycle, no merge
into the parent).

Edits are safe when packet paths are exclusive. Concurrent
`git commit` on one index is not — after `parallel()` joins, the
conductor persists each node's `constraints.paths` **sequentially**
on HEAD.
Workers edit and stop. The living spec still forbids a commit
exemption in the packet; the wave prompt simply does not isolate.

## Fileset organizer (ultrapilot-shaped) — later node

oh-my-claudecode's fileset coordinator is **ultrapilot** Phase 2
(not ultrawork — ultrawork is the parallel engine; ultrapilot
assigns exclusive write-sets). Borrow the split, not the `.omc/`
state file and not Team-mode. Bead `bazaar-7kb.1`.

Rules (north star, **not slice one**):

1. **Exclusive ownership** — no file in two workers' owned sets.
2. **Shared files deferred** — intersection of declared paths, plus
   shared patterns (`package.json`, `*lock*`, `openspec/specs/**`
   when two nodes both touch the living spec). Handled sequentially
   after the wave, by the conductor — `conflictPolicy:
   coordinator-handles`.
3. **Boundary imports tracked** — files a worker reads across the
   owned/shared line. Readable by all; not in the owned write-set
   unless the organizer assigned them to one worker.

Sol consult 2026-09-02 (**dissent** on doing this in slice one):
taking the packet's full `constraints.paths` still mutexes the
shared file, so stripping it in the organizer without projecting
the packet/lease is a lie; closing a node whose shared work is
still owed breaks `classify(pass)` → close; boundary imports on
shared HEAD are stale-read hazards; `ownedGlobs` is not what
`paths_overlap` implements. Slice one fans **wholly disjoint
packets** only. Shared-file extraction waits until the mutex,
verify, and close see the same projection.

The honesty substrate the organizer needs still lands here: write
+ lint the packet before `take` on the wave path, and treat empty
`paths` as overlapping everything. `pick_wave` walks packet paths
(whole), not a second owned-set field.

## Consult (Sol, 2026-09-02)

Side channel. Does not unblock `act`. Verdict: **dissent** on
shared-file splitting in this slice. Agrees parking worktrees,
sequential persist on HEAD, empty-`[]` refuse, cap-after-disjoint,
release-on-infra, Rhai = one act wave. One tradeoff: fewer waves
from whole-packet disjointness, vs partial-node execution. Raw:
`.spawns/consult-1788377376-55636-1381ffba/raw.txt`.

## Disjoint subset

`conductor.py ready` `dispatchable` is capped by `max_inflight` and
disjoint from *in-flight* paths. That cap currently runs **before**
mutual de-overlap, so the wave under-fills (`a(x) b(x) c(y)` → `[a]`
instead of `[a, c]`). Compute the disjoint subset over
ready-minus-deferred, **then** apply `free`.

Empty `paths` overlap everything. Two path-less nodes are a wave of
one (or of zero, if the remaining node is also empty — then fall
through to single `act`).

## Take before launch

The conductor `take`s every wave node before `workflow` starts. A
child that `take`s again fails. If the launch is infra-red, release
every taken node before the campaign `continue`s.

## After the wave

`run-wave.rhai` `complete()` returns `[{id, success}]`. The
conductor, per node: persist `constraints.paths` on HEAD
(sequential), read `groups/<id>/results/*.json`, `classify`, close /
repair / park, `release` on failure. A node still closes as a
whole — no partial shared-file remainder in this slice.

## One wave, not the campaign

Rhai does not read OpenSpec banners or spawn Sol. `/run` still
observes, picks fold/advise/change, and re-enters the loop. The
workflow is only the act fan-out inside a wave.
