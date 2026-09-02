# Tasks

- [x] `conductor.py wave` mutually disjoint dispatchable subset
- [x] `.grok/workflows/run-wave.rhai` + `validate_only` smoke
- [x] `run/SKILL.md` + `act/SKILL.md` native dispatch
- [x] harness.md
- [x] verbs delta
- [x] Tests for wave pick

## Owed (advise send-back 2026-09-02, fable-5.1-arch-review)

- [ ] Landing step: `act/<node>` branches from `conductor.py isolate`
      reach main after a wave (e.g. `conductor.py land --node <id>`:
      ff-only merge, worktree remove, branch delete; fail loud on
      non-ff). Fix `design.md` "our merge path" to name it.
- [ ] Post-wave reconciliation in `run/SKILL.md` loop: read each
      `groups/<id>/results/*.json`, `classify`, close / repair / park,
      `land` on close, `release` otherwise. `run-wave.rhai` `complete()`
      returns `[{id, success}]`, not counts only.
- [ ] Release every taken wave node when `workflow` fails to launch
      (infra-red). Add the SHALL to `specs/verbs/spec.md` delta.
- [ ] EYES: one real two-node wave from a Grok tab — both commits on
      main, both beads closed, no `act/*` branch or `.worktrees/` left.
- [ ] Scope: state "slice one runs from the bazaar clone only" in
      `proposal.md` Out of scope, or pass the skill dir via `args`.
- [ ] Write-set known at pick: `paths` come only from
      `groups/<id>/packet.json`, which `act` writes *after* `take`,
      so `wave` sees `[]` for any fresh node and calls it disjoint
      (repro: two path-less nodes → wave of 2). Either write + lint
      the packet before `take` on the wave path, or make `pick_wave`
      / `dispatch` treat empty `paths` as overlapping everything.
      SHALL + scenario in the delta; test `two path-less → wave of 1`.
- [ ] Cap after disjointness: `dispatch` applies `max_inflight`
      before `pick_wave` de-overlaps (repro: cap 2, `a(x) b(x) c(y)`
      → wave `[a]`, not `[a, c]`). Compute the disjoint subset over
      ready-minus-deferred then apply `free`, or name the under-fill
      in `design.md` "Disjoint subset".
