# Phase 1: Requirements

Inputs: `SPEC_DIR/proposal.md` Why, the user brief, relevant living specs,
and existing deltas. Read the codebase anchors found during discovery.

## Process

1. Extract user outcomes, functional requirements, nonfunctional constraints,
   integration contracts, and testable acceptance scenarios. Distinguish
   confirmed requirements from assumptions; resolve material gaps through
   decision steering rather than inventing scope.
2. Summarize intended behavior under `SPEC_DIR/proposal.md` **What** and
   list affected capabilities under **Impact**. Preserve Why and other sections.
3. Write requirements as deltas in
   `SPEC_DIR/specs/<capability>/spec.md`. Use ADDED, MODIFIED, or REMOVED
   Requirements and GIVEN/WHEN/THEN scenarios. For MODIFIED, copy the whole
   living requirement and amend it; a partial block loses clauses on fold.
4. Cover working, empty, failed, and off behavior where relevant. Check
   compatibility with existing contracts and trace each requirement to the
   user's goal. Keep out-of-scope requests for Phase 1B.
5. At lean detail use concise What and delta blocks. Deeper ceremony adds
   rationale and scenarios in these same files, never a separate PRD.

## Refinement and completion

When architecture reveals a conflict, update only affected requirements and
What, then reopen downstream phase boxes in `SPEC_DIR/tasks.md`. Record the
conflict and resolution there; do not silently expand scope.

Use decision steering for HIGH/CRITICAL choices. Check Phase 1 only after
requirements and scenarios are testable and required decisions resolved.
Do not update living specs. Next: Phase 1B.
