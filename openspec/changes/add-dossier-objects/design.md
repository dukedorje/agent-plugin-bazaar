# add-dossier-objects — settlements

Architecture write. These answers are the change. Act copies them into
ADR-007; it does not reopen them.

## Why a capability

`working-method` is the algebra: loop, kinds, split. Gather, cite, and
promote would turn that spec into a novel again. `dossier` is that
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
   kind. Promotion addresses that graph and cites the dossier.

3. **Values are named preferences** a project carries. A project
   breaks down into intentions *and* those values. “Value Function”
   as speech is allowed as a synonym for a named preference. A score
   engine or function runtime is not this change and is not a
   work-object kind.

4. **Promote by citing, not mutating.** Address (or mint the address
   of) the Project and record the dossier as a citation. The gathering
   stays citable. Mutating the dossier into a Project would destroy
   the thing later nodes need to point at.

5. **Self-description is not identity.** It may seed the project’s
   public lede. The project’s identity is its public address. This is
   not IdentiKey.

## Why not the other forks

- Host-only Dossier: the host already must not invent an object model
  (ADR-006). Naming it only in SvelteKit would be that invention.
- Project as a new kind: INTENT and ADR-006 already have the graph.
  An eighth-plus-ninth kind is a parallel kernel.
- Values as scores: invents a runtime the gather path does not need.
- Mutate-on-promote: `add-dossier-promote` acceptance is “the dossier
  is still citeable.”

## Paste

`add-paste-objects` is the parse face of these objects, not a second
ADR about kinds. It depends on this change.
