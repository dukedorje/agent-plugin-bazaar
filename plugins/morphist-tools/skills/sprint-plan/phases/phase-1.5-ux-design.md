# Phase 1.5: UX Design (Conditional)

Inputs: `SPEC_DIR/proposal.md`, spec deltas, and relevant existing UX sources.
Run only when there is UI. Existing UX artifacts may be referenced instead
of recreated. `--skip-ux` or fast mode skips elaboration; record the reason
and any UX gap in `SPEC_DIR/tasks.md`.

## Process

For a UI change, write the journey under `SPEC_DIR/design.md`:

- Actor, entry surface, goal, and working flow, linked to delta requirements.
- Empty, failed, and off states, including loading and recovery behavior.
- Screen/component hierarchy, available actions, navigation, and data needs.
- Validation, feedback, focus/keyboard behavior, responsive constraints,
  and accessibility considerations relevant to this change.

Reuse established conventions. Identify UX decisions that constrain APIs,
authentication, or real-time behavior for Phase 2A. Use decision steering
for significant choices. Keep all UX narrative in this design section;
do not create a standalone UX document or story specifications.

For a change without UI, record “No new UI because …” under proposal.md
User journey & surfaces. Do not create design.md solely for a non-UI journey.

## Completion

Check Phase 1.5 in `SPEC_DIR/tasks.md` after recording the journey or a
specific skip reason. A skip does not assert that UX design was produced.
Next: Phase 2A.
