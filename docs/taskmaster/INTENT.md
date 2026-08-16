# Taskmaster — commander’s intent

Dated 2026-08-15. Duke, in the shared Mjolnir box.

## Outcome

A polished classic SaaS that helps you **master your tasks**.

The product *is* the work graph we already run: an intention, a DAG of
nodes, a ready-set, groups that assign and split, resources bound to
nodes, evidence that a node landed. A project is that graph with a
public address. Governing agents is not a different product.

The same dynamics apply to how we build Taskmaster itself: name the
problem, split it, assign it, use MetaCoding when the structure is
already in the code.

## Non-goals

- Forking the agent surface (packet in, signed result out)
- SHALLs in this marketplace’s living specs for a site that does not exist
- Building Tatastu, `intentional.agency`, or Mjolnir-the-product in this pass
- Pretending IdentiKey login is finished

## Constraints

- Web app: SvelteKit, SQLite via libsql
- Auth: IdentiKey (their login UI is incomplete — hop to that team when auth blocks us)
- Runtime: Mjolnir boxes; scale-out is more instances, not a bigger SQLite
- Writes to SQLite are serial, in arrival order
- This kernel stays the source of objects and verbs; the app consumes them
