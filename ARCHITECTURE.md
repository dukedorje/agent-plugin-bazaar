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
