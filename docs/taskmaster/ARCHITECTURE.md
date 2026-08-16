# Taskmaster — architecture sketch

Not an accepted ADR. Activate `add-taskmaster-host` before any of this
becomes kernel truth. Amend in place when a decision flips.

## Decided (Orient survived)

| Decision | Why |
|---|---|
| Sibling app, not this marketplace | Kernel stays packets + skills; the SaaS is a host |
| SvelteKit web UI | Named stack for the first site |
| SQLite through **libsql** | Embedded, then adapted onto Mjolnir storage |
| Many connections, **serialized writes** | SQLite is single-writer. Hand out connections from a pool; linearize writes in arrival order. Readers may share. |
| Scale-out via **Mjolnir instances** | Traffic → more boxes. SQLite sync is a storage-layer problem, not “bigger VM” |
| Login via **IdentiKey** | Same identity fabric as Mjolnir. Do not invent a second IdP |
| Objects = node, assignment, evidence | Founding host table. Groups assign and split. Resources attach to nodes |

## Open (need a spike or a human)

1. **libsql on Mjolnir** — what the adapter actually talks to (file on guest disk vs a storage volume the host owns).
2. **Cross-instance SQLite** — how serialized writes stay serial when two boxes take traffic. Candidate: Mjolnir storage layers already used for LUKS volumes.
3. **IdentiKey login** — UI is not complete. First auth-blocked story is a hop to that team, not a local fake forever.
4. **SSG vs SSR** — earlier steer was SvelteKit SSG. A logged-in SaaS usually needs a server. Reconcile before `nod-repo` scaffolds: static shell + authenticated API, or adapter-node on the box.

## Shape we are not deciding here

Packet schema, topologies, fold rules — already ADR-001 / living specs.
Taskmaster **consumes** those. If the SaaS needs a different object
model, change the founding doc, do not grow a parallel kernel.
