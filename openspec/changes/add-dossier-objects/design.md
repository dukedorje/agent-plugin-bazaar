# add-dossier-objects — settlements

Architecture write. These answers are the change. Act copies them into
ADR-007; it does not reopen them.

Amended after advise send-back (2026-08-17) and Duke: intentions
come out of a dossier; several may emerge over time; keep provenance.

## Why a capability

`working-method` is the algebra: loop, kinds, split. Gather, cite, and
emerge would turn that spec into a novel again. `dossier` is that
cluster. The kinds list on `working-method` still has to be honest, so
this change MODIFIES it and ADDs the capability.

Packet / result stay `agent-surface`. Dossier is a work object, not an
actor: it does not accept a packet or sign a result.

## Settled

1. **New work object, plus a `dossier` capability.** Not host-only.
   Taskmaster may project it later; it must not be the first place the
   word exists.

2. **Project is the named graph Taskmaster already describes** — an
   intention and its work nodes with a public address. Not a ninth
   kind. A dossier is not a project. Each emerged intention may later
   have such an address; they need not share one.

3. **Values are named preferences** a project carries. A project
   breaks down into intentions *and* those values. Values are not
   work nodes and do not enter the ready-set. “Value Function” as
   speech is a synonym for a named preference. A score engine or
   function runtime is not this change and is not a work-object kind.

4. **Intentions emerge from a dossier; the gathering stays.** Mint or
   select an intention from the dossier. The dossier is not that
   intention and is not consumed. The epic word “promote”
   (`add-dossier-promote`) means this emerge, not “the dossier
   becomes the project.”

5. **Many intentions, over time.** One dossier may give rise to
   several intentions as assets compile. The first emerge does not
   close the well.

6. **Provenance is a citation trail.** Each emerged intention cites
   the dossier. It may cite specific assets already cited on the
   dossier. That is the provenance. Not a copy of bytes, not a fourth
   store, not a second packet shape. Bytes still wait on `bazaar-ja7`.

7. **Self-description is not identity.** It may seed a project’s
   public lede. Each project’s identity is its own public address.
   The host (Taskmaster) shows that address; this marketplace does
   not mint URLs. This is not IdentiKey.

## Why not the other forks

- Host-only Dossier: the host already must not invent an object model
  (ADR-006). Naming it only in SvelteKit would be that invention.
- Project as a new kind: INTENT and ADR-006 already have the graph.
- Values as scores or as work nodes: invents a runtime, or lies about
  READY.
- One-shot consume: “dossier becomes a Project” destroys the well
  later intentions need and drops provenance.
- Provenance log / blob store: store number four. Cite.

## Paste

`add-paste-objects` is the parse face of these objects, not a second
ADR about kinds. It depends on this change.
