## ADDED Requirements

### Requirement: Block-store stage fails closed

The system SHALL run a block-store stage as a stage step on the
named session, after the idle check and before the paste. A step
that does not finish SHALL NOT write the prompt file and SHALL NOT
paste. The declaration shape of that store waits on steer. This
requirement does not name a path, a hash, or a Mjolnir mount.

#### Scenario: The store step does not finish

- GIVEN a stage whose source is the block store named by steer
- WHEN that step does not finish
- THEN the prompt file is absent and the pane is not pasted

#### Scenario: No store declaration

- GIVEN a Pi spawn spec with no block-store stage
- WHEN the pane is idle
- THEN this requirement adds no copy
