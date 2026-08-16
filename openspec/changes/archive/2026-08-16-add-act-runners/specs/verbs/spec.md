## ADDED Requirements

### Requirement: act stages a unique prompt file

`act` SHALL launch a worker only after
`plugins/intention/scripts/spawn.py stage` has written a unique
prompt file. The prompt file SHALL be non-empty. A missing or empty
prompt SHALL fail before any worker starts. Two stages SHALL not share
a path.

#### Scenario: Empty prompt never launches

- GIVEN `spawn.py` is asked to run a spec whose `prompt_file` is
  missing or zero bytes
- WHEN `run` starts
- THEN it exits non-zero and no adapter process is started

### Requirement: stall is infra-red

If a spawned adapter exceeds `timeout_sec`, `spawn.py` SHALL kill it
and emit a distilled face with `disposition: infra-red` and a stall
blocker. It SHALL NOT blame the node's code.

#### Scenario: Sleep past timeout

- GIVEN an exec adapter that sleeps longer than `timeout_sec`
- WHEN `spawn.py run` finishes
- THEN the face disposition is `infra-red`

### Requirement: packet-only gets no slash command

A `surface: packet-only` (or cloud `interface`) prompt SHALL contain
the inlined packet and SHALL NOT contain `/act`, `/intend`, or
`/meta-execute`.

#### Scenario: Codex-shaped stage

- GIVEN a packet with `surface: packet-only`
- WHEN `spawn.py stage` writes the prompt
- THEN the prompt has no `/act` and names the packet path
