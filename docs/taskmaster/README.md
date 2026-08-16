# Taskmaster — how to read these files

Product notes for `taskmaster.dev`. This folder is **not** living truth.
Nothing here is a `SHALL`. Living specs stay under `openspec/specs/` after
a change folds.

These files move with the sibling app repo when that repo exists. Until
then they live next to the kernel so the host cannot drift from the
agent surface.

| File | Kind | Write when |
|---|---|---|
| [INTENT.md](INTENT.md) | Commander’s intent | Outcome, non-goals, constraints change |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Decisions + open questions | A choice survived Orient |
| [NOTES.md](NOTES.md) | Speculative | Doubts, hops, “we’ll probably…” |

**Do not** put speculation in `LEARNINGS.md` (that file is hard-won fact).
**Do not** put stack choices in this repo’s living specs.
**Do** amend ARCHITECTURE.md rather than delete when reality diverges.
**Do** open `add-taskmaster-host` before any kernel SHALL.

Playground VM (2026-08-15): `0a0fa094-252f-47b7-b348-6e4624eac9ef`,
shared guest tmux session `taskmaster`.
