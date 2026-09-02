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
