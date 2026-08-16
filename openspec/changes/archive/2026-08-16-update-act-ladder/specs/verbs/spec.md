## ADDED Requirements

### Requirement: intend and act resolve the ladder file

`intend` and `act` SHALL assign workers from
`plugins/intention/references/ladder.json` via
`plugins/intention/scripts/ladder.py assign --shape <shape>`.
They SHALL NOT invent a second assignment table. An explicit human
pick always wins.

#### Scenario: Known coding task

- GIVEN shape `known`
- WHEN `ladder.py assign --shape known` runs
- THEN the assignee is Claude Sonnet 5 (`skill-host`, density
  `explicit`)

#### Scenario: Architecture review is cross-family

- GIVEN shape `architecture-review`
- WHEN assign runs
- THEN the default reader is Grok, and GPT-5.6 Sol is not selected
  while `available` is false
