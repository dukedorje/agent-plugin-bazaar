# Tasks

- [x] Retarget `sprint-plan` so its spec directory is `openspec/changes/<change-id>/`.
- [x] Map each phase onto `proposal.md`, `design.md`, spec deltas, or `tasks.md` as in `design.md`.
- [x] Remove writes to `docs/sprints/` and `.omc/sprint-plan/`, including `phase-state.json`.
- [x] Replace the PARKED banner and description with the OpenSpec intake contract. Keep `disable-model-invocation: true`.
- [x] Update the default-loop living spec when this change folds.
- [x] Fresh advise after preparation

## Owed by advise — 2026-10-27

- [x] Reconcile the delta's broad “planning session” trigger and unprompted scenario with explicit factory invocation in `design.md`; preserve `intend` as the default for unrelated planning and prohibit generic planning requests from auto-starting Phase 0.
- [x] Reconcile the delta's exclusive change-directory write rule with phase 2A's external ADR and phase 2B's child artifacts: child beads and child change ids are non-plan outputs, plan narrative and progress stay in the current change, and story beads stay in the sibling change.
