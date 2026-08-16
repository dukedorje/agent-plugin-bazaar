# working-method

What **is** built: the method of working is named and has landing
change-ids. Folded from `extract-working-method` on 2026-08-16.

Loop, objects, and split rules still live in
`docs/from-intention-to-running.md` until `add-working-loop`,
`add-working-objects`, and `add-working-split` fold. Those are not
living truth yet (ADR-002).

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
