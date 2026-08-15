---
name: intend
description: >
  Capture an intention, observe the system, orient (load class × blast ×
  lifecycle), and split a DAG of named change-ids. Open groups when work is
  complementary or contested. Use when starting from a goal, "let's build
  this", or when asked to intend / plan work without a sprint factory.
user-invocable: true
argument-hint: "<intention>"
---

# intend

Conductor of the loop. You observe, orient, split, and assign. You do not
implement. You do not write a sprint folder.

Read, do not paste:

- `docs/from-intention-to-running.md` (commander’s intent)
- `docs/contracts/agent-surface.md`
- `docs/contracts/topologies.md`
- `openspec/specs/living-specs/spec.md`
- `openspec/specs/` (what is built)
- `docs/LEARNINGS.md`

## Procedure

1. **Observe.** Code, living specs, in-flight `openspec/changes/` (skip
   `archive/` and anything `PARKED`), learnings, who is available.
2. **Orient.** Load class (`structure-clear` / `intention-critical` /
   `ambiguous`) × blast × lifecycle → rigor
   (`vibe` / `brief` / `change` / `architecture` / `instrument`).
3. **Split.** Each node: one acceptance surface, a landing zone
   (`change-id`, `brief`, or `direct fix`). Edges are real dependencies.
   If you cannot name the capability, you are still in Orient.
4. **Groups.** Complementary pieces → `weave`. Contested expensive pieces
   → `fork` only under the fork gates. `ambiguous` / `sensitive` /
   architecture write → human member. A group is an agent.
5. **Write the DAG** where the user can see it (chat, or
   `.omc/intend/<slug>.md` if they want a file). Name change-ids. Do not
   put SHALLs in the DAG — those belong in a `change`.
6. **Stop.** Report the ready-set and which nodes need activation.
   Do not start write work on architecture+ nodes until the human activates.

Restore-only / typo / pin → say `direct fix` and stop. Do not open a change.

Packets you emit for later `act` must satisfy `docs/contracts/`. At
`change` rigor and above, set `capability`.
