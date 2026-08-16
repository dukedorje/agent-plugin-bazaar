# Taskmaster — commander’s intent

Amended 2026-08-16. Duke, on the Mjolnir playground box.

## Outcome

A polished classic SaaS that helps you **master your tasks**.

The product *is* the work graph we already run in this directory: an
intention, a DAG of nodes, a ready-set, groups that assign and split,
resources bound to nodes, evidence that a node landed. A project is
that graph with a public address. Governing agents is not a different
product.

The same dynamics apply to how we build Taskmaster itself: name the
problem, split it, assign it, use MetaCoding when the structure is
already in the code.

**MetaCoding** here means the local-first code graph *and* the
categorical overlay: category theory applied to abstract syntax trees
(`ctkr` in `~/work/WorldTree/MetaCoding`). Taskmaster’s tasks are about
that work, not a generic ticket tracker.

**Phong’s MetaDev (our copy)** is a related intention we still owe:
finish the work in `~/work/Projects/AI/meta-dev`. It is not a
Taskmaster feature. It is a peer landing in the same weave — see
[RELATED.md](RELATED.md). Path B (fork/overlay) stays parked until
Phong wants an overlay that consumes our packets (ADR-003). Do not
drop it because the SaaS is louder.

## Non-goals (now)

- Forking the agent surface (packet in, signed result out)
- SHALLs in this marketplace’s living specs for a site that is not folded
- Building Tatastu, `intentional.agency`, or Mjolnir-the-product in this pass
- Pretending IdentiKey login is finished
- Multi-instance SQLite, write pools, virtiofs bets, Storybook
- Immutable Mjolnir release snapshots for the first site (that pipeline
  has never completed an end-to-end run; we are allowed a dev server)

## Constraints

- One Mjolnir VM, one process, one SQLite file
- SvelteKit with **adapter-node**, running in **dev mode** at first
- A daemon listens on a guest port; `taskmaster.dev` and/or a subdomain
  point at that process
- Auth: IdentiKey when their login UI exists; hop to that team, do not
  invent an IdP
- Actions: whatever that guest can do for the agent type (Playwright
  on the box when we need to see the UI)
- This kernel stays the source of objects and verbs; the app consumes them
- Backup, sync, and scale-out are later nodes, not this landing
