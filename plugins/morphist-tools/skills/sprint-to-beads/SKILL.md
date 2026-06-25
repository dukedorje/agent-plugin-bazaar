---
name: sprint-to-beads
description: >
  Materialize a planned sprint (epics, stories, architecture decisions) into the beads
  issue tracker (`bd` binary) as the single source of truth. Emits ADRs as decision beads,
  epics as epic beads, and stories as task beads with acceptance criteria, design notes, and
  dependency edges. Idempotent — re-runs update existing beads rather than duplicating.
  Triggers on: sprint to beads, materialize to beads, push sprint to bd, beads from sprint.
user-invocable: true
argument-hint: "[--sprint=ID] [--swarm] [--dry-run] [--prune] [--db=PATH]"
model: sonnet
---

# sprint-to-beads: Sprint → Beads Materializer

Reads a planned sprint and writes its epics, stories, and architecture decisions directly into
[beads](https://github.com/steveyegge/beads) (`bd`) as the durable, single source of truth for **work
items**. After materialization, **beads owns the task & epic information** — the `docs/sprints/.../stories/*.md`
story specs (if any) collapse into bead fields and are no longer a second system of reference for work
items. Planning **narrative** docs (PRD, requirements, architecture-decisions) are *kept* as committed
supplementary documentation — they are the "why," not a competing work-item store. Architecture rationale
stays doc-sourced; decision beads are lightweight pointers to it.

This skill is the integration seam between morphist-tools (the planning *what/why*) and beads (the
execution *where*). It is invoked automatically by `sprint-plan --beads`, or run standalone against any
already-planned sprint.

---

## When to Use

- **Automatically** — `sprint-plan --beads` calls this skill as its terminal phase.
- **On-demand** — materialize an existing sprint that was planned without `--beads`:
  `/sprint-to-beads --sprint=sprint-003`
- **Re-sync** — after `/refine` or `/replan` changes a sprint, re-run to update the beads (idempotent).

Do **not** use this skill to:
- Plan a sprint (that's `/sprint-plan`)
- Execute work (that's `bd swarm` / `bd ready`, or `/sprint-exec --beads`)

---

## Core Principle: Single Source of Truth

When a sprint is materialized to beads, **beads holds the task & epic content** — not a parallel set of
markdown story specs. Concretely:

- A story's description, acceptance criteria, and design notes live **in the bead's fields**
  (`--description`, `--acceptance`, `--design`), not in a `docs/sprints/.../stories/*.md` file that the
  bead merely points at. There is no `--spec-id` pointer to a competing story document.
- **Architecture decisions are the exception** — their rationale is *supplementary documentation*, which
  beads does not own. The full ADR rationale lives in `architecture-decisions.md` / `docs/decisions/`
  (the source of truth). The `decision` bead is a **lightweight pointer**: title + one-line decision +
  a reference to the doc, linked `related` to the stories it constrains. Beads carries enough to surface
  the decision in `bd show`; the doc carries the *why*. This mirrors the task/doc boundary: work items in
  beads, planning narrative in docs.
- The only retained out-of-band state is a tiny **ephemeral** id-map in `STATE_DIR` used purely for
  reporting; idempotency itself is derived from beads via `--external-ref` keys, so beads remains
  self-describing even if the map is deleted.

---

## 1. Initialization

### 1a. Sprint Resolution

Resolve the target sprint directories (per `templates/sprint-resolution.md`):
1. If `--sprint=<id>` was provided in `$ARGUMENTS`, set `STATE_DIR` = `.omc/sprint-plan/<id>/`
2. Else if `state_read` is available, read key `morphist.active_sprint`. If set, `STATE_DIR` = `.omc/sprint-plan/<value>/`
3. Else if `.omc/sprint-plan/current` symlink exists, `STATE_DIR` = `.omc/sprint-plan/current/`
4. Otherwise halt: "No active sprint found. Run `/sprint-plan` first, or pass `--sprint=<id>`."

Verify `STATE_DIR/phase-state.json` exists. Read it and set `SPEC_DIR` from the `spec_dir` field.
Verify `SPEC_DIR` exists. If not, halt: "Sprint spec directory not found at {spec_dir}."

Extract `sprint_number` (e.g. `sprint-003` → the canonical sprint id used in external-refs and labels).

### 1b. Parse Arguments

| Flag | Default | Behavior |
|------|---------|----------|
| `--sprint=ID` | resolved | Target a specific sprint |
| `--swarm` | off | After materializing, run `bd swarm create` per epic so coordinators can pick up parallel work |
| `--dry-run` | off | Print the full bead plan (every `bd` command) without executing |
| `--prune` | off | Close beads whose external-ref belongs to this sprint but no longer appears in the plan (handles deleted stories on re-sync). Without it, stale beads are left open and reported. |
| `--db=PATH` | auto | Pass `--db PATH` to every `bd` call. Default: bd auto-discovers `.beads/*.db`. |

### 1c. Ensure Beads Database

Run `bd status` (with `--db` if provided). If it errors with "no beads database found":
- Halt and ask the user: "No beads database found in this project. Initialize one with `bd init --prefix <prefix>`? (a project prefix like `auth` or `app` is required)." Do **not** auto-init silently — the prefix is a durable project decision the user should make.

If the db exists, capture its issue prefix for reporting.

---

## 2. Load the Plan

Read the sprint artifacts from `SPEC_DIR`. These are the planner's outputs; this skill is the consumer.

### 2a. Architecture Decisions → decision beads

Read `SPEC_DIR/architecture-decisions.md`. For each ADR block (`## D-{NNN}: {Title}`), extract:
- `id` (e.g. `D-001`), `title`
- `significance` (CRITICAL/HIGH/MEDIUM → priority mapping below)
- The one-line **Decision** statement (NOT the full Context/Alternatives/Consequences body)

The `decision` bead is a **pointer, not a copy**: its description holds only the one-line decision plus a
reference to the source doc (`See architecture-decisions.md#D-{NNN}` or the `docs/decisions/` path). The
full rationale stays in the doc — beads does not duplicate it. This keeps the architecture narrative
single-sourced in the doc while letting `bd show` surface the decision against the stories it governs.

Only materialize decisions of significance CRITICAL or HIGH as beads (these are the ones that constrain
stories). MEDIUM/LOW decisions stay in the doc only — they don't earn a bead. Skip decisions whose
`Status` is `superseded by ...` (but materialize the superseding decision).

### 2b. Epics → epic beads

Read `SPEC_DIR/epics.md`. For each `## Epic {N}: {Title}` section, extract:
- `id` (`E{N}`), `title`, goal statement (→ description)
- Architecture constraints (decision IDs this epic references → linked later)
- `Depends on:` epic list (→ epic-level dependency edges)
- Estimated complexity (→ label)

### 2c. Stories → task beads

Stories come from one of two places (check enriched first, fall back to stubs):
1. **Enriched** — `SPEC_DIR/stories/{epic}-{story}-{slug}.md` files. Parse frontmatter
   (`epic`, `story`, `status`, `decisions`, `test_tier`) and body sections (Story, Acceptance Criteria,
   Architecture Compliance / design notes, Tasks).
2. **Stubs** — if no enriched files exist, read the per-story stubs inside `SPEC_DIR/epics.md`
   (Phase 3 decomposition output). Extract title, ACs, `test_tier`, `complexity`, referenced `decisions`,
   and any declared cross-story dependencies.

For each story capture: `id` (`{epic}.{story}`), `title`, parent epic id, description (the user story +
scope), acceptance criteria (BDD text), design notes (Architecture Compliance + Technical Requirements),
`test_tier`, `complexity`, referenced decision IDs, and story-to-story dependencies.

---

## 3. Build the Bead Plan

Assemble an ordered plan. **Order matters** — referents must exist before referrers:

1. **Decision beads** (no dependencies on epics/stories)
2. **Epic beads**
3. **Story beads** (need their parent epic to exist → use real `--parent`)
4. **Epic→epic dependency edges**
5. **Story→story dependency edges** (`blocks`)
6. **Story→decision links** (`related`, non-blocking)

### External-Ref Keys (idempotency)

Every bead gets a stable `--external-ref` so re-runs update instead of duplicate:

| Kind | external-ref |
|------|--------------|
| Decision | `morphist:{sprint}:D-{NNN}` |
| Epic | `morphist:{sprint}:E{N}` |
| Story | `morphist:{sprint}:{epic}.{story}` |

Before creating any bead, load the existing map: run `bd list --json` (with `--db`) and index issues by
`external_ref`. For each plan item:
- **ref exists** → `bd update <id> ...` with the current fields (content may have changed since last sync)
- **ref absent** → `bd create ...`, capture the new bead id, add it to the in-memory map

This makes the skill safe to run repeatedly (e.g. after `/refine`).

### Field Mapping

**Decision bead** (pointer only — CRITICAL/HIGH decisions only):
```
bd create "{D-NNN}: {title}" -t decision \
  --description "{one-line decision}. Rationale: see architecture-decisions.md#D-{NNN}" \
  --priority {sig→pri} \
  --external-ref "morphist:{sprint}:D-{NNN}" \
  --labels "adr,{sprint}" --silent
```
The full Context/Alternatives/Consequences stays in the doc; the bead does not copy it.

**Epic bead:**
```
bd create "Epic {N}: {title}" -t epic \
  --description "{goal statement}" \
  --priority {complexity→pri} \
  --external-ref "morphist:{sprint}:E{N}" \
  --labels "epic,{sprint},complexity:{low|med|high}" --silent
```

**Story bead:**
```
bd create "Story {epic}.{story}: {title}" -t task \
  --parent {epic-bead-id} \
  --description "{user story + scope boundaries}" \
  --acceptance "{full BDD acceptance criteria text}" \
  --design "{architecture compliance + technical requirements}" \
  --priority {derived} \
  --external-ref "morphist:{sprint}:{epic}.{story}" \
  --labels "story,{sprint},tier:{test_tier},complexity:{complexity}" --silent
```

**Significance / complexity → priority** (bd priority is an int, 0=highest..4=lowest):
- CRITICAL → 0, HIGH → 1, MEDIUM → 2, (LOW/unspecified) → 3
- Epic/story complexity high → 1, medium → 2, low → 3

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
(`N decisions, M epics, K stories, J dep edges`). Do not execute. Stop.

---

## 5. Execute

Run the plan in the order from Section 3. For each `bd create`, capture the returned id (use `--silent`
so the id is the only output) and store it in the map keyed by external-ref before emitting any edge that
references it.

Batch sensibly but keep it observable — emit a progress line per kind
(`✓ 3 decisions, ✓ 4 epics, ✓ 14 stories, ✓ 9 dependency edges`).

If any `bd` call fails:
- Capture stderr, report the failing command, and continue with independent items where safe
  (a failed story doesn't block unrelated stories), but skip edges that reference a bead that failed to
  materialize. Summarize failures at the end. Never silently swallow an error.

### 5a. Prune (if `--prune`)

Query `bd list --json` for issues whose `external_ref` matches `morphist:{sprint}:*` but whose key is not
in the current plan. For each, `bd close <id> --reason "pruned: removed from sprint plan on re-sync"`.
Report what was pruned. Without `--prune`, list these as "stale (left open)" and recommend `--prune`.

### 5b. Swarm (if `--swarm`)

For each materialized epic, run `bd swarm validate {epic-id}` and, if swarmable, `bd swarm create
{epic-id}`. Report each epic's wave count and max parallelism. This hands execution to beads coordinators.

---

## 6. Persist the ID Map & Report

Write `STATE_DIR/beads-map.json` (ephemeral, gitignored) for reporting and fast re-sync:
```json
{
  "sprint": "sprint-003",
  "db_prefix": "auth",
  "materialized_at": "{ISO 8601}",
  "decisions": { "D-001": "auth-8qv" },
  "epics": { "E1": "auth-rw6" },
  "stories": { "1.1": "auth-rw6.1" }
}
```
This file is a convenience cache, **not** a source of truth — it can be regenerated at any time from
`bd list --json` by reading `external_ref` values. Do not write story/epic *content* here.

If `state_write` is available, record `{ mode: "sprint-to-beads", sprint, epic_count, story_count }`
(non-blocking; skip if unavailable).

### Final Report

```
Sprint {NNN} → beads ({db_prefix})

  Decisions:  {n}  (decision beads, linked to constraining stories)
  Epics:      {m}  → {epic ids}
  Stories:    {k}  ({enriched|stub} source)
  Dep edges:  {j}  ({story-story blocks} + {epic-epic} + {story-decision related})
  {if --swarm}  Swarms:  {created epic ids with wave counts}
  {if stale}    Stale:   {refs left open — pass --prune to close}

Next:
  bd ready                  # see unblocked work
  bd swarm status           # if --swarm was used
  /sprint-exec --beads      # drive execution via OMC executors, synced to bd
```

---

## 7. Known Limitations

- **One-way push.** This skill writes plan → beads. It does not read bead status back into sprint
  artifacts (that's `/sprint-exec --beads`'s and `/status --beads`'s job). Editing a bead's content in
  `bd` and then re-running this skill will **overwrite** that field from the plan — beads is downstream of
  the plan for content, source-of-truth for *status*.
- **Stub fidelity.** Materializing from story stubs (Phase 4 skipped) yields thinner `--acceptance`/
  `--design` fields than enriched stories. Run `sprint-plan --write-stories` first for richer beads.
- **Decision link direction.** Story→decision uses `related` (non-blocking). A decision is not a gate on
  the story; it's reference context surfaced in `bd show`.
- **Requires `bd`.** If the `bd` binary is absent, halt with an install pointer — this skill has no
  fallback (its entire purpose is beads materialization).
