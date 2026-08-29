---
name: intend
description: >
  Capture an intention, observe the system, orient (load class × blast ×
  lifecycle), and split a DAG of named change-ids. Open groups when work is
  complementary or contested. Use when starting from a goal, "let's build
  this", or when asked to intend / plan work without a sprint factory.
  --extract-from names beads/epics to read first (action records + insight).
user-invocable: true
argument-hint: "[--extract-from <items>] <intention>"
---

# intend

Conductor of the loop. You observe, orient, split, and assign. You do not
implement. You do not write a sprint folder.

Load `../../references/shared.md` and `../../references/intend-dag.md`.
Read the citation table in `shared.md` from disk. Do not paste those files.

## Procedure

1. **Observe.** If `--extract-from <items>` is set (usual: bead / epic
   ids, repeatable), read those records first: descriptions, acceptance,
   comments, close reasons, signed results, blocking edges that resolve.
   Report **records of action** and **insight into the intent** they
   imply. Do not dump transcripts. A missing or unreadable item is named
   **unresolved** — do not invent its trail. Then, with or without the
   flag: code that the intention touches. `openspec/specs/` (built).
   `openspec/changes/*/proposal.md` excluding `archive/` and `PARKED`.
   `docs/LEARNINGS.md`. Who is available (human, which harnesses).
   No flag keeps this blank-page observe; the run is not rejected for
   lacking extract-from. Dossier ids wait on `add-intend-extract-dossier`.
2. **Orient.** Load class × blast × lifecycle → rigor for the *highest*
   node. If you cannot name the capability, stay here.
3. **Skip?** Restore / typo / pin / comment / test-for-existing → print
   `direct fix` and stop. No DAG, no change.
4. **Split.** One acceptance surface per node. Landing is `add-<id>`,
   `brief`, or `direct fix`. Edges are real dependencies (B cannot start
   until A committed a usable artifact). Set `density` from
   `docs/contracts/dispatch.md` (capability order is the inverse of
   depth). Blast raises density, never lowers it. Assign with
   `python3 plugins/intention/scripts/ladder.py assign --shape …`
   (known → Sonnet 5, thinking → Opus 5, plan → Fable 5, design →
   Opus 5 + designer skills). Real architecture opens a review-pair
   whose reader is Grok.
5. **Group.** Complementary jobs → `weave`. Contested expensive → `fork`
   only under the gates in `shared.md`. `ambiguous` / `sensitive` /
   architecture write → `human-gate`. Members are agents (or groups).
6. **Write** the DAG in the shape in `intend-dag.md`. Chat is enough;
   beads (`bd create`) if they want a tracker. No `.omc/`. No SHALLs in the DAG.
7. **Stop.** Report ready-set and what needs activation. Pin this
   DAG as the session current (`map --current <root-id>`) so later
   `map` / elicitation stay on it. Handoff:
   - change nodes → `change`
   - architecture / instrument after `change` → `advise`
   - brief nodes → `brief`
   - ready + activated writes (advise accept, or no advise required) → `act`
   - never `fold` from here

Do not start write work on architecture or instrument nodes until the
human activates them.
