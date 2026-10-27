# Phase 2A: Architecture Decisions

Inputs: `SPEC_DIR/proposal.md`, deltas, optional design journey, relevant
codebase anchors, and existing `ARCHITECTURE.md`. Decision steering is active.

## Process

1. Address applicable data, authentication/security, API/communication,
   frontend, and infrastructure concerns. Respect existing patterns unless
   the goal warrants a documented divergence.
2. For each consequential choice, record context, significance and why,
   viable alternatives, recommendation, consequences, and affected
   requirements under **Architecture** in `SPEC_DIR/design.md`.
   HIGH/CRITICAL choices warrant full rationale; MEDIUM choices may be
   one-line notes. Avoid creating design.md for trivial unchanged patterns;
   record that finding next to the phase box instead.
3. Default/fast: one planning pass. Thorough: planner proposes, architect
   challenges technical soundness and the strongest alternative, critic
   checks completeness, significance, and consistency. Limit consensus to
   three iterations and surface unresolved disagreement through steering.
   Any delegated work receives a packet scoped to these change files.
4. If the system shape changes, an ADR may be appended to `ARCHITECTURE.md`
   and linked from the change design. This is a bounded non-plan output;
   plan narrative and progress stay in the current change directory. If
   permissions exclude that file, leave an explicit ADR handoff task.
   No shape change means no ADR. Do not create separate decision logs or
   decision beads to store the plan.
5. Check whether decisions invalidate or create requirements. In thorough
   mode, refine Phase 1 and rerun architecture, at most three loops; record
   the iteration count in `tasks.md`. Default/fast records conflicts for
   resolution. Unresolved conflicts keep the phase unchecked.

## Completion

Resolve significant decisions through steering. Check Phase 2A in
`SPEC_DIR/tasks.md` when architecture is consistent with requirements,
review findings are resolved, and any bounded ADR handoff is explicit.
Reopen downstream boxes when requirements change. Next: Phase 2B.
