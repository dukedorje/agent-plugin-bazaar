## ADDED Requirements

### Requirement: run wave fans disjoint act nodes

When the campaign's `next` is `act` and this host provides
`workflow`, `run` SHALL ask `conductor.py wave` for a mutually
disjoint subset of `dispatchable` write nodes. If that subset has
two or more nodes, it SHALL launch the `run-wave` workflow with
those nodes (packet paths in `args.nodes`) and SHALL `take` each
node before launch. A single-node wave SHALL use the existing
single `act` path. Claude and Codex assignees SHALL still receive
`spawn.py` adapters. Host `isolation_worktree` SHALL NOT be the
persist path.

#### Scenario: Two disjoint writes fan out

- GIVEN `next: act` and `conductor.py wave` lists two nodes whose
  `paths` do not overlap
- WHEN this host has `workflow`
- THEN `run` launches `run-wave` with both node ids
- AND each node was `take`n before launch

#### Scenario: Overlapping dispatchable is not a wave of two

- GIVEN two `dispatchable` nodes that share a path
- WHEN `conductor.py wave` runs
- THEN the wave contains only the first of those two
