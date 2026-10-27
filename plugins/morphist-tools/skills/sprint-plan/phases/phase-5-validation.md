# Phase 5: Intake Validation

Inputs: `SPEC_DIR/proposal.md`, `SPEC_DIR/tasks.md`, optional design, spec
deltas, and references to bounded ADR/child handoffs. Validate the intake
that exists; story generation is deferred to `update-sprint-plan-beads`.

## Checks

- Why and What address the user's goal; requirements have testable scenarios.
- MODIFIED deltas contain the full living requirement with the intended
  amendment. Capability ids, references, and codebase anchors resolve.
- Every included outcome is covered by a delta and planned implementation
  task or an explicit child handoff. Deferred scope is not silently included.
- Architecture and UI journey (when applicable) agree with requirements;
  significant choices and conflicts are resolved or visibly outstanding.
- Child handoffs have coherent boundaries and acyclic dependencies.
- All plan narrative and phase progress are in the current change directory.
  An ADR exists only for a shape change; child artifacts are handoffs.
- Checked intake boxes have evidence or explicit conditional skip reasons.
  Unfinished implementation, story handoff, activation, and fold work stay open.

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

Finish the remaining intake/finding boxes only when their evidence supports
completion. Check Phase 5 when validation passes and required review accepts.
Show pass, pass-with-warnings, or fail with supporting paths and remaining
boxes. Do not create a readiness report or decision graph file.

Always present the outcome, including in automatic modes. Identify the
change directory, child handoffs, and deferred story work. Intake readiness
is not implementation completion; keep implementation and fold boxes open.
Do not edit living specs, fold, or archive from this phase.
