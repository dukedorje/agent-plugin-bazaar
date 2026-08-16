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
| **Secrets: Mjolnir `secrets_mode: :managed`** (2026-08-16) | The guest holds no plaintext secret at rest. LUKS `secrets.luks` on the rootfs (ciphertext), rendered to `/run/mjolnir/secrets.env` on tmpfs at boot, auto-sourced into every `exec`. Passphrase is host-escrowed by vm_id. **Fixed at spawn — there is no in-place conversion**, so changing it means respawning |
| **Deploy key lives only in RAM** | The Forgejo key is a base64 secret; a `.path`-triggered unit pipes it into `ssh-agent` at boot. It never becomes a file on any filesystem. `git` reaches it via `core.sshCommand=/usr/local/bin/tm-git-ssh` |
| **Design system: "Terminal Graphite"** (2026-08-16) | One ground `#0c0c0d`, one paper `#f4f1ea`, one signal `#c8ff2f`. The signal means READY and nothing else — lime on anything not startable is a bug. Space Grotesk + JetBrains Mono, self-hosted variable (no CDN, no CLS). Tokens live in `src/routes/layout.css` |
| **The ready set is the page** | `/` is the ready set, not a marketing hero. Load choreography *is* the computation: all nodes arrive lit, then blocked/landed recede and only what is startable keeps the signal |
| **Ready is derived, never stored** | `src/lib/graph.ts` computes ready from edges (`open ∧ all deps landed`). That invariant is the seam the node/edge schema inherits — do not add a `ready` column |
| **Related intentions are a weave** | MetaCoding + Phong’s MetaDev + this kernel are peers. [RELATED.md](RELATED.md) |

## Later (not this landing)

- libsql adapter onto Mjolnir storage / LUKS volumes
- Serialized write pool and cross-instance SQLite
- Immutable release snapshots (`Deploy.Runtime` / `mj deploy`)
- Storybook
- More than 512 MiB / a browser snapshot (needed before Chromium)

## Open

1. **Phong’s MetaDev** — checkout is `~/work/Projects/AI/meta-dev`. Bead `bazaar-zmq`. Overlay still parked.
2. **IdentiKey login** — hop when auth blocks.
3. **Live graph** — `graph.ts` is seeded. Promote to a bead when the node/edge table lands.
4. **Guest port / DNS** — settled 2026-08-16: `:5173`, `taskmaster.dev` routed + LE cert. `bazaar-lgr.2` note is stale.

## Shape we are not deciding here

Packet schema, topologies, fold rules — already ADR-001 / living specs.
Taskmaster **consumes** those. If the SaaS needs a different object
model, change the founding doc, do not grow a parallel kernel.
