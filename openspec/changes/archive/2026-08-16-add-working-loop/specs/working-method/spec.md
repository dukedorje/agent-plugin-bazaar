## ADDED Requirements

### Requirement: Every node circulates observe-orient-decide-act

Work SHALL circulate observe → orient → decide → act, then observe
what the act did. A surprise mid-act SHALL be a new Observe, not a
process violation. Tempo SHALL beat completeness.

#### Scenario: Surprise mid-act

- GIVEN a worker finds the plan contradicts the code
- WHEN they return
- THEN the conductor opens a new Observe (intend / split), and does
  not treat the surprise as a failed ritual

### Requirement: Rigor is a dial

Ceremony SHALL be a function of lifecycle and blast: vibe, brief,
change, architecture, instrument. It SHALL escalate only. A restore
or typo SHALL NOT require a change directory.

#### Scenario: Typo

- GIVEN a spelling fix in an existing specced file
- WHEN work starts
- THEN the agent does a direct fix and does not scaffold
  `openspec/changes/`

### Requirement: Load class sets posture

Orient SHALL name `structure-clear`, `intention-critical`, or
`ambiguous`. `ambiguous` SHALL include a human member.

#### Scenario: Ambiguous why

- GIVEN structure underdetermines the business rule
- WHEN the agent orients
- THEN they stop for a human instead of inventing the rule from a
  call graph
