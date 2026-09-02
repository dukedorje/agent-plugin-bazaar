## ADDED Requirements

### Requirement: run wave fans disjoint act nodes

When the campaign's `next` is `act` and this host provides
`workflow`, `run` SHALL write and lint each candidate packet, then
ask `conductor.py wave` for a mutually disjoint subset of
`dispatchable` write nodes. Empty `paths` overlap everything.
`max_inflight` SHALL apply after disjointness. If that subset has
two or more nodes, it SHALL `take` each node before launch, SHALL
launch the `run-wave` workflow with those nodes (packet paths in
`args.nodes`) on HEAD, and SHALL release every taken node if the
launch is infra-red. After the workflow joins, the conductor SHALL
persist each node's `constraints.paths` sequentially on HEAD, then
classify / close / repair / park. A single-node wave SHALL use the
existing single `act` path. Claude and Codex assignees SHALL still
receive `spawn.py` adapters. Host `isolation_worktree` SHALL NOT be
the persist path. Wave children SHALL NOT `conductor.py isolate`
while worktree land is PARKED. Shared-file extraction (ultrapilot
owned vs shared) SHALL NOT land in this slice. `/run-wave` SHALL
be a user-invocable skill at `plugins/intention/skills/run-wave/`
(`.agents/skills/run-wave` in this clone) that runs the same
fan-out without the campaign loop.

#### Scenario: /run-wave is a skill

- GIVEN a clone of this repo
- WHEN Grok starts in the repo root
- THEN it discovers `run-wave` from `.agents/skills/`
- AND the skill fans `conductor.py wave` of size ≥ 2 on HEAD

#### Scenario: Two disjoint writes fan out

- GIVEN `next: act` and `conductor.py wave` lists two nodes whose
  `paths` do not overlap
- WHEN this host has `workflow`
- THEN `run` launches `run-wave` with both node ids
- AND each node was `take`n before launch
- AND neither child isolates a worktree

#### Scenario: Overlapping dispatchable is not a wave of two

- GIVEN two `dispatchable` nodes that share a path
- WHEN `conductor.py wave` runs
- THEN the wave contains only the first of those two

#### Scenario: Two path-less nodes are not a wave of two

- GIVEN two `dispatchable` nodes whose `paths` are empty
- WHEN `conductor.py wave` runs
- THEN empty `paths` overlap everything
- AND the wave contains at most one of those nodes

#### Scenario: Cap applies after disjointness

- GIVEN `max_inflight` 2 and ready nodes `a(x)`, `b(x)`, `c(y)`
- WHEN `conductor.py wave` runs
- THEN the wave is `[a, c]`, not `[a]`

#### Scenario: Infra-red launch releases every take

- GIVEN two wave nodes already `take`n
- WHEN `workflow` fails to launch
- THEN the conductor `release`s both nodes before the campaign continues
