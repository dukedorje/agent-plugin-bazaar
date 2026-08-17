## ADDED Requirements

### Requirement: Founding doc is a pointer after extract

After `update-founding-doc-pointer` folds, `docs/from-intention-to-running.md`
SHALL be reasoning that points at `openspec/specs/working-method/` and
SHALL NOT be the only copy of a method rule.

#### Scenario: Stranger opens the founding doc

- GIVEN the pointer change has folded
- WHEN they want the rigor dial or split rules
- THEN the doc names the living spec and does not restate the SHALL
