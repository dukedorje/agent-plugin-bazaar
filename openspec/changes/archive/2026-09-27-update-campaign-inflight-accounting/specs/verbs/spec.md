## MODIFIED Requirements

### Requirement: take is the node mutex

`act` SHALL call `conductor.py take` with the explicit current campaign id
before staging a write worker. `take` marks the node `in_progress`, records the
holder, and writes a held act lease containing the node, campaign id, and
`constraints.paths`. A second take of the same node SHALL fail. `release`
releases that lease and frees its campaign slot. Bead status alone SHALL NOT be
treated as a held act lease. Overlapping write-sets across all held leases SHALL
stay `deferred`, including leases belonging to other campaigns.

#### Scenario: Second take is rejected

- GIVEN node C is dispatchable
- WHEN `take --node C` succeeds and is run again
- THEN the second take exits non-zero and C stays `in_progress`

#### Scenario: Cross-campaign overlap remains deferred

- GIVEN campaign A holds a lease whose paths overlap candidate C in campaign B
- WHEN campaign B asks whether C is dispatchable
- THEN C is deferred even though campaign A's lease consumes none of campaign B's slots

### Requirement: max_inflight caps campaign act leases

`run` SHALL pass the pinned intention/root id as an explicit campaign id to
`conductor.py ready`, `wave`, and `take`. Those operations SHALL apply
`max_inflight` from `ladder.json`, then `ACT_MAX_INFLIGHT`, then
`--max-inflight` against held act leases carrying that campaign id. Global bead
`in_progress` status and leases belonging to other campaigns SHALL NOT consume
the current campaign's slots. When no campaign slot remains, otherwise-ready
nodes SHALL be `capped`, not `dispatchable`.

#### Scenario: Unrelated project tracking does not exhaust a campaign

- GIVEN nineteen unrelated beads are `in_progress`
- AND the current campaign has no held act leases
- AND `max_inflight` is 2
- WHEN `ready` runs for the current campaign
- THEN it reports two free campaign slots

#### Scenario: Same-campaign leases consume the cap

- GIVEN two held act leases carry the current campaign id
- AND `max_inflight` is 2
- WHEN `ready` runs for that campaign
- THEN otherwise-ready nodes are capped

#### Scenario: Status without a lease consumes no slot

- GIVEN a current-campaign bead is `in_progress` without a held act lease
- WHEN `ready` runs for that campaign
- THEN that bead status does not reduce the campaign's free-slot count

#### Scenario: Release restores capacity

- GIVEN a campaign has reached its act-lease cap
- WHEN one of its held leases is released
- THEN the next `ready`, `wave`, and `take` observe the restored slot
