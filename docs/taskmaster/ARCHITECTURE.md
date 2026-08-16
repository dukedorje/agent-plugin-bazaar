# Taskmaster — architecture sketch

Not an accepted ADR. Activate `add-taskmaster-host` before any of this
becomes kernel truth. Amend in place when a decision flips.

## Decided now (2026-08-16)

| Decision | Why |
|---|---|
| Sibling app, not this marketplace | Kernel stays packets + skills; the SaaS is a host |
| **One VM, one process, one SQLite file** | First site. Backup / sync / multi-instance are later |
| **SvelteKit + adapter-node, dev mode** | Logged-in SaaS needs a server. SSG is off the table for v0. Dev server is an explicit exception to Mjolnir’s “deploy is a snapshot” discipline |
| **Daemon on a guest port → taskmaster.dev** | Hand-route the playground box (same honesty as Zine today). Snapshot cutover when we have a build |
| SQLite through **libsql**, local file | No write pool yet. One writer is the process |
| Login via **IdentiKey** | Same identity fabric. Do not invent a second IdP |
| Objects = node, assignment, evidence | Founding host table. Groups assign and split |
| **Actions run on the Mjolnir guest** | An agent of a given type can do whatever that guest can do |
| **See the UI from inside the guest** | Playwright / Chromium on the same VM. Storybook is not the action surface |
| **Related intentions are a weave** | MetaCoding + Fong Meta Env + this kernel are peers. [RELATED.md](RELATED.md) |

## Later (not this landing)

- libsql adapter onto Mjolnir storage / LUKS volumes
- Serialized write pool and cross-instance SQLite
- Immutable release snapshots (`Deploy.Runtime` / `mj deploy`)
- Storybook
- More than 512 MiB / a browser snapshot (needed before Chromium)

## Open

1. **Guest port** — Mjolnir’s SvelteKit plan defaults to `3000`. Confirm when the daemon starts.
2. **DNS / gateway** — who cuts `taskmaster.dev` (or a subdomain) to this VM’s route. Host-side; not a guest edit.
3. **Fong Meta Env path** — our copy is not on disk under a name I could find. Bead `bazaar-zmq`. Put the path in RELATED.md when you remember it.
4. **IdentiKey login** — hop when auth blocks.

## Shape we are not deciding here

Packet schema, topologies, fold rules — already ADR-001 / living specs.
Taskmaster **consumes** those. If the SaaS needs a different object
model, change the founding doc, do not grow a parallel kernel.
