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

**Not decided here.** Packaging (new skill tree vs MetaDev fork) is F1.
Living-spec directory layout is C2. Both cite this surface; neither may
redefine it.

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

**Not decided here.** Hygiene automation is G1. Skill verbs are S1–S4.
