# Change resolution

The old sprint protocol is retired. Do not create `docs/sprints/`,
`.omc/sprint-plan/`, `phase-state.json`, or a `current` symlink.
Story status lives on beads. Narrative lives in one OpenSpec change.

## Resolution

1. Use `--change=<id>` when the caller passed one.
2. Otherwise use the change this session is already working.
3. If that is ambiguous, ask. Do not pick the newest directory.

`SPEC_DIR` means `openspec/changes/<change-id>/`. Read `proposal.md`,
`design.md`, and `tasks.md` from there. An archived change under
`openspec/changes/archive/` is read-only.

Beads (`bd show`, `bd ready`, `bd note`) are the status record. Do not
keep a second map file.

`verify` and `review-fix` still contain an older inline preamble that
mentions `.omc/sprint-plan/`. That preamble is leftover. Follow this
file when the two disagree.
