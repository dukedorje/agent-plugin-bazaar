# Phase 4: Elaborate Story Beads

Inputs: the Phase 3 story beads and acceptance rows in `SPEC_DIR/tasks.md`,
proposal, spec deltas, optional design, and referenced architecture decisions.
The retained phase filename does not authorize story files or templates.

## Process

1. Read each bead's description, acceptance, design notes, parent, and
   dependencies. Elaborate the user outcome, scope boundaries, technical
   requirements, architecture compliance, and verification approach in its
   fields using `bd update`. Keep test tier and complexity labels current.
2. Make acceptance criteria concrete and independently checkable. Cover
   working, empty, failed, and off behavior where relevant. Use lean,
   standard, or full detail as selected, in these same bead fields.
3. Mirror every acceptance as one open checkbox under its story bead id in
   `SPEC_DIR/tasks.md`. Preserve stable acceptance ids. Re-sync unchanged
   rows without duplication or resetting checked work; new or substantively
   changed criteria start unchecked. Report removed criteria explicitly and
   preserve their history outside the active acceptance checklist.
4. Verify requirement coverage, design/architecture consistency, and the
   story dependency graph. Repair bounded gaps in place; unresolved scope
   choices return to steering. Do not invent implementation completion.

Never write story markdown, a stories directory, or a story template.
Story narrative belongs in beads; the current change keeps plan narrative,
phase progress, references, and acceptance checkboxes.

## Completion

Check Phase 4 only after enriched bead fields and acceptance rows agree.
Leave failed updates and missing criteria unchecked. Continue to Phase 5,
which runs sprint-to-beads as the normal end of intake without a flag.
