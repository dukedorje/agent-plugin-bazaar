# Decision Steering

Use during requirements, scope, UX, architecture, and epic split. Discovery
only gathers context; validation reports findings rather than inventing
new choices. All plan records stay in the current change directory.

## Significance

| Level | Meaning | Example |
|---|---|---|
| CRITICAL | Constrains the whole product or security/data model | Primary datastore or scope boundary |
| HIGH | Constrains multiple components and downstream APIs | Authentication method or communication pattern |
| MEDIUM | Limited, replaceable choice within a category | Validation library |
| LOW | Local convention with little downstream impact | File naming |

Explain why a level applies using actual downstream consequences. For a
significant choice, provide the decision, context, two to four viable options,
pros/cons, constraints, recommendation, and rationale. Group related choices.

## Modes

Default/thorough starts GUIDED: elicit HIGH/CRITICAL choices, handle lower
levels inline. Present the recommendation first, alternative choices,
“choose for me,” and “choose for me and automate the rest.” Wait for the
answer before finalizing a required decision. A pause timeout is not consent.

Fast starts AUTONOMOUS: decide within the user's authorized scope and mark
choices `[AUTO-DECIDED]`. The user may switch modes at any time. Autonomy
never grants activation, implementation, or additional write permission.
`--auto` suppresses phase pauses, not required GUIDED decision questions.

## Records

Keep steering mode and the first three user significance overrides as short
calibration notes in `SPEC_DIR/tasks.md`. Apply that calibration to later
choices in this change. Store rationale with its phase narrative:

- Requirements: `proposal.md` What and spec deltas.
- Scoping: `proposal.md` Out of scope.
- UI and architecture: relevant `design.md` sections.
- Child split: handoff references and notes in `tasks.md`.

A decision record may use a local D-id, title, significance, decider, status,
context, choice, alternatives, and consequences. One-line records suffice
for MEDIUM choices; omit trivial boilerplate. Do not number sprints, create
external decision logs, or use a separate state file. An ADR in
`ARCHITECTURE.md` is permitted only when the shape changes and does not
replace rationale in the change. A child bead/change id is only a handoff.
