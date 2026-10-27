# Phase 2B: Epic Split and Handoffs

Inputs: `SPEC_DIR/proposal.md`, deltas, optional design, and completed scope
and architecture decisions. Keep the current change id as the intake plan.

## Process

1. Split the included behavior into cohesive, independently verifiable
   outcomes. Define goal, boundaries, requirement coverage, dependencies,
   acceptance, and ordering for each proposed child.
2. Prefer a single planning pass with inline coverage/dependency checks.
   Thorough mode may use planner/architect/critic review with at most three
   iterations. Use decision steering for consequential split/order choices.
3. When a split is warranted, create child beads as epic handoffs, or child
   verb-led change ids when a capability splits, within granted permissions.
   A child artifact carries its own work scope, not the current session's
   phase narrative or progress. Do not number sprints or create a second
   copy of this intake plan. Do not auto-activate child changes.
4. Record child ids, requirement coverage, dependencies, and handoff status
   next to Phase 2B in `SPEC_DIR/tasks.md`. If permissions prevent child
   creation, record the proposed handoff and leave its task unchecked.
   When no split is needed, record that explicitly instead of inventing one.

Do not write an epics markdown document. Do not decompose or materialize
story beads: those belong to `update-sprint-plan-beads`. Child epic beads
are handoffs, not an alternate plan store.

## Completion

Check Phase 2B once split decisions and child handoffs (or no-split rationale)
are recorded. Leave unresolved handoff tasks open. Reassess detail level
from actual risk and record any escalation in `tasks.md`. Read the phase
3–4 boundary notes, then continue to Phase 5.
