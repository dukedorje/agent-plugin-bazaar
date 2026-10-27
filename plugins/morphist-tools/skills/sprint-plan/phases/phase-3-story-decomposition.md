# Phase 3: Story Decomposition

Inputs: `SPEC_DIR/proposal.md`, spec deltas, optional `design.md`, and the
intake epic and child handoff references in `SPEC_DIR/tasks.md`.

## Process

1. Decompose included outcomes into independently verifiable stories. Keep
   each story bounded by user value and requirement coverage; split oversized
   work by behavior rather than technical layers. Exclude deferred scope.
2. For each story define a stable local id, title, user story and scope,
   testable acceptance criteria (GIVEN/WHEN/THEN where useful), design notes,
   test tier, complexity, relevant decision ids, and story dependencies.
   Resolve consequential scope or ordering choices through decision steering.
3. Follow sprint-to-beads initialization (including database checks), then
   use its external-ref and field mapping to look up each
   story in beads. Create missing stories with `bd create -t task`,
   `--parent {intake-epic-id}`, `--description`, and `--acceptance`; update
   existing stories in place. Capture the real id before creating edges.
   Never create a stories directory, story markdown, or a story template.
4. Add one open checkbox per acceptance in `SPEC_DIR/tasks.md`, grouped by
   story bead id and stable acceptance id (for example `AC1`). Store the
   story external-ref and intake epic id there so continuation can re-anchor.
   Reuse existing matching rows on retries; do not duplicate checkboxes.
5. Check coverage and dependency direction; reject cycles and dangling
   references. Use the materializer's decision links and dependency rules.
   Preserve unrelated phase, implementation, and fold tasks.

## Completion

Check Phase 3 only when every decomposed story exists as a bead with its
acceptance criteria, intake epic parent, and matching acceptance checkboxes.
An empty included scope creates no story beads; record the reason. If `bd`
fails or permission prevents materialization, leave the phase unchecked and
report the blocker. Next: Phase 4.
