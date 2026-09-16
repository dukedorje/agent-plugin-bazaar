## MODIFIED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`steer`, `change`, `advise`, `act`, `demo`, `fold`, `brief`, `debrief`,
`map`, `status`, and `run` as the default planning loop. `run` is
the campaign; `map` and `status` are observe; `brief` / `debrief`
are disposable decide; `steer` is human-gated guidance (not a
campaign wave); `demo` is the human trying the iteration after
`act` and before `fold`; the rest are stages. `ready` SHALL be listed only
as an alias of `status`. `run-wave` SHALL be listed as the act
fan-out, not a default-loop stage.

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `steer` and `demo`

#### Scenario: Stranger asks how to chain

- GIVEN the default-loop presentation
- WHEN they want more than one stage without typing each
- THEN they are pointed at `run`, not at a second catalog of execute
  verbs
