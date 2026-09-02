# verbs

What each dispatcher must produce. Folded from `deepen-verbs` on
2026-08-15 (S1–S4), later `add-intend-extract` and
`update-run-stages` on 2026-08-18, `update-run-ooda` and
`update-run-gates` on 2026-08-19. Hosting is `packaging`. The
agent surface is `docs/contracts/`. This spec does not duplicate
either.

## Purpose

`intend`, `change`, `advise`, `act`, `fold`, `brief`, `ready`, `run`,
and `consult` are complementary. They share
`plugins/intention/references/shared.md`. None redefines the packet.
`run` is the campaign; the others are stages (or observe / disposable
decide).

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
paths, fold, or implement leftover notes. Verdict SHALL be `accept`
or `send-back`. Notes belong in the review body, not in the
verdict. A historical `accept-with-nits` banner SHALL still count
as `accept`. `send-back` SHALL add owed boxes
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

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`,
`debrief`, `map`, `ready`, and `run` SHALL load
`plugins/intention/references/shared.md` and SHALL NOT restate
packet fields or topology wirings. Adding a tenth law to a skill
body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`

### Requirement: run conducts a campaign

`run` SHALL walk the ready-set under a stop policy (`--until`,
`--autonomous`, `--pause-before`, `--max-inflight`) and SHALL invoke
stage verbs by reading `plugins/intention/skills/<stage>/SKILL.md` at
the wave it enters that stage. It SHALL accept an optional scope.
It SHALL set `next` from this decision table (not a preference
order). A **verb-led change-id** is a kebab matching
`^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$`. Any
other scope SHALL be a **goal**.

- `intend` when the scope is a goal, or when a surprise needs a
  new Observe
- `change` when the scope is a verb-led change-id that has no
  `openspec/changes/<id>/` directory
- `advise` when that change is ACTIVE BUILD architecture/instrument
  with no accepting review
- `act` when the change is dispatchable write work
- `fold` when `--until fold` (or equivalent) is set and fold is
  legal: banner `ACTIVE BUILD`, no open owed checkbox, not
  `PARKED`

`ready` SHALL remain the card's observe, not a `next` stage.
`brief` SHALL remain disposable and SHALL NOT be a campaign stage.

It SHALL NOT inline those skill bodies into `run/SKILL.md`. It SHALL
NOT implement a node except by dispatching `act`. It SHALL NOT fold
except when `--until fold` (or equivalent) is set and fold is legal.
It SHALL NOT flip a PENDING banner. Foreign harnesses SHALL receive
a task packet and SHALL NOT receive `/run`. `workers_launched` SHALL
stay 0.

`stop: no-ready` SHALL mean the observe script is missing. A missing
`openspec/` tree with a named verb-led change-id SHALL be
`next: change`, not `no-ready`. A missing `openspec/` tree with a
goal that is not a change-id SHALL be `next: intend`, not
`no-ready`.

`--until advise` SHALL dispatch `next: advise` when a read is owed
and SHALL NOT dispatch `act`. `--until activation` SHALL stop on
PENDING. `--until empty` SHALL walk change → advise → act until
nothing is dispatchable.

`--autonomous` SHALL suppress mid-run questions, route judgment
through consult-before-ask, defer by-eye gates to an EYES list, and
SHALL NOT flip a human-verify box or perform deploy / force-push /
secret-exposing work. A veto or true blocker SHALL park that subject
and SHALL NOT stop unrelated dispatchable nodes unless `--until ask`.

#### Scenario: Named landing has no change directory

- GIVEN `/run add-sheaf-type` and no `openspec/changes/add-sheaf-type/`
- WHEN `run.py` observes
- THEN the card has `next: change` and `focus: add-sheaf-type`
- AND `stop` is not `no-ready`

#### Scenario: Goal is not a change-id

- GIVEN `/run we need extract-from on intend` and that string is
  not a verb-led change-id
- WHEN `run.py` observes
- THEN the card has `next: intend`
- AND `workers_launched` is 0

#### Scenario: Until fold when fold is legal

- GIVEN `--until fold` and an ACTIVE BUILD change whose owed boxes
  are checked
- WHEN `run.py` observes
- THEN the card has `next: fold`
- AND no worker is launched

#### Scenario: Architecture owes a read before a write

- GIVEN `add-x` is ACTIVE BUILD, in `needs_advise`, and also has
  open owed boxes
- WHEN `run` observes with `--until empty`
- THEN `next` is `advise`, not `act`

#### Scenario: Until advise runs the read and not the write

- GIVEN dispatchable write nodes and `--until advise`
- WHEN a read is owed
- THEN `next` is `advise` and no PENDING banner is flipped
- AND `act` is not dispatched

#### Scenario: Until advise with no read owed

- GIVEN ready write nodes, no `needs_advise`, and `--until advise`
- WHEN `run` observes
- THEN it stops and does not set `next: act`

#### Scenario: Autonomous does not forge eyes

- GIVEN `--autonomous` and a node whose acceptance is by-eye
- WHEN that node is reached
- THEN the box stays unchecked, the item is listed under EYES, and
  the run continues elsewhere if anything else is dispatchable

#### Scenario: Foreign worker never sees /run

- GIVEN `run` assigns a node to Codex
- WHEN it dispatches
- THEN Codex is given a packet, not `/run` or `/act`

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
the inlined packet and SHALL NOT contain `/act`, `/intend`,
`/meta-execute`, or `/run`.

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

#### Scenario: Architecture review default reader

- GIVEN shape `architecture-review`
- WHEN assign runs
- THEN the default reader is Claude Fable 5.1, Grok remains
  available as a cross-family pick, and GPT-5.6 Sol is not selected
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
opus-5 / fable-5.1). The prompt SHALL be written to stdin, not
argv. Packet-only runs SHALL pass `--disable-slash-commands`.
Tests MAY stub the binary.

#### Scenario: Stub records print mode

- GIVEN a fake `claude` on PATH
- WHEN `run --adapter claude` executes
- THEN the fake argv includes `-p` and the model id
- AND the prompt body is on stdin, not argv

### Requirement: codex adapter is live exec stdin

`spawn.py run --adapter codex` SHALL invoke `codex exec -` with
the prompt on stdin, not argv. Shared effort SHALL map to
`-c model_reasoning_effort`. Tests MAY stub the binary.

#### Scenario: Stub records stdin prompt

- GIVEN a fake `codex` on PATH
- WHEN `run --adapter codex` executes
- THEN the fake argv ends with `-`
- AND the prompt body is on stdin, not argv

### Requirement: consult is a second opinion, not advise

`spawn.py consult` SHALL ask spawnable ladder readers (default
shape `architecture-review`) with the brief on stdin / `--goal`.
It SHALL NOT write `openspec/changes/*/reviews/`, flip a banner, or
unblock `act`. `--panel` SHALL fan out every spawnable reader.
`--id` is a human pick. Unspawnable harnesses (no CLI adapter)
SHALL be skipped. Verdicts SHALL be `agree` / `caution` / `dissent`.

#### Scenario: Stub consult is not advise

- GIVEN a fake `claude` on PATH and `--id fable-5.1-arch-review`
- WHEN `consult --goal "…" ` executes
- THEN the prompt asks for `CONSULT:` not `ADVISE:`
- AND stdout is opinions JSON, not a change review file

### Requirement: intend extract-from named items

When `intend` is given `--extract-from` with one or more items, it
SHALL observe those items before orient and split. Usual items SHALL
be bead ids and epic ids. Observe SHALL report records of action
(descriptions, acceptance, comments, close reasons, signed results,
blocking edges that resolve) and insight into the intent those
records imply. It SHALL NOT dump full transcripts into the DAG. It
SHALL NOT implement. A missing or unreadable item SHALL be named as
unresolved and SHALL NOT be invented. Absence of the flag SHALL keep
today’s observe (living specs, in-flight changes, learnings).

#### Scenario: Extract from an epic

- GIVEN epic `bazaar-db8` has children, comments, and a close on
  `bazaar-db8.1`
- WHEN `intend --extract-from bazaar-db8` runs
- THEN the output includes action records from that epic and insight
  into intent
- AND then Orient and a DAG
- AND no product paths were edited for architecture nodes that still
  need activation

#### Scenario: No flag stays blank-page

- GIVEN no `--extract-from`
- WHEN `intend` runs
- THEN observe is living specs, in-flight changes, and learnings
- AND the run is not rejected for lacking extract-from

#### Scenario: Missing item is named

- GIVEN `--extract-from` names an id that does not resolve
- WHEN `intend` observes
- THEN that id is reported unresolved
- AND no invented trail is presented as fact

### Requirement: run gate defaults

`--until roll` SHALL be the default walk: fold-legal inflight →
send-back amend → advise → act → bead landing/`change` → leftover
task/`intend`. It SHALL park ASK / EYES / PENDING on the card `ask`
list and SHALL continue unrelated dispatchable work. It SHALL NOT
stop on elicitation. It SHALL NOT flip PENDING or by-eye boxes.

`--until empty` SHALL be the cautious walk: `change` → `advise` →
`act`. It SHALL stop at PENDING, ASK, and fold. It SHALL NOT emit
`next: fold`. It SHALL NOT emit `next: intend` unless the scope
fails the verb-led change-id detector named by `update-run-ooda`
(`^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$`).

`--until fold` SHALL use that same change's legal-fold predicate
(ACTIVE BUILD, no open owed checkbox, not PARKED). It SHALL NOT
define a second fold rule. Unscoped `--until fold` SHALL scan
inflight for that predicate. `--until advise`, `--until activation`,
and `--until ask` SHALL keep their existing stop meanings.

`--autonomous` SHALL suppress mid-run questions and SHALL NOT flip
PENDING or by-eye boxes. Alone it SHALL use the default walk
(`--until roll`). Combined with an explicit `--until` it SHALL use
that walk. It SHALL NOT deploy.

#### Scenario: Empty does not fold

- GIVEN `--until empty` and an ACTIVE BUILD change whose owed boxes
  are checked
- WHEN `run.py` observes
- THEN `next` is not `fold`
- AND the card stops empty if nothing else is dispatchable

#### Scenario: Empty does not intend a change-id

- GIVEN `--until empty` and scope `add-x` which is a verb-led
  change-id
- WHEN `run.py` observes
- THEN `next` is not `intend`

#### Scenario: Until fold cites ooda's legal-fold predicate

- GIVEN `--until fold` and a change that is ACTIVE BUILD, has no
  open owed checkbox, and is not PARKED
- WHEN `run.py` observes
- THEN fold is legal under the predicate `update-run-ooda` named
- AND this requirement does not invent a second predicate

#### Scenario: Autonomous does not flip PENDING

- GIVEN `--autonomous` and a PENDING change
- WHEN `run` would next owe activation
- THEN the banner stays PENDING
- AND `next` is not `act`

#### Scenario: Bare run uses the roll table

- GIVEN no `--until` and `openspec/changes/add-x/` is fold-legal
- WHEN `run.py` observes unscoped
- THEN `next` is `fold` and `focus` is `add-x`

### Requirement: debrief expands a finished or failed unit

`debrief` SHALL take a just-finished or failed unit (bead id,
change-id, or signed result) and emit an expansion: what happened,
context the brief did not have, takeaways, and what the next
`intend` should extract. It SHALL stop so a human can process. It
SHALL NOT implement, fold, or treat the debrief page as durable
truth. Hard-won facts SHALL go to `docs/LEARNINGS.md` as one dated
line each. It SHALL NOT be a default `/run` wave.

#### Scenario: Finished unit

- GIVEN a closed bead or a signed result with `disposition: pass`
- WHEN `debrief` runs on that id
- THEN the output names what landed, takeaways, and what intend
  should extract
- AND no product paths were edited

#### Scenario: Failed unit

- GIVEN a signed result with `disposition` other than `pass`, or a
  parked / task-red node
- WHEN `debrief` runs on that id
- THEN the output names what was tried, what broke, takeaways, and
  what intend should extract
- AND the banner of any in-flight change is unchanged

#### Scenario: Debrief is not a spec

- GIVEN a debrief page from last week
- WHEN an agent cites it as current behavior
- THEN that citation is wrong; living spec, ADR, or LEARNINGS.md is
  the residue
### Requirement: map reprints the intend DAG with live residue

`map` SHALL print the intend-dag shape (intention, orient if known,
per-node goal/landing/deps, ready-set, needs activation, next) plus
live **Status**, **Wave**, and **Outcome** for each node. Status
SHALL come from the tracker. Wave SHALL name the last known stage
(change banner, advise verdict, act disposition, fold/archive).
Outcome SHALL be the signed result `distilled.summary` or the bead
close reason. It SHALL NOT implement, unpark, or invent a second
store. It SHALL NOT be a default `/run` wave.

No scope SHALL list open epics and their children. A named epic,
bead, or change-id SHALL focus that graph.

#### Scenario: Map an epic

- GIVEN epic `bazaar-6os` has a closed child `add-debrief-verb`
- WHEN `map bazaar-6os` runs
- THEN the page has a DAG node for that child
- AND Status is closed
- AND Outcome is the close reason or distilled summary

#### Scenario: Map invents no tracker

- GIVEN a proposal stores map state in a new file besides beads
  and openspec
- WHEN it is reviewed
- THEN it is rejected against this requirement
### Requirement: run roll walks while unblocked

`--until roll` SHALL observe openspec banners and unblocked beads
and SHALL set `next` from this table, first match wins:

1. fold-legal inflight change (no scope required) → `fold`
2. last advise is `send-back` on an ACTIVE BUILD change → `change`
3. `needs_advise` → `advise`
4. READY write → `act`
5. unblocked bead whose title names a verb-led change-id and that
   directory does not exist → `change`
6. unblocked task or feature bead with no verb-led landing, that
   is not an epic and whose title does not start with `nod-` →
   `intend` (focus is that bead id)
7. else stop empty

It SHALL NOT intend epics. It SHALL NOT flip PENDING. Epics and
`nod-` titles SHALL NOT auto-intend. `workers_launched` SHALL stay 0.

Unscoped `--until fold` SHALL scan inflight for fold-legal and
SHALL set `next: fold` on the first hit.

#### Scenario: Unscoped fold finds a legal change

- GIVEN `--until fold` or `--until roll`, no scope, and
  `openspec/changes/add-x/` is fold-legal
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`

#### Scenario: Send-back is amend not act

- GIVEN `--until roll` and `add-x` is ACTIVE BUILD whose last
  advise is `send-back`, and `add-x` is also READY
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-x`

#### Scenario: Bead landing with no change dir

- GIVEN `--until roll`, no READY writes, and an unblocked bead
  titled `add-tatastu-host: …` with no `openspec/changes/add-tatastu-host/`
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-tatastu-host`

#### Scenario: Epic does not auto-intend

- GIVEN `--until roll` and the only unblocked bead is an epic
- WHEN `run.py` observes
- THEN `next` is not `intend`
### Requirement: until ask is a roll that stops on elicitation

`--until ask` SHALL use the same observe table as `--until roll`.
It SHALL stop (`stop: ask`, `next` null) on the first elicitation:
an `ask` id on the observe face, a PENDING change, or an open owed
box matching ASK / EYES / by-eye / human-verify. A stage SHALL
raise an elicitation on that face (JSON `ask`, or such an owed
box). It SHALL NOT invent an `/ask` verb or a fourth store.

`--until roll` SHALL not stop on elicitation. It SHALL keep those
ids on the card `ask` list and SHALL continue unrelated
dispatchable work. It SHALL NOT flip PENDING or by-eye boxes.

#### Scenario: Ask stops while work remains

- GIVEN `--until ask`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask` (or activation-class)
- AND `next` is not `act`

#### Scenario: Ask without elicitation rolls

- GIVEN `--until ask`, no PENDING, no ask ids, and an unblocked
  bead titled `add-tatastu-host: …` with no change dir
- WHEN `run.py` observes
- THEN `next` is `change` and `focus` is `add-tatastu-host`

#### Scenario: Roll keeps the morning list

- GIVEN `--until roll`, PENDING `add-y`, and READY `add-x`
- WHEN `run.py` observes
- THEN `next` is `act` and `focus` is `add-x`
- AND `add-y` is listed under `ask` or `waiting`
### Requirement: second-family advise is spawned, not parked

When `next` is `advise` and this session’s harness is the same family
as the change author, `run` SHALL assign an available
`architecture-review` route whose `harness` differs from the author
(`ladder.py assign --shape architecture-review --not-harness <author>`)
and SHALL spawn that reader (packet + `spawn.py`). It SHALL wait for
that wave so the review can land, then re-observe. It SHALL NOT halt.
It SHALL NOT `--punt` that id unless no other-family route is
available or the spawn is `infra-red` after one retry. It SHALL NOT
write a sole-author `accept` or a fake `send-back` with no
architecture boxes. `--until roll` SHALL NOT treat same-family advise
as stuck or as an ASK park. `--punt` SHALL NOT be the first response
to ADR-005.

`advise` SHALL treat second family as any `architecture-review` harness
other than the author’s. A Grok-authored change SHALL spawn a Claude
reader when that route is available. A Claude-authored change SHALL
spawn Grok or Sol. “Sol unavailable” SHALL NOT mean no second family
while a Claude or Grok route remains available.

#### Scenario: Grok author, roll, Fable available

- GIVEN `--until roll`, Grok authored `add-x`, `add-x` is in
  `needs_advise`, and `sol-arch-review` is unavailable
- WHEN the conductor’s session is Grok
- THEN `next` is `advise` and the conductor spawns the Claude
  `architecture-review` route
- AND the campaign does not stop empty
- AND `add-x` is not `--punt`ed

#### Scenario: No other-family route

- GIVEN `next: advise` and `ladder.py assign --shape architecture-review --not-harness <author>` fails
- WHEN the conductor cannot spawn a different family
- THEN it `--punt`s that id
- AND it does not write a fake send-back
### Requirement: run operator flags

Bare `/run` SHALL use the roll walk. `--interrupt` SHALL use that
same walk and SHALL stop at the first elicitation (ASK box, PENDING,
EYES / by-eye / human-verify). `--only fold` SHALL scan fold-legal
inflight and SHALL not `act`. `--no-fold` SHALL skip fold picks.
`--no-beads` SHALL skip bead landing and leftover intend. Combined
`--no-fold --no-beads` SHALL match `--until empty`. `--until` tokens
SHALL remain aliases for one release (`roll` is a no-op for the
default). `--autonomous` SHALL NOT change the walk. `--until
activation` SHALL NOT be required; PENDING is an elicitation.

#### Scenario: Interrupt stops while work remains

- GIVEN `--interrupt`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask`
- AND `next` is not `act`

#### Scenario: Only fold

- GIVEN `--only fold`, no scope, and fold-legal `add-x`
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`

#### Scenario: No-fold no-beads is empty walk

- GIVEN `--no-fold --no-beads` and fold-legal `add-x` with no other
  dispatchable work
- WHEN `run.py` observes
- THEN `next` is not `fold`
### Requirement: wait and tidy are the operator names

`--wait` SHALL be desk mode: the roll walk, stopping at the first
elicitation. `--tidy` SHALL scan fold-legal inflight and SHALL not
`act`. `--interrupt` SHALL be an alias of `--wait`. `--only fold`
SHALL be an alias of `--tidy`. The observe verb SHALL be `status`.
`ready` SHALL remain an alias of `status`.

#### Scenario: Wait stops while work remains

- GIVEN `--wait`, READY `add-x`, and PENDING `add-y`
- WHEN `run.py` observes
- THEN `stop` is `ask`
- AND `next` is not `act`

#### Scenario: Tidy is fold-only

- GIVEN `--tidy`, no scope, and fold-legal `add-x`
- WHEN `run.py` observes
- THEN `next` is `fold` and `focus` is `add-x`
