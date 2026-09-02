## MODIFIED Requirements

### Requirement: Default verbs

The marketplace and repo orientation SHALL present `intend`,
`change`, `advise`, `act`, `fold`, `brief`, `debrief`, `ready`, and
`run` as the default planning loop. `run` is the campaign; the
others are stages (or observe / disposable decide). `debrief` is
the disposable expand after a finish or fail, the opposite analog
of `brief`.

#### Scenario: README install

- GIVEN the root README
- WHEN a stranger copies the install line
- THEN they install `intention@agent-plugin-bazaar`, not
  `sprint-plan@…`
- AND the listed skills include `advise`, `run`, and `debrief`

#### Scenario: Stranger asks how to chain

- GIVEN the default-loop presentation
- WHEN they want more than one stage without typing each
- THEN they are pointed at `run`, not at a second catalog of execute
  verbs

### Requirement: run may enter any loop stage

`run` SHALL be allowed to enter `intend`, `change`, `advise`,
`act`, or `fold` as a campaign wave. It SHALL NOT be presented as
only `change` → `advise` → `act`. `ready`, `brief`, and `debrief`
SHALL stay outside that wave set.

#### Scenario: Stranger asks if run can intend

- GIVEN the default-loop presentation
- WHEN they have a goal and no change-id
- THEN they are pointed at `/run` with that goal, which owes
  `next: intend`, not only at typing `/intend` first
