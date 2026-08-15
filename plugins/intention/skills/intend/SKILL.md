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

Load `../../references/shared.md` and `../../references/intend-dag.md`.
Read the citation table in `shared.md` from disk. Do not paste those files.

## Procedure

1. **Observe.** Code that the intention touches. `openspec/specs/` (built).
   `openspec/changes/*/proposal.md` excluding `archive/` and `PARKED`.
   `docs/LEARNINGS.md`. Who is available (human, which harnesses).
2. **Orient.** Load class × blast × lifecycle → rigor for the *highest*
   node. If you cannot name the capability, stay here.
3. **Skip?** Restore / typo / pin / comment / test-for-existing → print
   `direct fix` and stop. No DAG, no change.
4. **Split.** One acceptance surface per node. Landing is `add-<id>`,
   `brief`, or `direct fix`. Edges are real dependencies (B cannot start
   until A committed a usable artifact).
5. **Group.** Complementary jobs → `weave`. Contested expensive → `fork`
   only under the gates in `shared.md`. `ambiguous` / `sensitive` /
   architecture write → `human-gate`. Members are agents (or groups).
6. **Write** the DAG in the shape in `intend-dag.md`. Chat is enough;
   `.omc/intend/<slug>.md` if they want a file. No SHALLs in the DAG.
7. **Stop.** Report ready-set and what needs activation. Handoff:
   - change nodes → `change`
   - brief nodes → `brief`
   - ready + activated writes → `act`
   - never `fold` from here

Do not start write work on architecture or instrument nodes until the
human activates them.
