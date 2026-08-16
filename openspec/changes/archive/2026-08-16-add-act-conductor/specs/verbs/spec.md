## ADDED Requirements

### Requirement: act dispatches a disjoint ready-set

`act` SHALL admit a write node only when
`plugins/intention/scripts/conductor.py ready` lists it as
`dispatchable`. A node is dispatchable when its inbound deps are
closed and its `constraints.paths` do not overlap an in-flight
write-set. Overlap SHALL defer that node; it SHALL NOT stop the tree.

#### Scenario: Overlapping in-flight is deferred

- GIVEN node A `in_progress` on `plugins/intention/scripts/conductor.py`
  and node B ready on that same path
- WHEN `conductor.py ready` runs
- THEN A is not dispatchable and B is `deferred`, and an unrelated
  ready node on another path remains dispatchable

### Requirement: conductor persists in the isolation boundary

When `act` isolates a node in a worktree, the conductor SHALL persist
with `conductor.py persist` on exact paths. Worker packets SHALL NOT
contain a commit exemption (`do not commit`, `don't commit`, or
`do_not` containing `commit` / `git`). `do_not: ["push"]` remains
allowed.

#### Scenario: lint rejects a commit exemption

- GIVEN a packet whose `do_not` includes `commit`
- WHEN `conductor.py lint-packet` runs
- THEN it exits non-zero

#### Scenario: persist commits only declared paths

- GIVEN a worktree from `conductor.py isolate` with two dirty files
- WHEN persist is given one path
- THEN the commit contains only that path
