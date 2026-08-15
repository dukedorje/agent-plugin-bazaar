# From intention to a running system

A work algebra for humans and agents. Documents are projections of the graph. The graph is the work.

This file is two things at once: the user-facing explanation, and the first use of the method on itself. Later it will be split into site explainers, skill references, and interactive pieces. Until then it is the source.

---

## The claim

Intention becomes running software by circulating a short loop over a directed graph of work.

The loop is Boyd’s: **observe → orient → decide → act**, then observe what the act did. Tempo beats completeness. Orientation can skip an explicit Decide when the shape is already clear — that is “steer on vibes,” with a name.

The graph is not a sprint backlog and not a folder of novels. It is a set of **nodes** (intentions, capabilities, changes, work items, evidence) and **verbs** (split, assign, activate, act, verify, fold, learn, park, fork, weave). Nodes are carried by living specs and a tracker. Verbs are carried by a small set of skills.

**Ceremony is a function of what is being mutated**, not of “we are in planning.” A typo does not earn a requirements document. A new money path does not earn vibes.

Three durable artifacts survive any loop:

| Artifact | Question |
|---|---|
| `ARCHITECTURE.md` | Why is it shaped this way? |
| a work graph (beads, or anything that can answer *ready*) | What is the state of the work? |
| `docs/LEARNINGS.md` | What did we learn the hard way? |

Plus one disposable page per unit of work: a **brief**. If it is 200 lines, it is a story template wearing a brief’s clothes.

Everything else — personas, readiness reports, As-a/I-want restatements, status enums in markdown, velocity formulas — is scaffolding for a weaker model generation. Keep the density that late stories actually earned: real signatures, inherited gotchas, explicit out-of-scope. Drop the template.

---

## Why this exists

The previous default in this marketplace, `/sprint-plan`, is a document factory. It copies a software-sprint ritual: discovery, requirements, scoping, UX, architecture, epics, stories, a write-stories gate, validation, optional materialization into beads.

Ceremony tiers (`lean` / `standard` / `full`) were added because the factory was too much. They help, but they are a routing overlay on Scrum-shaped phases. Invoke the skill and you still stand up directories, fan out planners, and can escalate a three-task idea into a novel the moment a HIGH decision appears.

That ritual was rational when models needed the goal restated three ways. It is no longer the failure mode. The remaining failures are different:

| Failure | What actually fixes it |
|---|---|
| The model invents a plausible-but-wrong API | A **contract** pasted from real docs or source |
| The model re-learns a painful fact | **LEARNINGS.md**, carried into the brief |
| The model does adjacent work | **Out of scope**, named and tracked elsewhere |
| The model satisfies the check and defeats the intention | **Discriminating evidence** — a check that would look different if the claim were false |
| Process docs lie about what is built | **Two-layer truth**: living specs vs in-flight changes, status *in the file* |
| A multi-agent tree leaves unowned dirty files | **Commit-on-red**, exact paths, one write door for graph state |

This system is built to fix those, and to stay quiet the rest of the time.

---

## Lineage

Nothing here is invented from a blank page. Four working systems were observed, then oriented.

### Morphist conventions

Already voted. A project needs architecture, a tracker, and learnings. Briefs are disposable. Sprint-plan remains useful only as a resumable batch planner for work that is genuinely large. Lean-and-beads is the honest small path; it just was not the default when someone said “let’s build this.”

### Tatastu / OpenSpec

The right *document* model.

- `specs/` is what **is** built. It is the only source of truth for behavior.
- `changes/` is what **should** change. Deltas, not rewrites: `ADDED` / `MODIFIED` / `REMOVED`.
- `documents/` may reason and sequence. They never carry a requirement without naming a change-id.
- Status lives in the file (`PENDING`, `ACTIVE`, `PARKED`) because retrieval strips paths.
- Humans **activate** work. Agents draft. A directory listing is not a mandate.
- Done is **fold + archive**, not “the PR merged.”
- Restore-only fixes skip the ritual.
- A user-facing change is not done until the journey was exercised from a real entry surface.

Tatastu also shows the cost of copying this too faithfully: archive lag made shipped work look pending; mega-proposals rotted; a capability archived with tests and no way in. Steal the two-layer truth, deltas, in-file disposition, human activation, and fold-as-done. Do not steal the disposition encyclopedia until those failure modes appear. Enforce the few rules with one hygiene script.

### MetaCoding

The ontology, not the ritual.

A codebase **is** a category: symbols are objects, typed edges are morphisms, path concatenation is composition. Intention is a **one-way enrichment** over frozen structure. Names never renegotiate the partition.

| Idea | Plugin-thin form |
|---|---|
| Structure first, meaning second | Observe the shape, then name the purpose |
| Boundary = crossing morphisms | An interface is what crosses the module edge, not a wishful doc |
| Composition laws | Builders need the algebra of how pieces combine, not a component list |
| Intention harvest | Tests, errors, constants, and WHY-comments are executable or near-executable intention |
| Load class | `structure-clear` / `intention-critical` / `ambiguous` |
| Instrument vs measured | Full adversarial weight only when changing the measuring stick |

With a live oracle, static briefs measured near zero during the build itself. Category-theoretic machinery earns keep in **scoping, finding, deciding, auditing** — not as a mid-implementation chat ritual. Do not ship colimits as a default skill step.

### MetaDev

The right *execution* contracts.

- A plan is not permission. Default stop before code.
- One write door for plan/graph state. Checkbox ceremony records readiness; it does not create it.
- The task’s declared focused verify is the whole acceptance surface. Suites are not task gates.
- Persistence and acceptance are separate. Workers commit the paths they touched, including on red.
- Failures classify: a causal red parks a branch; a baseline red and an infra red do not stop the graph.
- Plan depth is inverse to model strength. Strong models get lean plans. Weak/cheap workers get explicit sketches.
- Foreign harnesses receive **tasks**, never slash commands.
- Assignment is by task shape, not brand loyalty.

Do not port the airport: dashboard, inbox, overlord, forty commands. Take the contracts.

### OODA

The runtime. Observe the world (code, specs, people, evidence). Orient through load class, blast radius, and lifecycle stage. Decide the split, the rigor, the assignment, whether to open a group. Act. The act becomes the next observation.

Boyd’s supporting principles, used without costume:

- **Variety** — more than one path where a single orientation is likely a local maximum. Not everywhere.
- **Rapidity** — short loops, focused verifies, no suite-as-gate.
- **Harmony** — commander’s intent (outcome + non-goals) so nodes do not need a novel.
- **Initiative** — `structure-clear` work proceeds without a meeting.

---

## The loop

```
INTENTION     commander’s intent: outcome, non-goals, constraints
    │
    ▼
OBSERVE       code, tests, living specs, ready-set, learnings, who is available
    │
    ▼
ORIENT        load class × lifecycle × blast radius → rigor, and whether a group
    │
    ▼
DECIDE        split into a DAG; assign; activate (human) or auto (low severity)
    │
    ▼
ACT           one worker or group per ready node; focused verify; commit-on-red
    │
    └──► fold into specs + architecture + learnings; park or regroup on surprise
```

This is not a waterfall walked once. Every node runs the loop. A surprise mid-act is a new Observe, not a process violation.

### Rigor is a dial, not a phase

| Lifecycle / blast | Default rigor | What you write |
|---|---|---|
| Typo, restore intended behavior, pin, copy | **vibe** | nothing, or a bead |
| One unit, known shape, few files | **brief** | disposable page: goal, acceptance, contract, inherited, out of scope |
| New or changed user-visible behavior | **change** | a delta + tasks + one journey |
| New subsystem, protocol, schema, auth, money | **architecture** | ADR in `ARCHITECTURE.md` + a change + a spike if unvalidated |
| Tests, oracles, judges, kernel, “what counts as done” | **instrument** | a property-red, “how would I fake this?”, an independent reader |

Ceremony **escalates only**. It never silently grows a vibe-fix into a sprint.

Load class, from MetaCoding, is the other axis of Orient:

| Load class | Agent posture |
|---|---|
| `structure-clear` | The graph already determines behavior. Steer on vibes. Implement the shape. |
| `intention-critical` | Structure underdetermines the why. Read tests, errors, constants. Do not invent business rules from a call graph. |
| `ambiguous` | Stop for a human. |

Instrument vs measured is the third axis. Changing the measuring stick is expensive on purpose. An instrument that is cheap to change is an instrument nobody can trust.

---

## Objects

These are the only object kinds the system needs. Documents are how some of them are *shown*.

| Object | Meaning | Carrier |
|---|---|---|
| **Intention** | An outcome that should become true, plus non-goals | A short statement; later, a signed intent on a project |
| **Capability** | What **is** built | `openspec/specs/<capability>/spec.md` |
| **Change** | What **should** change | `openspec/changes/<id>/` with disposition in the file |
| **Work node** | A ready or blocked unit with one acceptance surface | A bead, or a checkbox that *is* a bead |
| **Agent** | Something that can accept a task packet and return a signed result | Human, model, group, or later a VM |
| **Evidence** | A check that would look different if the claim were false | A focused command, a journey, a contrast pair |
| **Learning** | A fact the next loop must not re-discover | `docs/LEARNINGS.md`, append-only |

### Capabilities vs changes

A `SHALL` found by search is not evidence the behavior exists. Delta files and living specs share a voice. Status and provenance must survive path-stripping.

- Living spec: this is true of the running system.
- Change: this will be true after fold, if activated.
- Parked change: not available work until its revive condition fires.
- Icebox (when needed): an idea with zero code, removed so it stops polluting the ready-set.

Skip a change entirely when the work *restores* intended behavior, or is a typo, a pin, a comment, or a test for something already specced.

### The brief

What a capable agent actually needs, and nothing else:

```markdown
# <id>: <one-line goal>

**Goal.** What is true after this that is not true now.

## Acceptance
- [ ] Outcomes, independently checkable. Not tasks.

## Contract
Real signatures, pasted from real docs or source.

## Inherited
Gotchas from LEARNINGS.md that touch this subsystem.

## Out of scope
The adjacent thing we are deliberately not doing, and where it lives.
```

Briefs die after the work lands. Durable residue is the code, the bead, the architecture amendment, the learning.

---

## Verbs

The morphisms. If a proposed process step is not one of these, it is probably a document.

| Verb | Meaning |
|---|---|
| `observe` | Read structure, specs, tests, people, prior evidence |
| `orient` | Classify load, blast, stage; pick rigor |
| `split` | Intention → a DAG of changes / work nodes |
| `assign` | Bind a node to an agent (human, model, or group) |
| `activate` | Human marks PENDING → ACTIVE. Agents do not self-activate architecture+ work |
| `act` | Mutate the world |
| `verify` | Focused, causal, discriminating |
| `fold` | Delta → living spec; amend architecture; do not delete the trail |
| `learn` | Surprise → LEARNINGS.md |
| `park` | Not available work until a revive condition |
| `group` | Open a topology of agents that still presents as one agent |

`fork` and `weave` and `pipeline` are not extra verbs. They are **topologies** of `group`.

---

## Splitting intention

One test, from Tatastu: *can you write a scenario that fails today and passes after?* If yes, it is a change. If no, it is a document, a spike, or a vibe-fix.

Rules:

1. A node has **one acceptance surface**.
2. Edges are **real dependencies** — B cannot start until A has committed a usable artifact with the evidence its contract requires. Readiness comes from artifacts. Ceremony records that fact.
3. The ready-set is nodes with all inbound edges satisfied. That is `bd ready`. Do not maintain a second graph in markdown.
4. Prefer modifying an existing capability over inventing a new one.
5. If you cannot name the capability, you are still in Orient.
6. Checkboxes are work **this node** owes. Handoffs, findings, and out-of-scope are bullets. A checkbox that can never close is a lie in the ready-set.

Governing prose (this file, a product note, a sequencing doc) may reason. It must **name landing change-ids**. It must not become a second requirements store.

---

## Agents

An agent is anything that implements the **agent surface**:

```
task packet in  →  signed result out
```

A human is an agent. A model in a harness is an agent. A group is an agent. Later, a Mjolnir VM running a specialist is an agent. The surface does not change. That is what makes the graph composable.

### Task packet

The packet is the only thing a foreign harness is given. Never a slash command.

| Field | Why |
|---|---|
| Goal | Commander’s intent for this node |
| Anchors | Symbol names and invariants. Not pasted file bodies. The worker re-anchors on live HEAD |
| Acceptance | The focused verify: command, journey, or contrast |
| Out of scope | Adjacent work and where it is tracked |
| Constraints | Permission class, paths, “do not deploy” |
| Load class | `structure-clear` / `intention-critical` / `ambiguous` |
| Rigor | vibe / brief / change / architecture / instrument |
| Identity of requester | Who asked, so the result can be addressed |

Plans record **where** and **what must remain true**. HEAD says what the file currently contains.

### Signed result

| Field | Why |
|---|---|
| Artifacts | Paths written |
| Evidence | The focused result, or why it could not run |
| Disposition | pass / task-red / baseline-red / infra-red / blocked / parked |
| Signer | The agent’s key (or, today, a stable id) |
| Members | If the signer is a group, who actually ran |
| Topology | If a group, which topology produced this |
| Commit | Persistence is not optional on edit, including red |

On disk, in this generation, “signed” may mean a result file with identity, members, topology, and a content hash. On Mjolnir, it means a real key on a real VM. The schema does not change when the cryptography becomes literal. Design the surface as if the key is already real.

### Assignment

Assignment is `shape × load class × permission`, not who is logged in.

| Shape | Who | Why |
|---|---|---|
| Mechanical edits, renames, lint | Cheap / fast model | Abundant, low blast |
| Multi-step implementation | Grok as default processing worker | Third-family lens, strong, abundant |
| Long-horizon or a second family | Codex | Independent orientation |
| Harness, slash, vision, tight back-and-forth | Native conductor | Foreign harnesses cannot run host commands |
| `ambiguous`, journey, money, deploy, instrument | Human | Activation and eyes |
| Complementary or contested work | Group | Topology, not a bigger prompt |

Same-family review of one’s own work cannot **promote**. Self-check is free and not load-bearing. Promotion needs a fresh reader, a live oracle, or a human.

Permission classes, from MetaDev, stay first-class:

- **read** — observe, draft, split
- **write** — act on an activated node
- **sensitive** — auth, schema, money, deploy; always a person

A plan is not permission. Default stop before code on architecture+ work. `--autonomous` (or the spoken equivalent) buys *unattended*, never *unsafe*. Human-verify boxes stay unchecked. True blockers halt the implicated branch, not the graph.

### Failure classes

Stolen from MetaDev, because they keep a 4–20 agent tree moving:

| Class | Meaning | Effect |
|---|---|---|
| `pass` | Focused verify is green | Complete the node. Do not rerun a green. |
| `task-red` | Causal evidence ties the failure to this node’s paths | Repair the smallest implicated branch |
| `baseline-red` | Failure unchanged from pre-state, or outside declared paths | Complete the node. Do not “fix” the baseline. |
| `infra-red` | Runner, tool, or environment failed | Retry infra once, then report. Do not blame the code. |
| `blocked` | Missing input, missing human, missing decision | Park the branch. Independent nodes keep moving. |

Commit-on-red is invariant. Unowned dirty files on a multi-agent tree get adopted by the next peer’s broad add. If a backend cannot commit, fix the executor or route elsewhere. Never write the exemption into a brief — it will be pasted onto a backend it was not meant for.

---

## Groups

A group is an agent whose interior is a **topology of other agents**.

That sentence is the whole point. Groups are not “run it twice.” They are how complementary work is composed, how contested work is compared, how a human and a model share a node, and how this system later governs fleets on Mjolnir without growing a new abstraction.

From the outside, a group has:

- an **identity** (a key it signs with)
- the **same surface** as any agent (task packet in, signed result out)
- a **membership** (humans, models, other groups)
- a **topology** (how members are wired)
- a **reduce** (how interior results become one signed result)

From the inside, members receive ordinary packets. They do not need to know they are inside a group, except when the topology gives them another member’s artifact as input.

Because a group *is* an agent, groups nest. A weave of two specialists can be one member of a review pair. A fork can sit inside a pipeline. Composability is not a feature we add later; it is the type of `group`.

### Topologies

These are the ones we know we need. More can be added without changing the surface. A topology is a wiring, not a ceremony.

#### Solo

One member. The degenerate group. Exists so “assign to Grok” and “assign to a group” are the same operation.

#### Weave

The default complementary group. Separately assigned pieces, different jobs, one outcome.

Example: one member extracts the living-spec delta, another writes the journey, a third implements. They do not duplicate. They produce parts that only make sense together. The reduce step weaves: the change is not foldable until delta, journey, and code all exist and cite each other.

Weave is how most real software is made. Fork is the exception.

#### Pipeline

Ordered specialists. Observe → design → implement → read. Each member’s signed result is the next member’s packet. Use when the output of A is the input of B and they cannot run in parallel.

A pipeline is not a sprint. It is three agents and two edges.

#### Fan-out / reduce

Independent nodes in parallel, then a reduce. Use when pieces do not share a write-set. The reduce is a fold, a summary, or a compatibility matrix — not a rewrite of everyone’s work.

Harness adapters are a fan-out: one member per harness, reduce into “the skill loads here, with these gaps.”

#### Fork

Same acceptance, two (or more) implementations, pick by discriminating evidence.

Open a fork only when at least two of these hold:

- blast is schema, auth, money, or protocol
- load class is `intention-critical` or `ambiguous`
- two plausible designs survive Orient
- the cost of being wrong exceeds the cost of two short acts

Both sides share the **same acceptance**. They do not share an implementation. The loser is parked with a revive condition, not deleted. That is variety without a fake backlog.

“Two plans is one; one plan is none” is a Marine proverb, not a standing order. Most nodes are Solo or Weave.

#### Review pair

Builder + independent reader. The reader does not edit. Promotion requires the reader’s signed pass, or a documented dissent the human accepts.

For instrument-grade work the reader asks *how would I fake this?* and whether the evidence would look the same if the claim were false.

#### Human gate

Agent drafts; human activates or rejects. This *is* Tatastu’s PENDING → ACTIVE BUILD. The human is a member, not an external exception. The group cannot sign a write result until the human member has signed activation.

#### Conductor / workers

One conductor holds permission, stage transitions, and the write door. Workers receive inlined packets, edit scoped paths, commit-on-red, return. The conductor never broad-adds. This is MetaDev’s execution tree, named as a topology so it can nest.

#### Quorum

N members, K signatures required. Use for contested promotions, releases, or anything whose failure is political as well as technical. Do not use for typo-fixes.

### What a group is not

- Not a standup.
- Not a bigger prompt with “consider multiple perspectives.”
- Not a duplicate path unless the topology is Fork.
- Not a way to dodge a human on sensitive work — the human is a member.
- Not a new object type. If it cannot accept a packet and sign a result, it is not a group.

### Identity, now and later

Today, in a repo:

```
groups/<id>/
  surface.md      # id, members, topology, key or stand-in
  packet.md       # what was asked
  results/        # per-member signed results
  reduced.md      # the group’s signed result
```

Later, on Mjolnir:

- each agent (model, human session, or group) runs in or is addressed as a VM
- the key is a real key
- the packet and result are messages
- attestation is the same schema with cryptography filled in

`intentional.agency` and `taskmaster.dev` are the same graph with a public address. A project is an intention plus a ready-set plus the agents (including groups) bound to its nodes. Governing agents is not a different product. It is this surface hosted.

Until those exist, the skills write the files. The files keep the shape honest.

---

## Skills

The portable unit is an [Agent Skill](https://agentskills.io/specification): a directory with `SKILL.md` (name + description in frontmatter, body short) and optional `references/` and `scripts/`.

Five skills. Thin dispatchers. Progressive disclosure. No phase-0 through phase-5.

| Skill | Job |
|---|---|
| `intend` | Capture intention; observe; orient; split the DAG; decide rigor; open groups |
| `change` | OpenSpec-lite: proposal, deltas, disposition, journey. Skip for restore-only |
| `act` | Ready-set execution; assign; focused verify; commit-on-red |
| `fold` | Archive deltas into living specs; amend architecture; append learnings |
| `brief` | Already exists. The unit-of-work payload |

`intend` is the conductor of the loop. The others are verbs it can invoke, and that a human can invoke alone.

Scripts are host-neutral (shell / Python). Foreign workers get a packet. They are never told to “run `/sprint-plan`.”

### Harness touch-ins

Canonical skills live where every harness can see them: `.agents/skills/` (and the same tree published from this marketplace).

| Harness | Touch-in |
|---|---|
| **Grok** | Loads `.agents/skills/`, `.grok/skills/`, `.claude/skills/`; Claude-compatible marketplaces |
| **Claude** | Marketplace wrapper and/or project skills. Optional `plugin.json` *points at* the same tree |
| **Codex** | Native `$name:skill` / `@name:skill`. A small route map. No `/slash` as the API |
| **Hermes** | Agent Skills native. Extra `hermes:` fields are ignored elsewhere |
| **Prime Agent** | Agent Skills native. Python-backed skills are a Prime superset — do not require them |

A Claude-only plugin is not the source of truth. Morphist-tools is that today; it will not travel. MetaDev pays a tax maintaining dual manifests and still cannot give Grok slash commands.

Optional wrappers:

- Claude / Grok marketplace `plugin.json` pointing at the skill tree
- Codex routes for `intend` / `change` / `act` / `fold` / `brief`
- `AGENTS.md` as a one-page orientation pointer, not the system

MCP is optional Observe, not required. MetaCoding’s graph tools plug in when present. Grep + tests are the fallback.

Hooks stay host-specific and non-load-bearing. If the hook is down, the loop still runs.

### What we are not building in the first fold

- A 40-command control plane
- Dual Claude/Codex packaging as the core
- Mandatory SCIP / ladybug / operad mining
- Sprint numbers, epic novels, readiness-report theater
- `taskmaster.dev`, `intentional.agency`, or Mjolnir hosting — named so the surface stays compatible; not in the first ready-set

Forking MetaDev is an open Fork (see the build graph). Phong would likely take merge requests. We do not decide that by vibe after writing skills that assume one answer.

---

## Using the loop

A walk-through, so the verbs have weight.

**Intention:** users can leave with their keys and their data, and stop paying, without permission.

1. **Observe** — existing export paths, auth store, living specs, LEARNINGS.
2. **Orient** — `intention-critical` (policy lives in tests, errors, constants); blast = data/auth; existing product → rigor **architecture + change**, not vibe.
3. **Decide** — split: (a) inventory what is captive, (b) export format, (c) key-handoff journey, (d) delete-on-exit. Open a **Fork** on (b) if two formats survive Orient, same acceptance: a departed user restores elsewhere with no permission. Open a **Weave** on (c)+(d) with a human member for the journey.
4. **Assign** — (a) Grok solo; (b) fork Grok + Codex; (c)+(d) weave, human-gated.
5. **Act** — ready-set; focused verifies; commit-on-red.
6. **Fold** — capability `exit-and-export` updated; ADR amended, not deleted; surprises into LEARNINGS.

No sprint number. Two implementations only where being wrong is expensive. Complementary work is woven, not duplicated.

---

## Building the methodology with the methodology

This section is the first Act. The rest of the file was Observe, Orient, and Decide.

### Observe (what we have)

- This marketplace, morphist-tools, `/brief`, `/spike`, `/vision`, `/sprint-plan` and its ceremony overlay, `CONVENTIONS.md`
- Tatastu’s OpenSpec tree, dispositions, journey gate, `check:docs`
- MetaDev’s plan IR, `planctl`, work ladder, execute charter, Grok/Codex headless runners
- MetaCoding’s graph, intention harvest, load classes, port briefs
- Harness skill loading: Grok, Claude, Codex, Hermes, Prime
- Delivery surfaces not yet in this ready-set: Tatastu app, `taskmaster.dev`, `intentional.agency`, Mjolnir VMs

### Orient

- Load class for *this* work: `intention-critical`. The verbs and the group surface *are* the product. Structure (a skill folder) is easy; the meaning of a group is not.
- Blast: process kernel. If we get the agent surface wrong, every later host encodes the mistake.
- Lifecycle: greenfield kernel, brownfield around morphist. We are not deleting `/sprint-plan` in the first fold; we park it with a revive condition.
- Rigor: **architecture** for the surface and the topologies; **change** for each skill; **brief** for harness touch-ins; **instrument** only for the hygiene script that decides what “folded” means.
- Group? Yes. Complementary pieces, not a fork of the whole system. One Fork only: *new skill tree vs extend MetaDev*.

### Decide

We write this file (done). We treat it as commander’s intent. We split the DAG below. We activate nodes in chat or by adding them to the build — agents draft, they do not self-activate architecture nodes.

Landing zone for requirements that grow out of this file: named change-ids, not more SHALL in this prose.

### The DAG

Dependencies flow down. Ready-set = nodes with all inbound done.

```
I0  this document (commander’s intent)
 │
 ├── C1  agent surface + group contract          [architecture · folded 2026-08-14]
 │     weave: schema · topologies · identity
 │     landed: ARCHITECTURE.md ADR-001 · docs/contracts/
 │
 ├── C2  living-spec layout (OpenSpec-lite)      [change · folded 2026-08-14]
 │     depends on C1 (packets cite capabilities)
 │     landed: openspec/specs/living-specs · ADR-002 · archive/2026-08-14-add-living-spec-layout
 │
 ├── F1  packaging Fork                          [architecture · folded 2026-08-14]
 │     winner: Path A (plugins/intention + .agents/skills)
 │     Path B (MetaDev fork) PARKED — revive in ADR-003
 │     landed: ADR-003 · openspec/specs/packaging
 │
 ├── S1  intend                                  [change · folded 2026-08-15]
 ├── S2  change                                  [change · folded 2026-08-15]
 ├── S3  act                                     [change · folded 2026-08-15]
 ├── S4  fold                                    [change · folded 2026-08-15]
 │     weave: shared references + four dispatchers
 │     landed: openspec/specs/verbs · plugins/intention/references/
 │
 ├── H1  harness touch-ins                       [brief]
 │     fan-out: Grok · Claude · Codex · Hermes · Prime
 │     reduce: compatibility matrix
 │     depends on S1–S4
 │
 ├── G1  hygiene script                          [instrument]
 │     banners, fold-debt, journey present, checkboxes honest
 │     review pair: builder + independent reader
 │     depends on C2
 │
 ├── D1  dogfood                                 [change]
 │     run intend on a real unit in this repo (park or shrink sprint-plan)
 │     depends on S1–S4, G1
 │
 └── P1  park, do not build                      [parked]
       Tatastu shipping, taskmaster.dev,
       intentional.agency, Mjolnir VM hosting
       revive: D1 has folded once on a real change
```

### Groups for this build

| Group | Topology | Members (roles, not people) | Reduce |
|---|---|---|---|
| **C1 weave** | Weave | (1) packet + result schema, (2) topology catalog, (3) identity/key stand-in | One contract: a group is an agent |
| **F1 fork** | Fork | Path A: skills-first tree. Path B: MetaDev extension | Same acceptance; loser parked |
| **Skills weave** | Weave | Four authors (or one author, four packets) for `intend` / `change` / `act` / `fold` | Skills share vocabulary; none redefines the surface |
| **H1 fan-out** | Fan-out / reduce | One adapter per harness | Matrix: loads? packet-only? gaps? |
| **G1 review pair** | Review pair | Builder of the hygiene script + independent reader | Reader asks how to fake “folded” |
| **Human gate** | Human gate | Drafting agent + Duke | Architecture nodes (C1, F1) do not write until activated |

Complementary, not duplicate: C1’s three members write different faces of one surface. H1’s members write different hosts. S1–S4 write different verbs. The only duplicate path is F1, and it is expensive on purpose.

### Acceptance for the first fold

The methodology has begun to exist when all of these are true:

- [x] A stranger can read this file and assign a node without a call — founding doc + intend-dag, 2026-08-15
- [x] `intend` produces a DAG of named change-ids, not a sprint folder — dispatcher landed F1; S1 deepens
- [x] `change` writes a PENDING delta with a journey or an explicit “no new UI because…” — dispatcher landed F1; S2 deepens
- [x] `act` gives a foreign harness a packet, never a slash command — dispatcher landed F1; S3 deepens
- [x] A group can be Solo, Weave, or Fork, and signs one result — C1 examples + schema, 2026-08-14
- [x] `fold` moves truth into living specs and leaves an amendment trail — C2, 2026-08-14
- [x] Restore-only work still skips the ritual — specced in living-specs; G1 will enforce
- [ ] `/sprint-plan` is parked or demoted, with a revive condition
- [ ] G1 would fail if a change claimed done without fold or with eternal checkboxes
- [ ] D1 has used the loop on a real change in this repo

Out of scope for the first fold (tracked as P1): hosting, billing, VM attestation, public agency directory, Tatastu product-run integration beyond “this markdown can be a brief that materializes a change.”

### Inherited

- Briefs are disposable; architecture is amended, not deleted. (`CONVENTIONS.md`)
- Status in the file, not the path. (Tatastu `check:docs`)
- Foreign harnesses get tasks, never commands. (MetaDev work ladder)
- Self-verify is not load-bearing. (MetaCoding iteration methodology)
- Process docs at 1.7× production code is how we know the factory failed. (`identikey-core`, 2026-07)

---

## What this replaces, when it has folded

| Today | After D1 |
|---|---|
| `/sprint-plan` 10-phase factory | `intend` → DAG of `change`s |
| `docs/sprints/{NNN}/` novels | living `specs/` + `changes/` |
| Story templates | `brief` or a change’s `tasks.md` |
| `phase-state.json` as process truth | beads as work truth; specs as behavior truth |
| `/sprint-exec` as OMC-only dispatch | `act` with a work ladder and groups |
| `/prd` + `/vision` as required prequel | optional Observe sources, not a gate |
| Readiness-report theater | fold + journey + discriminating evidence |

Keep `/spike` (empirical Orient), `/vision` (when the product *is* the question), and beads. Keep `/brief`. Demote `/sprint-plan` to “I explicitly want a multi-week batch plan,” or park it.

---

## For later hosts

Named so the surface stays stable. Not a promise to build them in this repo.

| Host | What it is, in this vocabulary |
|---|---|
| **Tatastu** | A place to run the loop with humans in the room. This file can seed a Product Run brief that materializes a `change`. |
| **taskmaster.dev** | The ready-set as a product. Nodes, assignments, evidence. |
| **intentional.agency** | Intentions with public address. Projects as signed intent + bound agents. |
| **Mjolnir VMs** | Agents (and groups) with real keys, real isolation, signed packets. The same surface. |

If those products need a different object model, this file was wrong. Change this file. Do not invent a parallel kernel.

---

## How to read this later, when it has been split

This document will be cut into explainers, skill references, and interactive pieces. The cuts are already visible:

1. The claim and the loop
2. Lineage (why these four systems)
3. Objects and verbs
4. Rigor and load class
5. Splitting and the work graph
6. The agent surface
7. Groups and topologies
8. Skills and harness touch-ins
9. The first DAG (this will move into a `change` and then into history)

Until those cuts exist, this is the source. Amend it when reality diverges. Do not delete the trail.
