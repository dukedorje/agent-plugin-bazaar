## MODIFIED Requirements

### Requirement: In-file disposition

Every in-flight `proposal.md` SHALL begin its body with a disposition
banner: `> **PENDING**`, `> **ACTIVE BUILD**`, or
`> **PARKED** — revive when <condition>`.

Agents SHALL draft at `PENDING`. Humans SHALL authorize `ACTIVE BUILD` activation (including by saying
"activate <id>" in chat). `change` MAY apply recorded whole-intention
authority to dependency-ready, prepared nodes within agreed scope, as
defined by verbs / Bounded campaign activation. A banner alone SHALL NOT
prove preparation or authorize changed commitments. A `PARKED` change
SHALL NOT be implemented, extended, or counted in the ready-set.

#### Scenario: Path-stripped retrieval still shows status

- GIVEN a chunker that returns `proposal.md` body without the directory path
- WHEN a reader sees the first banner
- THEN they can tell whether the change is draft, active, or parked

