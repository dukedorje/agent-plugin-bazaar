# verbs

What each dispatcher must produce. Folded from `deepen-verbs` on
2026-08-15 (S1–S4). Hosting is `packaging`. The agent surface is
`docs/contracts/`. This spec does not duplicate either.

## Purpose

`intend`, `change`, `advise`, `act`, and `fold` are complementary. They share
`plugins/intention/references/shared.md`. None redefines the packet.

## ADDED Requirements

### Requirement: intend emits a DAG

`intend` SHALL observe living specs, in-flight changes, and learnings,
orient (load class × blast × lifecycle), and emit a DAG of nodes whose
landings are a verb-led change-id, `brief`, or `direct fix`. It SHALL NOT
implement, write SHALLs, or create `docs/sprints/`. Restore-only work
SHALL stop at `direct fix`.

#### Scenario: A goal becomes named landings

- GIVEN an intention that needs new behavior
- WHEN `intend` finishes
- THEN the ready-set names change-ids (or brief / direct fix), each with
  one acceptance surface, and no code has been written for architecture
  nodes that still need activation

### Requirement: change scaffolds OpenSpec-lite

`change` SHALL write `openspec/changes/<id>/{proposal,tasks}.md` and
delta specs. `proposal.md` SHALL start with `PENDING` or `ACTIVE BUILD`
and SHALL include a journey or `No new UI because <reason>`. It SHALL
skip scaffolding for restore-only work. It SHALL NOT fold.

#### Scenario: New behavior gets a PENDING change

- GIVEN a change-id from `intend`
- WHEN `change` runs and the human has not activated
- THEN `openspec/changes/<id>/proposal.md` exists with `> **PENDING**`
  and a journey section

### Requirement: act uses packets

`act` SHALL write a task packet and a signed result (solo on the bead
or in chat; groups under `groups/<id>/`). It SHALL NOT write `.omc/`.
Foreign harnesses SHALL receive that packet, never a slash command.
Edits SHALL commit-on-red on exact paths. Focused verify SHALL be the
only task gate.

#### Scenario: Codex is assigned a node

- GIVEN `act` routes a node to Codex
- WHEN it dispatches
- THEN Codex is given the packet (bead note, chat, or
  `groups/<id>/packet.json`), not `/act`

### Requirement: fold archives

`fold` SHALL apply deltas to `openspec/specs/`, move the change to
`openspec/changes/archive/YYYY-MM-DD-<id>/`, amend `ARCHITECTURE.md`
when shape changed, and append surprises to `docs/LEARNINGS.md`. It
SHALL refuse PENDING and PARKED.

#### Scenario: Active change after act

- GIVEN `openspec/changes/<id>/` is ACTIVE BUILD and owed tasks are done
- WHEN `fold` finishes
- THEN `openspec/changes/<id>/` is gone, the archive directory exists,
  and every SHALL from the deltas appears in `openspec/specs/`

### Requirement: advise is the read between change and act

`advise` SHALL load an in-flight change, assign a review-pair from
`ladder.json` (`architecture-review` reader, optional Fable consult),
and write `openspec/changes/<id>/reviews/<date>-advise.md` plus a
signed result with `permission: read`. It SHALL NOT edit product
paths, fold, or implement nits. Verdict SHALL be `accept`,
`accept-with-nits`, or `send-back`. `send-back` SHALL add owed boxes
on the change and SHALL NOT flip the banner. The change author SHALL
NOT be the sole accepting reader.

#### Scenario: Architecture change after scaffold

- GIVEN `openspec/changes/add-buzz-local-client/` is ACTIVE BUILD
- WHEN `advise` runs
- THEN a review file exists under `reviews/`
- AND no file under `lib/` or `native/` was edited

#### Scenario: Send-back blocks act

- GIVEN the last advise verdict is `send-back`
- WHEN `conductor.py ready` lists implement nodes of that change
- THEN they are not `dispatchable`

### Requirement: Shared references, not four surfaces

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`, and
`ready` SHALL load `plugins/intention/references/shared.md` and
SHALL NOT restate packet fields or topology wirings. Adding a tenth
law to a skill body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`

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

### Requirement: intend and act resolve the ladder file

`intend` and `act` SHALL assign workers from
`plugins/intention/references/ladder.json` via
`plugins/intention/scripts/ladder.py assign --shape <shape>`.
They SHALL NOT invent a second assignment table. An explicit human
pick always wins.

#### Scenario: Known coding task

- GIVEN shape `known`
- WHEN `ladder.py assign --shape known` runs
- THEN the assignee is Claude Sonnet 5 (`skill-host`, density
  `explicit`)

#### Scenario: Architecture review is cross-family

- GIVEN shape `architecture-review`
- WHEN assign runs
- THEN the default reader is Grok, and GPT-5.6 Sol is not selected
  while `available` is false

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
