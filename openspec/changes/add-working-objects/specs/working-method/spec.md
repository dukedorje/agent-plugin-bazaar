## ADDED Requirements

### Requirement: Work objects are the seven kinds

The method SHALL talk in these objects: intention, capability, change,
work node, agent, evidence, learning. Documents SHALL be how some of
them are shown, not a parallel store.

#### Scenario: Status in a path

- GIVEN a change directory named as if it were done
- WHEN an agent decides whether the behavior exists
- THEN they read the living spec and the in-file banner, not the path

### Requirement: A brief dies after landing

A brief SHALL contain goal, acceptance, contract, inherited, and out
of scope. After the work lands, the brief SHALL NOT be treated as
durable truth.

#### Scenario: Brief kept as spec

- GIVEN a 200-line brief after fold
- WHEN an agent cites it as current behavior
- THEN that citation is wrong; living spec, ADR, or LEARNINGS.md is
  the residue
