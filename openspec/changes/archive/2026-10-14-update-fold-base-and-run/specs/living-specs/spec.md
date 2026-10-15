## MODIFIED Requirements

### Requirement: Deltas, not rewrites

A change that affects a capability SHALL record the effect as `ADDED`,
`MODIFIED`, or `REMOVED` requirements. Each requirement SHALL include at
least one `#### Scenario:`. A `MODIFIED` requirement SHALL paste the entire
requirement block; fold replaces that block wholesale. A `MODIFIED` or
`REMOVED` requirement SHALL include a base comment naming the blob of the
living spec file and its path, `<!-- base: <blob> openspec/specs/<capability>/spec.md -->`,
written when the delta is pasted. Fold SHALL omit that comment from the
living spec.

#### Scenario: Fold does not drop clauses

- GIVEN a living requirement with two scenarios
- WHEN a change MODIFIES it and omits one scenario
- THEN fold leaves only what the change pasted — so the change MUST paste
  both unless the omitted scenario is intentionally gone

#### Scenario: Paste records its base

- GIVEN a living requirement that a change MODIFIES
- WHEN `change` writes the delta
- THEN the requirement block contains a base comment whose blob is the
  living spec file at paste time
