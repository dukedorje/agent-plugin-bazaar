# working-method

What **is** built: the method is named, and the loop (OODA, rigor
dial, load class) is living. Folded from `extract-working-method` and
`add-working-loop` on 2026-08-16.

Objects and split rules still live in
`docs/from-intention-to-running.md` until `add-working-objects` and
`add-working-split` fold. Those are not living truth yet (ADR-002).

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
