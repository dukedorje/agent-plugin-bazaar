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

Do not write an epics markdown document. Record or reuse the intake epic
bead id in `SPEC_DIR/tasks.md`; create an epic for the current change when
none exists, even when no child split is needed. Use the stable epic
external-ref and initialization checks from sprint-to-beads to avoid
duplicates. Child epic handoffs
remain references; every story in this intake is parented to its intake epic.
Story decomposition follows in Phase 3.

## Completion

Check Phase 2B once split decisions and child handoffs (or no-split rationale)
are recorded. Leave unresolved handoff tasks open. Reassess detail level
from actual risk and record any escalation in `tasks.md`. Next: Phase 3.
