# Phase 1B: Scoping

Inputs: `SPEC_DIR/proposal.md` and spec deltas. Scope appetite may be focused,
standard, or ambitious; it describes a bounded change, not a numbered sprint.

## Process

1. Cluster requirements by cohesion and dependencies. Identify foundations,
   independent work, uncertain integrations, and the smallest useful outcome.
2. Propose IN, STRETCH, and DEFER boundaries with rationale, user value,
   dependency impact, and risk of deferral. Use estimates only to compare
   scope; do not create stories or story counts as a deliverable.
3. Treat the boundary as a CRITICAL decision. In GUIDED mode present the
   recommendation and options to include, exclude, or adjust appetite and
   wait for the user's choice. In AUTONOMOUS mode record the chosen boundary
   with an `[AUTO-DECIDED]` marker within authorized scope.
4. Write exclusions, deferred clusters, pickup conditions, and risks under
   `SPEC_DIR/proposal.md` **Out of scope**. Keep included behavior in What
   and the deltas consistent. Record stretch items as excluded unless their
   inclusion condition has been explicitly accepted.

Do not create a separate scope document or an external backlog. Phase 2B
may hand independently scoped work to child beads or child change ids.

## Completion

Record the resolved appetite and scope decision in `SPEC_DIR/tasks.md`,
then check Phase 1B. Lightweight scopes still get a short Out of scope
section. Next: Phase 1.5.
