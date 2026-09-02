# steer add-run-wave-workflow

**When.** 2026-09-02
**Depth.** standard

## Decided

- Native dispatch lives in skill prose, plus a `/run-wave` workflow
  (user | recommended+workflow)
- First slice: campaign `parallel()` for disjoint ready writes
  (user)

## Skipped

- Grok-only fork of the verbs

## Feeds change

When this host has `workflow` and `conductor.py wave` has two or more
nodes, launch `run-wave`. Packet stays the brief. `spawn.py` remains
for Claude/Sol. Do not replace the whole `/run` loop with Rhai.

## Later (2026-09-02)

- Park worktree isolate / land / merge (`add-act-worktree-land`).
  Wave children stay on HEAD.
- Parallelism north star is an organizer split of filesets
  (ultrapilot-shaped). **Slice one** (Sol consult, dissent on
  shared-file extraction): whole-packet disjoint waves on HEAD.
  Organizer is `bazaar-7kb.1`, after honesty + sequential persist.
