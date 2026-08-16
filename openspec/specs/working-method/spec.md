# working-method

What **is** built: the method is named; loop, objects, and split
rules are living. Folded from `extract-working-method`,
`add-working-loop`, `add-working-objects`, and `add-working-split`
on 2026-08-16.

The founding novel is still the long explainer until
`update-founding-doc-pointer` folds.

## Purpose

The method can be extracted as named changes. The founding novel may
reason. It is not the only store once a matching change has folded.

## Requirements

### Requirement: Method lives in named changes, not only the novel

The method of working SHALL be extractable as named verb-led change-ids.
`docs/from-intention-to-running.md` MAY reason. It SHALL NOT be the only
place a method rule exists once the matching change has folded.
Landing ids for the first extract SHALL be `add-working-loop`,
`add-working-objects`, `add-working-split`, and
`update-founding-doc-pointer`.

#### Scenario: Stranger asks how we work

- GIVEN the extract has folded
- WHEN they look for the loop, objects, or split rules
- THEN they find a living spec under `working-method` (or a child
  requirement folded into it), not only a section in the founding novel

#### Scenario: Founding doc still reasons

- GIVEN `update-founding-doc-pointer` has not folded
- WHEN an agent cites a SHALL only in `docs/from-intention-to-running.md`
- THEN that citation is not living truth (ADR-002)

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

### Requirement: Checkboxes are owed work

A checkbox SHALL be work **this** node or change owes. Handoffs,
findings, and out-of-scope SHALL be bullets. A checkbox that can
never close SHALL NOT appear in the ready-set.

#### Scenario: Handoff as a checkbox

- GIVEN a tasks.md box that says "tell Duke" or "fold later"
- WHEN hygiene or `ready` runs
- THEN that box is not owed work and must be a bullet, or the change
  is not honest
