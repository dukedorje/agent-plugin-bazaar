# Architecture

Living. ADRs inline. Amend rather than delete when reality diverges.

This file answers *why it is shaped this way*. Behavior that is true of the
running system belongs in living specs (C2). Work state belongs in the graph.

---

### ADR-001: Agent surface — a group is an agent ✅

**Status:** Accepted 2026-08-14 (C1 activated).
**Blast:** process kernel. Every later host (skills, Tatastu, taskmaster,
intentional.agency, Mjolnir) encodes this or forks it.

**Decision.** Every actor — human, model, group, later a VM — implements one
surface: **task packet in → signed result out**. A group is not a new object
type. It is an agent whose interior is a topology of other agents. Groups nest
because the type allows it.

**Why.** Composability dies the moment “the team” is a different thing from
“the worker.” Duplicate-path A/B is one topology among several; the default
complementary form is a weave. Identity is a key (stand-in today, real later)
so a result can be addressed and attested without changing schema.

**Consequences.**

- Skills (`intend`, `change`, `act`, `fold`) dispatch packets. They never
  invent a second RPC. Foreign harnesses receive a packet, never a slash command.
- On-disk layout and JSON schemas live under `docs/contracts/`. The normative
  prose is `docs/contracts/agent-surface.md`.
- Cryptography may fill in `signature.bytes` later. `content_hash` is required
  now. The field set does not grow a parallel “unsigned result.”
- `/sprint-plan` is not the agent surface. It is parked relative to this ADR
  until D1 says otherwise.

**Not decided here (superseded).** Packaging was F1 — see ADR-003.

**Normative contract:** [`docs/contracts/agent-surface.md`](docs/contracts/agent-surface.md)

---

### ADR-002: Living specs live under `openspec/` ✅

**Status:** Accepted 2026-08-14 (C2 activated).
**Blast:** process memory. Skills and later Tatastu shipping read this tree.

**Decision.** Two-layer truth uses the OpenSpec directory names, under
`openspec/`:

- `openspec/specs/<capability>/spec.md` — what **is** built
- `openspec/changes/<id>/` — what **should** change (deltas + disposition)
- `openspec/changes/archive/YYYY-MM-DD-<id>/` — folded deltas, frozen
- `openspec/project.md` — project conventions, not requirements
- `docs/` and this file — reasoning and ADRs. They name change-ids. They
  never carry a `SHALL`.

**Why.** Tatastu already speaks this layout; the founding doc stole the
two-layer model from OpenSpec. Using the same names means a Tatastu Product
Run can materialize a change here without a translator. We do **not** require
the `openspec` CLI. We do **not** copy Tatastu’s disposition encyclopedia,
icebox taxonomy, or `check:docs` allowlists. Those wait for the failure modes
that produced them. G1 will enforce the few rules this spec names.

**Consequences.**

- Capability ids are directory names. Packets at `change` rigor and above
  MUST set `capability` to one of those ids (or to an id a change is ADDing).
- C1’s normative schema stays in `docs/contracts/`. The living spec
  `agent-surface` points at it. Do not fork the schema into markdown SHALLs.
- Done is fold + archive in the same breath as “the work shipped.” A fully
  checked change still sitting in `changes/` is a lie.

**Not decided here.** Hygiene automation is G1. Skill *depth* is S1–S4;
hosting is ADR-003.

---

### ADR-003: Skills-first packaging; MetaDev fork parked ✅

**Status:** Accepted 2026-08-14 (F1 activated). Path A won. Path B parked.
**Blast:** how verbs reach Grok, Claude, Codex, Hermes, Prime.

**Decision.** Canonical verbs are Agent Skills. Files live in
`plugins/intention/skills/<verb>/SKILL.md`. `.agents/skills/<verb>` is a
symlink to the same directory so Grok / Hermes / Prime load them in-repo
with no install. Claude and Grok marketplaces list plugin `intention`.
Codex invokes by skill name, never as a Claude slash command.

**Path B (fork/extend MetaDev) is parked.** Revive when we need MetaDev’s
planctl / headless runners *and* Phong wants an overlay. The overlay MUST
consume these skills’ packets. It MUST NOT become a second skill tree.

**Why (discriminating).** Shared acceptance was: five verbs runnable on
Grok and Claude.

- Path A: Grok scans `.agents/skills/` natively. This session loaded
  `intend`, `change`, `act`, `fold`, `brief` from those paths. Claude
  installs `intention` from the marketplace / `--plugin-dir`.
- Path B: MetaDev’s Grok surface is `grok-headless-exec` — a *worker*,
  not a skill host. Its user-invocable verbs are Claude slash commands
  and Codex `$meta-dev:*`. Making `/intend` native on Grok under Path B
  requires adding an Agent Skills tree — which is Path A inside MetaDev.

The two observations cannot be the same. Path B fails the Grok half of
the acceptance without becoming Path A.

**Consequences.**

- Do not add Claude-only commands as the source of truth.
- Do not vendor MetaDev’s dashboard / inbox / 40-command surface.
- S1–S4 deepen these five dispatchers. They do not move the files.
- H1 adds harness notes; it does not fork the tree.

---

### ADR-004: Dispatch density, distilled face, persist-at-boundary ✅

**Status:** Accepted 2026-08-15 (`add-dispatch-density` activated).
**Blast:** instrument. Changes what a packet says and what a conductor
is allowed to look at.

**Decision.** Packets carry optional `density` (`lean` · `standard` ·
`explicit`), `surface` (`skill-host` · `packet-only`), and `consult`.
Results may carry a `distilled` face and `raw_ref`. Identity may carry
`interface` for hosts not in the closed `harness` enum (`harness: other`).

Capability order is the **inverse** of density: strongest workers get
the leanest packets. A weaker assignee may consult a stronger model for
`explain` / `replan`; that is not a write handoff.

Edits persist at the **isolation boundary**. Worktrees are allowed.
Inside one, the conductor commits; workers edit and stop. A cloud/VM
agent that is the top of its tree persists itself. Never put “do not
commit” in a packet.

The conductor reads distilled, not the transcript. Vocabulary:
[`docs/contracts/dispatch.md`](docs/contracts/dispatch.md).

**Why.** Fan-out dies when the main thread absorbs six novels, when a
Flash worker is given a lean packet with no warning, or when a
git-exemption in prose is pasted onto the wrong backend.

**Not decided here.** Ready-set scheduling, worktree creation, spawn
runners (`add-act-conductor`, `add-act-runners`).

---

### ADR-005: Claude Code coding pool; Grok architecture reader ✅

**Status:** Accepted 2026-08-16 (`update-act-ladder` activated).
**Blast:** assignment. Who gets the packet.

**Decision.** Default coding agents are Claude Code, which holds the
high usage limits:

| Shape | Assignee |
|---|---|
| Known / mechanical | Sonnet 5 · `explicit` |
| Implementation that needs thought | Opus 5 · `standard` · effort medium |
| Design | Opus 5 · effort low/medium · CC designer skills |
| Planning helper / replan consult | Fable 5 · `lean` · no write |
| Real architecture review | **Grok** reader (required). GPT-5.6 Sol if `available` |

Same-family review still cannot promote. Grok reading an Opus design
is the cross-family gate. Sol stays in the file with `available:
false` until there is a Codex subscription. Human pick always wins.

Source of truth: `plugins/intention/references/ladder.json`.
Resolve: `plugins/intention/scripts/ladder.py assign --shape …`.

**Why.** The previous ladder assumed Grok was the default coder and
Codex was in the pool. That is not the subscription set.

---

### ADR-006: Taskmaster host — a sibling, not a fork ✅

**Status:** Accepted 2026-08-16 (`add-taskmaster-host` activated).
**Blast:** product boundary. Where a running SaaS is allowed to sit
relative to this kernel, and what it is allowed to redefine.

**Decision.** `taskmaster.dev` is a **sibling host**. This repo stays
packets, skills, and specs; Taskmaster is an application that *hosts*
that surface, the way Claude, Grok, and Codex host the verbs.

- It **consumes ADR-001**. Node, assignment, and evidence are a
  projection of task-packet-in / signed-result-out — not a second
  object model. If the SaaS needs a different object model, amend
  [`docs/contracts/agent-surface.md`](docs/contracts/agent-surface.md);
  do not grow a parallel kernel next to it.
- **Ready is derived, never stored.** The ready set is `open ∧ all deps
  landed`, computed from edges. That invariant travels with the surface
  into any host, so a `ready` column is a defect wherever it appears.
- **Stack is not kernel truth.** Framework, adapter, database driver,
  look tokens, one-VM/one-process/one-SQLite-file, Mjolnir managed
  secrets — all recorded in the sibling app
  (`~/work/Taskmaster/taskmaster-web/docs/ARCHITECTURE.md`; hop:
  [`docs/taskmaster/ARCHITECTURE.md`](docs/taskmaster/ARCHITECTURE.md))
  and amended there. They may flip without touching this file.
- **The living capability `taskmaster` is created by fold, not by this
  ADR.** Until `add-taskmaster-host` folds, `openspec/specs/` gains no
  Taskmaster requirement. No framework choice of a site that is not
  running ever becomes a `SHALL` in this repo's living specs.

**Why.** Two failures were live at once. First, the recurring question
of whether the SaaS belongs inside the marketplace: naming it a sibling
host in an accepted ADR closes it, and keeps the kernel from acquiring
a web tier it would then have to carry. Second, the sketch in
`docs/taskmaster/` reads like decided architecture but had no accepted
status — so either it stays advisory forever, or its volatile parts
leak into living specs. Those parts are the *most* volatile things we
own: the dev-server exception to Mjolnir's snapshot discipline exists
precisely because that pipeline has never completed an end-to-end run.
A living spec that names it would lie the week it changes. Hosting is a
kernel decision; the stack under the host is not.

**Consequences.**

- The sketch of record is `~/work/Taskmaster/taskmaster-web/docs/`.
  Amend in place; it is reasoning, so it never carries a `SHALL`
  (ADR-002). This repo keeps a hop at `docs/taskmaster/`.
- The `taskmaster` living spec is stack-neutral. A reader looking for
  SvelteKit in `openspec/` should find nothing, now or after fold.
- Taskmaster does not absorb MetaDev or MetaCoding. They are peers in
  the same weave (`~/work/Taskmaster/taskmaster-web/docs/RELATED.md`);
  the MetaDev overlay stays parked under ADR-003.

**Not decided here.** IdentiKey login, snapshot deploy, guest port and
DNS (`bazaar-lgr.1` / `bazaar-lgr.2`), the MetaDev copy (`bazaar-zmq`),
and the node/edge table itself.
