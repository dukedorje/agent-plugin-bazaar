# advise — add-run-wave-workflow (2026-09-02)

> **ADVISE:** send-back
> **READER:** fable-5.1-arch-review
> **SPAWN:** .spawns/add-run-wave-workflow-advise-1788376095-82878-c03c2ab5

Rigor: architecture. Banner: ACTIVE BUILD (not touched). Blind pass:
proposal Why → living `verbs` "run conducts a campaign" + ADR-001 →
`conductor.py` `dispatch`/`pick_wave`, `run/SKILL.md` Native host,
`run-wave.rhai` → independent take → then `design.md` / `tasks.md`.
`test-conductor.py` green (8 pass). Two reproductions below were run
against `conductor.py wave` with throwaway inventories.

**Provenance.** A first spawn of this same reader
(`.spawns/add-run-wave-workflow-advise-1788375878-69806-94d349c0`)
wrote a send-back to this path at 12:09 and added five owed boxes to
`tasks.md`. No design, code, or delta file changed between that spawn
and this one (design/proposal/delta 11:45, rhai/SKILL 11:47), so this
is a duplicate dispatch, not a re-advise. This file supersedes that
one. Its findings are all re-confirmed here and its five boxes stand;
this pass adds one blocker it did not catch (finding 1) and one box
for the cap order.

## Verdict

**Send-back.** The shape is right and small: `wave` is a pure subset
of `dispatch` output, `take` stays the only mutex, the packet stays
the brief, and one-node / no-`workflow` hosts fall through to the
existing `act`. Two things block acceptance at architecture rigor:

1. **The wave's disjointness is computed against a write-set that
   mostly does not exist yet.** `paths` come only from
   `groups/<id>/packet.json` (`conductor.py:256-266`, `:302`); no
   packet → `[]`. `intend` writes no packet and no `paths`
   (`intend/SKILL.md`, grep empty). The packet is written by `act`
   step 4, *after* `take` in step 3 (`act/SKILL.md:31-37`), and the
   wave loop has the same order — `wave` → `take` → "write packets"
   → `workflow` (`run/SKILL.md:128-132`). `paths_overlap([], …)` is
   always empty (`conductor.py:55-65`), so a path-less node overlaps
   nothing in `dispatch` (`:152`) and nothing in `pick_wave`
   (`:186`). Reproduced: inventory `a{}`, `b{}`, `c{in_progress}` →
   `wave = [a, b]`. In this repo 51 beads, 14 have a packet; for the
   other 37 the word "disjoint" in the proposal, delta, and
   `design.md:20-25` is not a property the code can see. Two fresh
   nodes that will both edit `run/SKILL.md` are a legal wave today.

2. **Nothing lands and nothing reconciles.** `design.md:16-18`
   rejects host `isolation_worktree` because it "does not merge into
   the parent" and names `conductor.py isolate` + `persist --worktree`
   as "our merge path". That path does not merge either: `isolate`
   makes `.worktrees/<node>` on branch `act/<node>`
   (`conductor.py:484-502`); `persist` commits onto that branch
   (`:505-529`). There is no `land`/`merge` subcommand, no merge step
   in `act/SKILL.md:38-63`, none in the child prompt
   (`run-wave.rhai:22-33`), and the loop goes `workflow` → `waves +=
   1` → `continue` (`run/SKILL.md:132-134`). N children → N committed
   branches nobody lands, N beads left `in_progress` by `take`, and
   the next observe treats them as in-flight, blocking their
   dependents. (Spawn 1's finding; re-confirmed.)

Finding 1 is the one this pass adds. It is the more fundamental of the
two because it falsifies the change's own premise; finding 2 falsifies
the design's central "why not X". Owed boxes are on `tasks.md`.

## Independent take (written before opening design.md / tasks.md)

1. Pin: packet is the only brief; the rhai envelope stays thin and
   must not grow into a second `act` body.
2. Pin: `wave` is a pure function over `dispatch` output; `take` is
   the only mutex; no wave-level lock, no second RPC (ADR-001).
3. Pin: wave is an optimisation — one node or no `workflow` falls
   through unchanged; `workers_launched` stays 0 on the card.
4. Refuse: host `isolation_worktree` as the persist path.
5. Refuse: admitting a node into a wave whose write-set is unknown.
   `paths` are read from the packet; if the packet is written after
   the pick, "disjoint" is vacuous. Must be answered.
6. Refuse: N `take`s then a launch with no release-on-failure.
7. Refuse: children that persist on `act/<node>` with no owner for
   getting those commits to main and closing the beads.
8. Concern: `dispatch` applies `max_inflight` (`:160-162`, default 2
   at `:122`) *before* `pick_wave` removes mutual overlap, so the wave
   under-fills. Reproduced: cap 2, `a(x) b(x) c(y)` → `wave = [a]`,
   though `[a, c]` was legal.
9. Concern: rhai hardcodes `plugins/intention/...` (`:23`, `:29`)
   while `run/SKILL.md:16-21` calls that exact assumption a bug.
10. Unverifiable from here: Rhai `parallel()` result shape
    (`r.success`, `:47`), `pause` semantics (`:8-13`). Needs by-eye.

## Steelman against my take

- *"Finding 1 is pre-existing: `dispatch`'s in-flight overlap check
  has the same blind spot."* Partly true, but in the single-`act`
  path the in-flight node's packet has been written by the time a
  second node is admitted (step 4 precedes step 6), so the in-flight
  side of the comparison is usually populated. Inside one wave both
  sides are picked in the same instant, before either packet exists.
  The wave is the first place the blind spot is symmetric.
- *"Just write the packet before `wave`."* That is a legitimate fix
  and probably the right one — it also gives `lint-packet` a chance
  to run before `take`. But it reorders `act` steps 3 and 4 for the
  wave path, so it belongs in the delta as a SHALL, not as an
  implementer's private choice. Alternatively make `[]` overlap
  everything; either is fine, one must be written down.
- *"The merge gap is `act`'s debt, not this change's."* Before this
  change isolation was optional ("Disjoint nodes may stay on HEAD",
  `act/SKILL.md:38-40`) and single. This change makes it mandatory
  per child (`proposal.md:21`, `run-wave.rhai:29-32`), multiplies it
  by N, and promotes it to the stated merge path. The debt is now on
  this change's critical path.
- *"Children could persist on shared HEAD since paths are disjoint."*
  Edits are safe; commits are not. N concurrent `git add` + `git
  commit --only` (`conductor.py:514-522`) in one tree race on
  `.git/index.lock`. Isolation is right — which is why landing must
  be owned.
- *"`validate_only` smoke covers the rhai."* Syntax only. `r.success`,
  `pause`, and `parallel` shape fail only at runtime.

## One real tradeoff

**Where the write-set is declared.** Today `paths` live only in the
packet, written by the conductor at `act` time. Moving the declaration
earlier — `intend` emits `paths` per node, or `act` writes the packet
before `take` — makes the wave honest and lets the scheduler see
collisions before it commits N beads to `in_progress`. The cost is
that `intend` (or the pre-take packet) must guess a write-set before
the worker has looked, and a wrong guess is worse than no guess: two
nodes declared disjoint that actually collide will both persist on
their own branch and the collision surfaces only at `land`. The
alternative — treat `[]` as "overlaps everything" — is safe and cheap
but makes the wave useless for any bead without a packet, i.e. the
wave only fires on the second visit to a node. The design implicitly
picks neither; it assumes the packet exists. Pick one and say so.

## Findings

1. **Wave disjointness is vacuous for packet-less nodes** — blocker.
   `conductor.py:256-266` (`[]` when no packet), `:302`, `:55-65`,
   `:186`; order `take` → write packet at `act/SKILL.md:31-37` and
   `run/SKILL.md:128-132`. Reproduced `wave = [a, b]` for two
   path-less nodes. Delta scenario "Overlapping dispatchable is not a
   wave of two" only covers nodes that already have `paths`.
2. **Design claims a merge path that does not exist** — blocker.
   `design.md:16-18` vs `conductor.py:484-502` (branch `act/<node>`),
   `:505-529` (commit on that branch). No merge anywhere.
3. **No post-wave reconciliation** — blocker, same root as 2,
   different fix. `run/SKILL.md:132-134` goes `workflow` → `continue`.
   Nothing reads `groups/<id>/results/*.json`, `classify`es, closes /
   repairs / parks, or releases leases. `run-wave.rhai:43-50` returns
   counts only, discarding node identity.
4. **No release on launch failure** — owed. `design.md:29-30` says
   "Release on infra-red" in one line; the delta has no SHALL and the
   loop has no step. `take` has already flipped N beads and written N
   leases (`conductor.py:430-445`).
5. **Rhai unverified at runtime** — owed. `tasks.md` box 2 is
   `validate_only`. `r.success` (`:47`), `pause` (`:8-13`), and
   `parallel` shape have no fixture here. EYES box.
6. **Cap before disjointness under-fills the wave** — owed (small).
   `conductor.py:160-162` caps before `:178-191` de-overlaps.
   Reproduced `wave = [a]` where `[a, c]` was legal. Either compute
   the disjoint subset over ready-minus-deferred then apply `free`,
   or name the under-fill in `design.md:20-25`.
7. **Clone-only paths** — owed (one-line scope). `run-wave.rhai:23,
   29` hardcode `plugins/intention/...`; `.grok/workflows/` copy is
   identical (diffed). `run/SKILL.md:16-21` treats this assumption as
   a bug for `run.py`. Declare "bazaar clone only" or thread the
   skill dir through `args`.
8. **Prompt-vs-skill drift (minor, no box)** — `run-wave.rhai:22-33`
   restates `act` steps 5, 7, 8, 9, 10, 11. "Do not take again" is
   necessary; the rest duplicates "Read act/SKILL.md" and will drift.

## What is solid

- `pick_wave` (`conductor.py:178-191`) is pure, greedy, first-match.
  Greedy is correct here; maximum disjoint set is not worth it. Test
  `test_wave_drops_overlapping_dispatchable` covers the shape it can
  see.
- `take` remains the sole mutex (`conductor.py:359-377`); the wave
  adds no second lock. Delta "SHALL `take` each node before launch"
  matches `run/SKILL.md:130` and `design.md:27-30`.
- Rejecting host `isolation_worktree` is right for the reason given
  (opaque lifecycle); the error is in what was claimed for the
  alternative.
- ADR-001 amendment is minimal and honest: native spawn only when the
  conductor *is* that host; the packet is passed by path
  (`run-wave.rhai:24-25`); no second RPC; foreign harnesses still get
  a packet; `run.py` still launches nothing so `workers_launched`
  stays 0.
- The wave sits under `next: act` only (`run/SKILL.md:127`), so
  `--ask` / "run it by me" / `needs_advise` gates are untouched. The
  living decision table is unchanged.
- Fallbacks are explicit and match across three files: one node →
  single `act`; no `workflow` → existing path; Claude/Codex →
  `spawn.py` (`design.md:5-9`, `act/SKILL.md:41-49`,
  `run/SKILL.md:170-177`).
- Scope discipline: "one act fan-out, not the loop" is stated in
  proposal, steer, design, and the rhai honours it — no banner reads,
  no reader spawns.

## Implementer gaps (for whoever picks up the send-back)

- Write-set before pick: the smallest honest fix is to write and lint
  the packet **before** `take` on the wave path (reorder `act` 3↔4
  for wave children and say so in the delta), so `wave` sees real
  `paths`. Belt-and-braces: make `pick_wave` refuse a node with empty
  `paths` (treat `[]` as overlapping everything) and add the test
  `two path-less nodes → wave of 1`. Add a SHALL + scenario.
- Landing: `conductor.py land --node <id>` — `git merge --ff-only
  act/<node>` in the main tree, `git worktree remove
  .worktrees/<node>`, `git branch -d`. Disjoint paths make ff-only
  safe only if main has not moved on those paths; if it has, fail
  loud and park — do not rebase silently. Fix `design.md:16-18`.
- Reconciliation: after `workflow` returns, per wave node read
  `groups/<id>/results/*.json`, `classify`, close / repair
  (`implicated`) / park; `land` on close, `release` otherwise. Make
  `run-wave.rhai` `complete()` return `[{id, success}]`.
- Failure path: wrap the `workflow` launch; on infra-red `release`
  every taken node before `continue`. SHALL in the delta.
- Cap order: disjoint subset over ready-minus-deferred, then `free`.
- Scope line: "slice one runs from the bazaar clone only" in
  `proposal.md` Out of scope, or pass the skill dir via `args`.
- Do not fix any of this by telling children "do not commit" — the
  living spec forbids it (`verbs/spec.md:270-274`, `lint-packet`).
