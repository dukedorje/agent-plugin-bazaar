## MODIFIED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`change`, `advise`, `act`, `fold`, `brief`, `ready`, and `run` as
the default planning loop. `run` is the campaign; the others are
stages (or observe / disposable decide).

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `advise` and `run`

#### Scenario: Stranger asks how to chain

- GIVEN the default-loop presentation
- WHEN they want more than one stage without typing each
- THEN they are pointed at `run`, not at a second catalog of execute
  verbs
