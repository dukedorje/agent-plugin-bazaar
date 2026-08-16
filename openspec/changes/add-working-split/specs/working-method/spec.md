## ADDED Requirements

### Requirement: A node has one acceptance surface

A work node SHALL have one acceptance surface. If a scenario cannot
fail today and pass after, it SHALL NOT be a change.

#### Scenario: No failing scenario

- GIVEN a proposed change with no scenario that fails today
- WHEN `change` runs
- THEN it is refused or rewritten as a document, spike, or vibe-fix

### Requirement: Edges are real dependencies

B SHALL NOT start until A has committed a usable artifact with the
evidence its contract requires. Readiness SHALL come from artifacts.
Ceremony SHALL record that fact, not create it.

#### Scenario: Checkbox without artifact

- GIVEN A's checkbox is marked done and no commit exists
- WHEN B asks if it is ready
- THEN B is not ready

### Requirement: Governing prose names landings

Reasoning documents SHALL name verb-led change-ids when they imply
work. They SHALL NOT become a second requirements store.

#### Scenario: Novel implies a SHALL

- GIVEN `docs/from-intention-to-running.md` states a rule as if it
  were required
- WHEN that rule is not in `openspec/specs/`
- THEN it is not living truth until a named change folds it
