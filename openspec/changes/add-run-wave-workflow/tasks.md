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

- [x] Write-set known at pick: empty `paths` overlap everything
      (`pick_wave` / in-flight unknown). Packet write+lint before
      `take` is in the run loop. Test `two path-less → wave of 1`.
- [x] Cap after disjointness: `wave` de-overlaps dispatchable+capped
      then applies `free`. Test cap 2 `a(x) b(x) c(y)` → `[a, c]`.
- [x] Release every taken wave node when `workflow` fails to launch
      (infra-red). SHALL in the delta; loop in `run/SKILL.md`.
- [x] Post-wave reconciliation in `run/SKILL.md` loop: persist each
      node's `constraints.paths` sequentially on HEAD, classify /
      close / repair / park. `run-wave.rhai` `complete()` returns
      `{nodes: [{id, success}]}`.
- [ ] EYES: one real two-node wave from a Grok tab — wholly disjoint
      packets, both persists on HEAD, both beads closed, no
      `act/*` branch or `.worktrees/` left.
- [x] Scope: slice one runs from the bazaar clone only (stated in
      `proposal.md` Out of scope). Leave rhai paths as
      `plugins/intention/...` until a later slice threads the skill
      dir through `args`.

## Parked (split out 2026-09-02)

- Landing step (`act/<node>` ff-only land) is PARKED as
  `add-act-worktree-land`. Do not implement land in this change.
