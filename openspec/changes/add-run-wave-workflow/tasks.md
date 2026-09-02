# Tasks

- [x] `conductor.py wave` mutually disjoint dispatchable subset
- [x] `.grok/workflows/run-wave.rhai` + `validate_only` smoke
- [x] `run/SKILL.md` + `act/SKILL.md` native dispatch
- [x] harness.md
- [x] verbs delta
- [x] Tests for wave pick
- [x] Park worktree isolate/land (`openspec/parked.md` `add-act-worktree-land`); wave children stay on HEAD

## Owed (advise send-back 2026-09-02, fable-5.1-arch-review — amended 2026-09-02 after park)

Worktree landing is **not** owed here. It lives in PARKED
`add-act-worktree-land`. Fileset organizer (shared-file split) is
**not** this slice — bead `bazaar-7kb.1`, after Sol 2026-09-02
dissent. Slice one is whole-packet disjoint waves on HEAD.

- [ ] Write-set known at pick: `paths` come only from
      `groups/<id>/packet.json`, which `act` writes *after* `take`,
      so `wave` sees `[]` for any fresh node and calls it disjoint
      (repro: two path-less nodes → wave of 2). Write + lint the
      packet before `take` on the wave path, **and** make `pick_wave`
      / `dispatch` treat empty `paths` as overlapping everything.
      SHALL + scenario in the delta; test `two path-less → wave of 1`.
- [ ] Cap after disjointness: `dispatch` applies `max_inflight`
      before `pick_wave` de-overlaps (repro: cap 2, `a(x) b(x) c(y)`
      → wave `[a]`, not `[a, c]`). Compute the disjoint subset
      over ready-minus-deferred then apply `free`.
- [ ] Release every taken wave node when `workflow` fails to launch
      (infra-red). Add the SHALL to `specs/verbs/spec.md` delta.
- [ ] Post-wave reconciliation in `run/SKILL.md` loop: persist each
      node's `constraints.paths` sequentially on HEAD, read each
      `groups/<id>/results/*.json`, `classify`, close / repair / park,
      `release` otherwise. `run-wave.rhai` `complete()` returns
      `[{id, success}]`, not counts only.
- [ ] EYES: one real two-node wave from a Grok tab — wholly disjoint
      packets, both persists on HEAD, both beads closed, no
      `act/*` branch or `.worktrees/` left.
- [ ] Scope: slice one runs from the bazaar clone only (stated in
      `proposal.md` Out of scope). Leave rhai paths as
      `plugins/intention/...` until a later slice threads the skill
      dir through `args`.

## Parked (split out 2026-09-02)

- [ ] ~~Landing step: `act/<node>` branches from `conductor.py isolate`
      reach main~~ → `openspec/parked.md` `add-act-worktree-land`.
      Revive when Duke wants worktrees again. Do not implement land
      in this change.
