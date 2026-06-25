---
name: sprint-from-beads
description: >
  Reverse-migrate an existing beads (`bd`) corpus into a structured sprint: cluster loose beads
  into epics, infer architecture decisions and a product narrative, and backfill acceptance criteria
  and design notes on tasks that lack them. Emits enriched work-item beads (in place) AND the planning
  narrative docs (PRD, architecture) you'd get from the full process. Additive by default; rewrites of
  existing bead content are proposed through an approval gate, never applied silently.
  Triggers on: sprint from beads, migrate beads to sprint, reverse migrate, plan over existing beads,
  beads to prd, structure my beads.
user-invocable: true
argument-hint: "[--scope=<epic-id|label|open|all|query>] [--into=sprint-NNN] [--ceremony=lean|standard|full] [--accept-rewrites] [--no-rewrites] [--dry-run] [--db=PATH]"
model: opus
---

# sprint-from-beads: Reverse Migration (Beads → Sprint)

The inverse of `sprint-to-beads`. Where that skill pushes a *planned sprint* into beads, this one reads an
*existing beads corpus* and reverse-engineers the planning structure over it — grouping loose work into
epics, inferring the architecture decisions and product story implied by the beads, and backfilling the
acceptance criteria and design notes that hand-authored beads usually lack.

It produces **both** outputs, honoring the task/doc boundary:
- **Work items** (epics, stories) → enriched **in place in beads** (the single source of truth for *what*)
- **Planning narrative** (PRD, requirements, architecture decisions) → committed **docs/** (the *why*) —
  the same documents the forward `sprint-plan` process would generate

Use this when you already live in `bd`, have a pile of beads, and want the planning artifacts (a PRD, an
architecture doc, structured epics with ACs) without re-entering everything by hand.

---

## Authority Model: Additive by Default, Rewrites Gated

This skill operates on beads **you** authored. It must never silently overwrite your content.

- **Additive** changes apply directly: creating epic/decision beads, re-parenting orphans, and filling a
  field that is **empty** (a task with no `acceptance_criteria` gets one). These are safe — they only add.
- **Rewrites** of a **non-empty** existing field (tightening a vague AC, rewording a thin description) are
  **proposed**, never auto-applied. They are collected and presented as a diff for approval. `--no-rewrites`
  skips them entirely; `--accept-rewrites` applies them without the interactive gate; default is to prompt.

This is the "enrich + propose rewrites" model: aggressive about filling gaps, conservative about touching
what you already wrote.

---

## 1. Initialization

### 1a. Ensure Beads Database

Run `bd status` (with `--db` if provided). If no database exists, halt: "sprint-from-beads reads an
existing beads corpus — no `.beads` database found here. Nothing to migrate." (Unlike `sprint-to-beads`,
this skill has nothing to do without an existing db.)

### 1b. Parse Arguments

| Flag | Default | Behavior |
|------|---------|----------|
| `--scope=<...>` | `open` | Which beads form the corpus. One of: an **epic id** (that epic + its children), a **label**, `open` (all non-closed beads), `all`, or a raw `bd query` string. See 1c. |
| `--into=sprint-NNN` | new sprint | Associate the migrated work with this sprint id (for labels + doc paths). If omitted, allocate the next `sprint-NNN` and derive a slug from the corpus. |
| `--ceremony=<level>` | auto | Force ceremony (`lean`/`standard`/`full`). Default: auto-derive from corpus size per `sprint-plan` Section 1.5. A beads-only project with a handful of items lands at `lean` — beads enriched, minimal docs. |
| `--accept-rewrites` | off | Apply proposed rewrites of existing fields without the interactive gate. |
| `--no-rewrites` | off | Skip rewrites entirely — additive changes only. |
| `--dry-run` | off | Print the full migration plan (every bead change + every doc to be written) without applying. |
| `--db=PATH` | auto | Pass `--db PATH` to every `bd` call. |

### 1c. Scope Guard

A beads-heavy project may have hundreds of beads. Resolve the scope, then count. If the corpus exceeds
**30 beads** and scope was the default (`open`), do **not** proceed blindly — report the count and the
detected epic/orphan breakdown, and ask the user to narrow scope (by epic, label, or query) or confirm
`--scope=all`. Migrating the wrong 300 beads is expensive to unwind.

---

## 2. Read & Classify the Corpus

### 2a. Load

1. `bd list --json` (filtered by scope) for the bead set.
2. For hierarchy and rich fields, `bd show <id> --json` per bead (or `bd children <epic> --json` per epic).
   **Do not trust `parent_id` from `bd list --json` — it is unreliable.** The authoritative parent is the
   `parent` field from `bd show --json`, and the hierarchical id suffix (`proj-995.1` → parent `proj-995`)
   corroborates it.
3. `bd dep tree` / `bd dep list` for existing dependency edges (preserve them — do not recreate).

### 2b. Classify

Sort the corpus into:
- **Epics** — `issue_type=epic`, or any bead with children.
- **Structured tasks** — tasks/features/bugs that already have a parent epic.
- **Orphans** — work items with no parent and no epic. These are the primary clustering candidates.
- **Gaps** — for every task-like bead: does it lack `acceptance_criteria`? lack `design`? These are the
  backfill targets.

Build a classification summary (counts per bucket, list of gaps). This drives the plan and the report.

---

## 3. Analyze (the planning intelligence)

Run the same reasoning the forward phases would, but with the beads as input. Scale depth to the resolved
ceremony (Section 1.5 of `sprint-plan`).

### 3a. Cluster orphans → epics

Group orphan beads by user-capability theme (the same "After this epic, users can…" grouping rule as
Phase 2B epic design). Propose an epic per cluster. A single coherent orphan can stand alone; do not
manufacture epics for the sake of structure. Existing epics are kept as-is (their boundaries are yours).

### 3b. Infer architecture decisions → doc + pointer beads

Inspect the corpus (and the actual codebase, if present) for implied or already-made architecture
decisions — the database in use, the auth model, key libraries, patterns the beads assume. Record them as
ADRs in the architecture doc (the source of truth). Only **CRITICAL/HIGH** decisions also get a lightweight
`decision` bead pointer, linked `related` to the beads they constrain (per the ADR-home rule shared with
`sprint-to-beads`). At `lean` ceremony with no significant decision, skip the architecture doc entirely.

### 3c. Infer the product narrative → PRD/requirements doc

From the corpus, synthesize the product story: what is being built, for whom, the functional requirements
the beads collectively imply. This becomes the PRD/requirements narrative doc (`standard`+ ceremony; at
`lean`, fold a 2–4 sentence goal into the sprint's epic descriptions instead of a standalone doc).

### 3d. Backfill ACs & design

For each gap bead, draft acceptance criteria (BDD) and/or design notes from the bead's title, description,
and surrounding context. Filling an **empty** field is additive (auto-apply). Replacing a **non-empty**
field is a rewrite (gated).

---

## 4. Build the Migration Plan

Assemble an ordered, labeled plan separating **additive** from **rewrite** actions:

**Additive (auto-apply unless `--dry-run`):**
1. Create proposed epic beads (`bd create -t epic ... --external-ref morphist:{sprint}:E{n}`).
2. Re-parent orphans into their epic (`bd update <id> --parent <epic-id>`).
3. Fill empty `acceptance_criteria` / `design` fields (`bd update <id> --acceptance ... --design ...`).
4. Create CRITICAL/HIGH `decision` pointer beads and `related` links.
5. Apply sprint labels (`{sprint}`) and `--external-ref` keys so the migrated set is self-describing and
   idempotent on re-run (same external-ref scheme as `sprint-to-beads`).

**Rewrites (proposed → gated):**
- Any change to a non-empty existing field. Each is collected as a `{bead, field, old, new, why}` proposal.

**Docs (written on apply):**
- PRD/requirements + architecture decisions under `docs/sprints/{NNN}-{slug}/` (or `docs/`), per ceremony.
  These are committed narrative — never duplicated into bead content.

Preserve all existing dependency edges. Never close or delete beads (this skill only adds and, with
approval, refines).

---

## 5. Dry-Run / Approval Gate

- If `--dry-run`: print the full plan — additive actions, rewrite proposals (as diffs), and the list of
  docs that would be written — then stop. Nothing is applied.
- Otherwise: apply additive actions, then handle rewrites:
  - `--no-rewrites` → skip, note the count of un-applied proposals.
  - `--accept-rewrites` → apply all.
  - default → present the rewrite proposals as a compact diff list and ask which to apply (all / none /
    select). Apply the chosen subset.

Report any `bd` failures with the failing command; continue with independent items; never swallow errors.

---

## 6. Write Docs & State

1. Write the narrative docs (PRD/requirements, architecture-decisions) per ceremony to the sprint's
   `SPEC_DIR` (`docs/sprints/{NNN}-{slug}/`). At `lean`, there may be none.
2. Initialize a `STATE_DIR` (`.omc/sprint-plan/sprint-{NNN}/`) with a `phase-state.json` describing the
   migrated sprint (`ceremony`, `beads_mode: true`, `source: "sprint-from-beads"`, `spec_dir`), so the
   normal `/status`, `/sprint-exec --beads`, `/refine` flows can pick it up.
3. Write `STATE_DIR/beads-map.json` (the ephemeral id-map, regenerable from `external_ref`).

### Final Report

```
Beads → Sprint {NNN}  (ceremony: {level})

  Corpus:     {n} beads ({e} epics, {s} structured, {o} orphans)
  Created:    {k} epics
  Re-parented:{j} orphans
  Backfilled: {a} acceptance criteria, {d} design notes  (additive)
  Decisions:  {c} CRITICAL/HIGH → doc + pointer beads
  Rewrites:   {r} proposed → {applied} applied, {skipped} skipped
  Docs:       {list of narrative docs written, or "none (lean)"}

Next:
  bd ready                 # unblocked work, now structured
  /status --sprint={NNN}   # sprint dashboard over the migrated beads
  /sprint-exec --beads     # execute, synced to bd
```

---

## 7. Known Limitations

- **Inference is a draft.** Clustered epics, inferred ADRs, and backfilled ACs are proposals grounded in
  the corpus — review them. The approval gate covers rewrites; for additive inference, the `--dry-run`
  preview is your checkpoint.
- **Existing structure is respected, not re-litigated.** Existing epics, parents, and dependency edges are
  kept as-is. To restructure aggressively, edit in `bd` first or use a forward `/refine` pass after.
- **Idempotent, additive re-runs.** Re-running enriches further (fills newly-empty gaps, picks up new
  orphans) without duplicating — external-ref keys dedupe. It will not undo a prior migration.
- **Requires `bd`.** No corpus, nothing to do.
