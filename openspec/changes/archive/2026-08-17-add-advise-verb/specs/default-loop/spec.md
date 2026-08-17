## MODIFIED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`change`, `advise`, `act`, `fold`, and `brief` as the default
planning loop.

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `advise`
