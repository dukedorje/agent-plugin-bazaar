## ADDED Requirements

### Requirement: run may enter any loop stage

`run` SHALL be allowed to enter `intend`, `change`, `advise`,
`act`, or `fold` as a campaign wave. It SHALL NOT be presented as
only `change` → `advise` → `act`. `ready` and `brief` SHALL stay
outside that wave set.

#### Scenario: Stranger asks if run can intend

- GIVEN the default-loop presentation
- WHEN they have a goal and no change-id
- THEN they are pointed at `/run` with that goal, which owes
  `next: intend`, not only at typing `/intend` first
