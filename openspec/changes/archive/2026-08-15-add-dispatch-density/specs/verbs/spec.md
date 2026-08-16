## ADDED Requirements

### Requirement: intend emits density

`intend` SHALL set `density` on each node (lean / standard / explicit)
from `docs/contracts/dispatch.md`. Blast may raise density, never lower
it. A weaker assignee MAY consult a stronger model for `explain` or
`replan`; it SHALL NOT hand off the write.

#### Scenario: Flash node is explicit

- GIVEN `intend` assigns a mechanical node to a cheap / explicit-tier
  worker
- WHEN the DAG is written
- THEN that node names `density: explicit` and one focused acceptance

### Requirement: act reads the distilled face

`act` SHALL treat `distilled` (or the output of
`plugins/intention/scripts/distill-result.py`) as the conductor's
default read. The full report remains at `raw_ref`. The conductor of
an isolation boundary SHALL persist; workers inside that boundary SHALL
NOT be told "do not commit" in the packet.

#### Scenario: Conductor does not open the transcript

- GIVEN a worker returned a signed result with `raw_ref`
- WHEN the conductor classifies the node
- THEN it reads `distilled` and only opens `raw_ref` when investigating
