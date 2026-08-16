## ADDED Requirements

### Requirement: take is the node mutex

`act` SHALL call `conductor.py take` before staging a write worker.
`take` marks the node `in_progress`, records the holder, and holds
its `constraints.paths`. A second take of the same node SHALL fail.
`release` frees the slot. Overlapping write-sets stay `deferred`.

#### Scenario: Second take is rejected

- GIVEN node C is dispatchable
- WHEN `take --node C` succeeds and is run again
- THEN the second take exits non-zero and C stays `in_progress`

### Requirement: max_inflight caps background workers

`conductor.py ready` SHALL treat `in_progress` count against
`max_inflight` from `ladder.json`, then `ACT_MAX_INFLIGHT`, then
`--max-inflight`. When no slot remains, otherwise-ready nodes SHALL
be `capped`, not `dispatchable`.

#### Scenario: Cap of one

- GIVEN one `in_progress` node and `--max-inflight 1`
- WHEN ready runs
- THEN other open disjoint nodes are `capped`

### Requirement: claude adapter is live print mode

`spawn.py run --adapter claude` SHALL invoke `claude -p` with
`--model` and `--effort` from the spec interface (sonnet-5 /
opus-5 / fable-5). Packet-only runs SHALL pass
`--disable-slash-commands`. Tests MAY stub the binary.

#### Scenario: Stub records print mode

- GIVEN a fake `claude` on PATH
- WHEN `run --adapter claude` executes
- THEN the fake argv includes `-p` and the model id
