# Phase 5: Intake Validation

Inputs: `SPEC_DIR/proposal.md`, `SPEC_DIR/tasks.md`, optional design, spec
deltas, and references to bounded ADR/child handoffs. Validate the intake
that exists, including the story beads and their acceptance checkboxes.

## Checks

- Why and What address the user's goal; requirements have testable scenarios.
- MODIFIED deltas contain the full living requirement with the intended
  amendment. Capability ids, references, and codebase anchors resolve.
- Every included outcome is covered by a delta and planned implementation
  task or an explicit child handoff. Deferred scope is not silently included.
- Architecture and UI journey (when applicable) agree with requirements;
  significant choices and conflicts are resolved or visibly outstanding.
- Child handoffs have coherent boundaries and acyclic dependencies.
- Every story bead has acceptance criteria and the recorded intake epic parent.
  Each acceptance has one matching checkbox in `SPEC_DIR/tasks.md`; new
  criteria are open. Story ids and dependencies resolve without cycles.
- All plan narrative and phase progress are in the current change directory.
  An ADR exists only for a shape change; child artifacts are handoffs.
- Checked intake boxes have evidence or explicit conditional skip reasons.
  Unfinished implementation, activation, and fold work stay open.

## Findings and review

Record findings, evidence, and remaining work in `SPEC_DIR/tasks.md`.
Use checkboxes for actionable findings. Correct mechanical reference errors
within scope, at most two repair passes, then report remaining gaps. Do not
fix scope/architecture conflicts by silently adding work. Reopen the affected
phase and downstream boxes when their conclusions change.

At architecture rigor, route the prepared change through `advise` using a
fresh reader. For a foreign harness, send a review packet rather than a host
slash command. Record the verdict/evidence in `tasks.md`; self-verification
does not supply independent acceptance. An outstanding required review
keeps validation open. Do not expand permissions to run the review.

## Completion

Run `sprint-to-beads` against this `CHANGE_ID` and `SPEC_DIR` as the normal
end of intake, without a separate flag. Re-sync the existing beads and
acceptance rows using their stable ids; do not duplicate them. Confirm the
materializer succeeds and `bd ready` lists unblocked stories. On failure,
leave Phase 5 unchecked and report the failing item and recovery path.
An empty story list is valid and mints no story beads.

Finish the remaining intake/finding boxes only when their evidence supports
completion. Check Phase 5 when validation passes and required review accepts.
Show pass, pass-with-warnings, or fail with supporting paths and remaining
boxes. Do not create a readiness report or decision graph file.

Always present the outcome, including in automatic modes. Identify the
change directory, intake epic, child handoffs, and story bead ids. Intake readiness
is not implementation completion; keep implementation and fold boxes open.
Do not edit living specs, fold, or archive from this phase.
