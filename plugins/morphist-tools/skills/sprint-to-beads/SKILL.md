---
name: sprint-to-beads
description: >
  Materialize an OpenSpec intake change (epics, stories, architecture decisions) into the beads
  issue tracker (`bd` binary) as the single source of truth. Emits ADRs as decision beads,
  epics as epic beads, and stories as task beads with acceptance criteria, design notes, and
  dependency edges. Idempotent — re-runs update existing beads rather than duplicating.
  Triggers on: sprint to beads, materialize to beads, push sprint to bd, beads from sprint.
user-invocable: true
argument-hint: "[--change=ID] [--swarm] [--dry-run] [--prune] [--db=PATH]"
model: sonnet
---

# sprint-to-beads: Intake Change → Beads Materializer

Reads the current `openspec/changes/<change-id>/` plan and writes its epics,
stories, and architecture decisions directly into beads (`bd`). Beads owns
story descriptions, acceptance criteria, and design notes. The change's
`tasks.md` mirrors one checkbox per acceptance, linked to the story bead.
Never create a stories directory, story markdown, or a story template.
Planning narrative stays in `proposal.md`, optional `design.md`, spec deltas,
and bounded ADRs in `ARCHITECTURE.md` when the shape changes.

This skill is the integration seam between morphist-tools (the planning
what/why) and beads (the execution where). `sprint-plan` invokes it at the
end of intake without a separate flag. It can also re-sync an existing change.

---

## When to Use

- **Automatically** — `sprint-plan` calls this skill at the end of intake, without a separate flag.
- **On-demand** — materialize an existing intake change:
  `/sprint-to-beads --change=add-account-recovery`
- **Re-sync** — after a change's plan changes, re-run to update the beads (idempotent).

Do **not** use this skill to:
- Plan a sprint (that's `/sprint-plan`)
- Execute work (that's `bd swarm` / `bd ready`, or `/sprint-exec --beads`)

---

## Core Principle: Single Source of Truth

When intake is materialized, beads holds task and epic content:

- A story's description, acceptance criteria, and design notes live in bead
  fields (`--description`, `--acceptance`, `--design`). `tasks.md` carries the
  acceptance checkboxes and bead references, not a competing story narrative.
- Architecture decisions are supplementary documentation. Their rationale
  stays in the change's `design.md` or a referenced `ARCHITECTURE.md` ADR.
  A decision bead is a lightweight pointer: title, one-line decision, source
  anchor, and `related` links to the stories it constrains.
- Idempotency comes from beads' stable `--external-ref` keys and the ids in
  `SPEC_DIR/tasks.md`. Keep the working id-map in memory; do not use OMC,
  phase-state files, symlinks, or an external cache as plan storage.

---

## 1. Initialization

### 1a. Change Resolution

1. Use `--change=<id>` if supplied; otherwise use the unambiguous current
   change passed by sprint-plan or established in session context. If
   ambiguous, ask which change rather than choosing the newest folder.
2. Set `CHANGE_ID` to that id and `SPEC_DIR` to
   `openspec/changes/<change-id>/`. Verify `proposal.md`, `tasks.md`, and
   applicable spec deltas exist. Read the disposition banner; materialization
   records intake work and does not grant implementation or activation authority.
3. Read phase progress, intake epic id, child handoffs, story bead ids and
   acceptance rows from `SPEC_DIR/tasks.md`. Resume there on re-sync.

Never read or write OMC sessions, an active-sprint key, or phase-state files.
If the change is missing, halt with its expected path and request the change
id or completed intake inputs.

### 1b. Parse Arguments

| Flag | Default | Behavior |
|------|---------|----------|
| `--change=ID` | current change | Target an existing OpenSpec change |
| `--swarm` | off | After materializing, run `bd swarm create` per epic so coordinators can pick up parallel work |
| `--dry-run` | off | Print the full bead plan (every `bd` command) without executing |
| `--prune` | off | Close beads whose external-ref belongs to this change but no longer appears in the plan (handles deleted stories on re-sync). Without it, stale beads are left open and reported. |
| `--db=PATH` | auto | Pass `--db PATH` to every `bd` call. Default: bd auto-discovers the project database. |

### 1c. Ensure Beads Database

Run `bd status` (with `--db` if provided). If it errors with "no beads database found":
- Halt and ask the user: "No beads database found in this project. Initialize one with `bd init --prefix <prefix>`? (a project prefix like `auth` or `app` is required)." Do **not** auto-init silently — the prefix is a durable project decision the user should make.

If the db exists, capture its issue prefix for reporting.

---

## 2. Load the Plan

Read `SPEC_DIR/proposal.md`, `tasks.md`, optional `design.md`, and spec deltas.
Use the story beads referenced by tasks.md as the authoritative story content.
During initial decomposition, accept the in-memory story records from Phases
3–4; write them directly to beads, never to an intermediate story file.

### 2a. Architecture Decisions → decision beads

Read decision sections in `SPEC_DIR/design.md` and any explicitly referenced
`ARCHITECTURE.md` ADRs. For each decision block, extract:
- `id` (e.g. `D-001`), `title`
- `significance` (CRITICAL/HIGH/MEDIUM → priority mapping below)
- The one-line **Decision** statement (NOT the full Context/Alternatives/Consequences body)

The `decision` bead is a **pointer, not a copy**: its description holds only the one-line decision plus a
reference to the source doc (`See openspec/changes/{change-id}/design.md#D-{NNN}` or the referenced `ARCHITECTURE.md` anchor). The
full rationale stays in the doc — beads does not duplicate it. This keeps the architecture narrative
single-sourced in the doc while letting `bd show` surface the decision against the stories it governs.

Only materialize decisions of significance CRITICAL or HIGH as beads (these are the ones that constrain
stories). MEDIUM/LOW decisions stay in the doc only — they don't earn a bead. Skip decisions whose
`Status` is `superseded by ...` (but materialize the superseding decision).

### 2b. Epics → epic beads

Read the intake epic and child handoff references in `SPEC_DIR/tasks.md`,
with scope and goals from `proposal.md`. Reuse the recorded intake epic;
if absent, create one for this change and record its id. For each epic, extract:
- `id` (`E{N}`), `title`, goal statement (→ description)
- Architecture constraints (decision IDs this epic references → linked later)
- `Depends on:` epic list (→ epic-level dependency edges)
- Estimated complexity (→ label)

### 2c. Stories → task beads

Resolve story ids and stable acceptance ids from `SPEC_DIR/tasks.md`, then
read their bead fields with `bd show <id> --json`. For initial Phase 3 input,
consume the decomposed story records directly from the caller's current
context. Existing beads remain authoritative on standalone re-sync; a
checkbox alone is not enough to reconstruct or overwrite story narrative.
If required content is missing, report the gap and leave intake unchecked.
Do not fall back to old story trees, stubs in epic documents, or templates.

For each story capture: `id` (`{epic}.{story}`), `title`, parent epic id, description (the user story +
scope), acceptance criteria (BDD text), design notes (Architecture Compliance + Technical Requirements),
`test_tier`, `complexity`, referenced decision IDs, and story-to-story dependencies.

---

## 3. Build the Bead Plan

Assemble an ordered plan. **Order matters** — referents must exist before referrers:

1. **Decision beads** (no dependencies on epics/stories)
2. **Epic beads**
3. **Story beads** (need the intake epic to exist → use real `--parent`)
4. **Epic→epic dependency edges**
5. **Story→story dependency edges** (`blocks`)
6. **Story→decision links** (`related`, non-blocking)

### External-Ref Keys (idempotency)

Every bead gets a stable `--external-ref` so re-runs update instead of duplicate:

| Kind | external-ref |
|------|--------------|
| Decision | `morphist:{change-id}:D-{NNN}` |
| Epic | `morphist:{change-id}:E{N}` |
| Story | `morphist:{change-id}:{epic}.{story}` |

Before creating any bead, load the existing map: run `bd list --all --limit 0 --json` (with `--db`) and index issues by
`external_ref`. For each plan item:
- **ref exists** → `bd update <id> ...` with explicitly revised intake fields; otherwise preserve bead content, status, and ownership
- **ref absent** → `bd create ...`, capture the new bead id, add it to the in-memory map

Reuse a Phase 2B epic recorded by id even if its external-ref is missing;
attach the change key to that same bead instead of creating a duplicate.
If an id and external-ref resolve to different beads, stop and report the
conflict. Never silently reparent unrelated work. This makes re-runs safe.

### Field Mapping

**Decision bead** (pointer only — CRITICAL/HIGH decisions only):
```
bd create "{D-NNN}: {title}" -t decision \
  --description "{one-line decision}. Rationale: see {source-path}#{decision-anchor}" \
  --priority {sig→pri} \
  --external-ref "morphist:{change-id}:D-{NNN}" \
  --labels "adr,{change-id}" --silent
```
The full Context/Alternatives/Consequences stays in the doc; the bead does not copy it.

**Epic bead:**
```
bd create "Epic {N}: {title}" -t epic \
  --description "{goal statement}" \
  --priority {complexity→pri} \
  --external-ref "morphist:{change-id}:E{N}" \
  --labels "epic,{change-id},complexity:{low|med|high}" --silent
```

**Story bead:**
```
bd create "Story {epic}.{story}: {title}" -t task \
  --parent {intake-epic-id} \
  --description "{user story + scope boundaries}" \
  --acceptance "{full BDD acceptance criteria text}" \
  --design "{architecture compliance + technical requirements}" \
  --priority {derived} \
  --external-ref "morphist:{change-id}:{epic}.{story}" \
  --labels "story,{change-id},tier:{test_tier},complexity:{complexity}" --silent
```

**Significance / complexity → priority** (bd priority is an int, 0=highest..4=lowest):
- CRITICAL → 0, HIGH → 1, MEDIUM → 2, (LOW/unspecified) → 3
- Epic/story complexity high → 1, medium → 2, low → 3

### Acceptance Checkboxes

After a story create/update succeeds, reconcile its acceptance criteria in
`SPEC_DIR/tasks.md`. Record the intake epic, story bead id, and external-ref.
Give each criterion a stable local id; a row can use this form:

```markdown
### Story {bead-id} — {title} (`morphist:{change-id}:{epic}.{story}`)
- [ ] {bead-id}/AC1: {complete acceptance criterion}
- [ ] {bead-id}/AC2: {complete acceptance criterion}
```

Write exactly one checkbox per criterion, including multiline BDD text in
that row. New criteria are open. On re-sync, match by bead id + acceptance id,
preserve unchanged checked rows, and reopen substantively revised criteria.
Record removals explicitly outside the active checklist rather than silently
losing history. Preserve unrelated intake, implementation, and fold tasks.
If the write fails after bead creation, retry by external-ref and reconcile
rows; do not mint another bead or mark the phase complete. No stories means
no story beads or acceptance rows; record the empty-scope reason.

### Dependency Edges

- Epic→epic: for each epic's `Depends on: E{k}`, run
  `bd dep add {this-epic-id} {dep-epic-id}` (this epic depends on / is blocked by the earlier epic).
- Story→story: for each declared dependency, `bd dep add {dependent-story-id} {blocker-story-id}`
  (blocks type, the default). This is what `bd swarm` reads to compute parallel waves — get it right.
- Story→decision: `bd dep add {story-id} {decision-id} --type related` (non-blocking; records that the
  story is governed by the decision so `bd show` surfaces it).

Guard against cycles: if the plan's story dependencies form a cycle, do not emit the cycle-closing edge —
report it instead (`bd dep cycles` can confirm post-hoc).

---

## 4. Dry-Run

If `--dry-run`: print the assembled plan as the literal ordered list of `bd` commands (with resolved
parent ids shown as `{ref}` placeholders for not-yet-created beads), plus a summary count
(`N decisions, M epics, K stories, J dep edges`) and the proposed acceptance
checkbox changes. Do not execute bd writes or edit tasks.md. Stop. Dry-run
is a preview, not intake completion.

---

## 5. Execute

Run the plan in the order from Section 3. For each `bd create`, capture the returned id (use `--silent`
so the id is the only output) and store it in the map keyed by external-ref before emitting any edge that
references it.

Reconcile acceptance checkboxes after each successful story write as above.

Batch sensibly but keep it observable — emit a progress line per kind
(`✓ 3 decisions, ✓ 4 epics, ✓ 14 stories, ✓ 9 dependency edges`).

If any `bd` call fails:
- Capture stderr, report the failing command, and continue with independent items where safe
  (a failed story doesn't block unrelated stories), but skip edges that reference a bead that failed to
  materialize. Summarize failures at the end. Never silently swallow an error.

### 5a. Prune (if `--prune`)

Query `bd list --all --limit 0 --json` for issues whose `external_ref` matches `morphist:{change-id}:*` but whose key is not
in the current plan. For each, `bd close <id> --reason "pruned: removed from change intake on re-sync"`.
Report what was pruned. Without `--prune`, list these as "stale (left open)" and recommend `--prune`.

### 5b. Swarm (if `--swarm`)

For each materialized epic, run `bd swarm validate {epic-id}` and, if swarmable, `bd swarm create
{epic-id}`. Report each epic's wave count and max parallelism. This hands execution to beads coordinators.

---

## 6. Record References & Report

Keep the id-map in memory and record the intake epic, story ids, stable
external-refs, and acceptance checkboxes in `SPEC_DIR/tasks.md`. Rebuild the
map on continuation from `bd list --all --limit 0 --json` and those references; do not
write an additional map file or use state tools. Beads owns story content.
Record materialization failures next to the unchecked intake phase.

### Final Report

```
Change {change-id} → beads ({db_prefix})

  Decisions:  {n}  (decision beads, linked to constraining stories)
  Epics:      {m}  → {epic ids}
  Stories:    {k}  (bead fields; acceptance mirrored in tasks.md)
  Dep edges:  {j}  ({story-story blocks} + {epic-epic} + {story-decision related})
  {if --swarm}  Swarms:  {created epic ids with wave counts}
  {if stale}    Stale:   {refs left open — pass --prune to close}

Next:
  bd ready                  # see unblocked work
  bd swarm status           # if --swarm was used
  # Return the change path, bead ids, acceptance count, and any failures
```

---

## 7. Known Limitations

- **Intake sync only.** This skill records work and acceptance; it does not
  execute stories, mark acceptance complete, activate changes, or fold living
  specs. Re-sync preserves bead content unless intake explicitly revises it.
  A standalone run needs existing bead content or current decomposed records;
  it cannot infer missing stories from acceptance checkboxes alone.
- **Decision link direction.** Story→decision uses `related` (non-blocking). A decision is not a gate on
  the story; it's reference context surfaced in `bd show`.
- **Requires `bd`.** If the `bd` binary is absent, halt with an install pointer — this skill has no
  fallback (its entire purpose is beads materialization).
