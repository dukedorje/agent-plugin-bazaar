---
name: sprint-plan
description: Multi-phase sprint planning workflow that transforms product ideas into implementation-ready user stories with architecture decisions, requirements expansion, and adversarial validation
user-invocable: true
argument-hint: "[product-idea-or-prd-path] [--fast] [--thorough] [--auto] [--step] [--sprint-size=SIZE] [--continue[=phase]] [--restart-from=phase]"
---

# Sprint Plan Orchestrator

You are the orchestrator for a multi-phase sprint planning workflow. Follow these instructions precisely, phase by phase. You coordinate OMC agents to transform a product idea into implementation-ready user stories.

---

## 1. Argument Parsing

Parse `$ARGUMENTS` for the following:

1. **Product input**: The remaining text after flags are extracted. This may be:
   - A file path (check if it exists) pointing to a product idea, PRD, or brief
   - Inline text describing the product idea
   - Empty (prompt the user: "What would you like to build?")

2. **Flags**:
   - `--fast`: Single-pass mode. No RALPLAN-DR consensus loops. Decision Steering starts in AUTONOMOUS mode. Refinement loops disabled. Implies `--auto` (no inter-phase pauses).
   - `--thorough`: Full consensus mode. RALPLAN-DR active in Phases 2A/2B. Decision Steering starts in GUIDED mode. Refinement loops enabled.
   - `--auto`: Run all phases without pausing between them. Pauses only for Decision Steering elicitations in GUIDED mode.
   - `--step`: Pause after EVERY phase with a summary for user review. Maximum control.
   - `--sprint-size=SIZE`: Sprint sizing hint. Values: `focused` (1-2 epics, 3-8 stories — learning sprint, maximum steering), `standard` (2-4 epics, 8-18 stories — balanced, default), `ambitious` (4-6 epics, 15-30 stories — high confidence, full delivery). Used by Phase 1B (Sprint Scoping) to propose a sprint boundary. For sprint N>1, velocity data may override this unless explicitly set.
   - `--skip-ux`: Skip Phase 1.5 (UX Design) even if frontend requirements are detected and no UX artifacts exist.
   - `--continue`: Resume the current sprint from the next incomplete phase. Reads `phase-state.json` to auto-detect where to pick up. Optionally accepts a phase name (`--continue=<phase>`) to resume from a specific phase without re-running it.
   - `--restart-from=<phase>`: Re-run a specific phase and everything downstream. Use this when you want to redo a completed phase. Valid values: `discovery`, `requirements`, `sprint-scoping`, `ux-design`, `architecture`, `epic-design`, `story-decomposition`, `story-enrichment`, `validation`. Marks the specified phase and all downstream phases as stale.

If both `--fast` and `--thorough` are provided, `--thorough` wins.
If both `--continue` and `--restart-from` are provided, `--restart-from` wins (it's the more specific intent).
`--fast` implies `--auto`. `--step` overrides `--auto` if both are provided.

Store the parsed input for use throughout the workflow.

---

## 2. Initialization

### 2a. Determine Sprint Number

**Skip this step if `--continue` or `--restart-from` is set** — those flags resume an existing sprint (see 2g/2h).

1. Check `.omc/sprint-plan/` for existing `sprint-NNN/` directories.
2. If none exist, this is sprint 1 (`sprint-001`).
3. If directories exist, increment: find the highest NNN and use NNN+1.
4. Store the sprint number (zero-padded 3 digits).

### 2b. Create Sprint Directory

**Skip this step if `--continue` or `--restart-from` is set.**

```bash
mkdir -p .omc/sprint-plan/sprint-{NNN}/stories
mkdir -p .omc/sprint-plan/decisions
```

### 2c. Update Symlink

**Skip this step if `--continue` or `--restart-from` is set** — handled in 2g/2h.

```bash
rm -f .omc/sprint-plan/current
ln -s sprint-{NNN} .omc/sprint-plan/current
```

### 2c2. Write AGENTS.md

Write `.omc/sprint-plan/AGENTS.md` (create or overwrite). This is a static pointer so any agent working in the repo knows where sprint artifacts live:

```markdown
# Sprint Plan

Sprint planning artifacts are in `.omc/sprint-plan/current/` (symlink to active sprint).
Refer to files there for architecture decisions, requirements, story specs, and execution context.
```

This file is written once and does not need to be kept in sync — the `current` symlink handles resolution.

### 2d. Determine Mode

- All sprints default to `thorough` mode.
- Use `--fast` to opt into single-pass mode (no RALPLAN-DR, autonomous steering).
- Flags always override the default.

### 2e. Initialize phase-state.json

Write `.omc/sprint-plan/current/phase-state.json`:

```json
{
  "sprint": "sprint-{NNN}",
  "mode": "thorough|fast",
  "active": true,
  "current_phase": "discovery",
  "steering_mode": "GUIDED|AUTONOMOUS",
  "significance_calibration": [],
  "decisions_log": [],
  "sprint_size": null,
  "sprint_scope": null,
  "refinement_loops": {
    "requirements_architecture": { "count": 0, "max": 3 }
  },
  "refine_passes": {
    "requirements": 0,
    "architecture": 0,
    "epics": 0,
    "stories": 0,
    "enrichment": 0
  },
  "stale_phases": [],
  "epics_count": 0,
  "stories_total": 0,
  "stories_enriched": 0,
  "validation_status": "pending"
}
```

Set `steering_mode` to `GUIDED` if thorough, `AUTONOMOUS` if fast.

### 2f. Register with OMC State (optional)

If OMC state tools (`state_write`) are available, register the session. If unavailable, skip — the workflow uses `phase-state.json` as the primary state store.
```json
{
  "mode": "sprint-plan",
  "active": true,
  "current_sprint": "sprint-{NNN}",
  "session_id": "<generate unique id>"
}
```

### 2g. Handle --continue

If `--continue` is specified (with or without a phase argument):

1. Find the most recent sprint directory (highest `sprint-NNN/`). Do NOT create a new sprint directory — this resumes an existing one.
2. Read `phase-state.json` from that sprint.
3. **Without a phase argument** (`--continue`):
   - Read `current_phase` from `phase-state.json`.
   - Determine the next phase in the chain after `current_phase`. That is the resume point.
   - If `current_phase` is `"validation"`, report: "Sprint {NNN} is already complete."
4. **With a phase argument** (`--continue=<phase>`):
   - Verify the artifact for the specified phase already exists (it was completed previously).
   - The resume point is the next phase after the specified one.
5. Update `current_phase` in `phase-state.json` to the resume point.
6. Update the `current` symlink to point to this sprint directory.
7. Skip directly to the resume phase in the orchestration loop below.

Report to user: "Resuming sprint {NNN} from Phase {X}: {phase name}."

### 2h. Handle --restart-from

If `--restart-from=<phase>` is specified:
1. Find the most recent sprint directory (highest `sprint-NNN/`). Do NOT create a new sprint directory.
2. Read `phase-state.json` from that sprint.
3. Verify all artifact files for phases BEFORE the restart phase exist.
4. Update `current_phase` in `phase-state.json` to the restart phase.
5. Mark the restart phase and all downstream phases as stale in `stale_phases`.
6. Update the `current` symlink to point to this sprint directory.
7. Skip directly to the specified phase in the orchestration loop below.

Report to user: "Restarting sprint {NNN} from Phase {X}: {phase name}. Downstream phases marked stale."

---

## 3. Phase Orchestration

Execute phases sequentially. For each phase:
1. Read the phase instruction file from `${CLAUDE_SKILL_DIR}/phases/` for detailed agent prompts.
2. Load the previous phase's output artifact (context shedding -- load the file, do not rely on memory).
3. Dispatch to the appropriate agent(s).
4. Write the phase output to the correct file path.
5. Update `current_phase` and metrics in `phase-state.json`.
6. Run Decision Steering if the phase is in an active steering zone.
7. **Inter-Phase Summary & Pause** (see section 3a below).

### 3a. Inter-Phase Summary & Pause

After each phase completes (steps 1-6), determine whether to pause based on the pause mode:

**Pause modes**:

| Mode | Pauses after |
|------|-------------|
| Default | **Decision points only**: Requirements (Phase 1), Sprint Scoping (Phase 1B), Architecture (Phase 2A), Validation (Phase 5) |
| `--step` | Every phase |
| `--auto` / `--fast` | Never (proceeds immediately; only Decision Steering elicitations in GUIDED mode can pause) |

**Decision point phases** are where the user's input has the most impact — scope (requirements), sprint boundary (scoping), technology choices (architecture), and go/no-go (validation). Other phases are downstream work that flows from those decisions.

If the current phase is NOT a pause point for the active mode, skip the summary and proceed immediately.

**Summary format**:

```
═══════════════════════════════════════════════════
  Phase Complete: {phase_name}
═══════════════════════════════════════════════════

  Artifact: {artifact_path}

  What was produced:
    {2-4 bullet summary of the key outputs — e.g., "12 functional requirements",
     "5 architecture decisions (2 CRITICAL)", "3 epics with 11 stories"}

  Key decisions made:
    {list significant decisions from this phase, if any}
    {or "No significant decisions in this phase."}

  Things to consider:
    {1-3 items the user might want to review, steer, or discuss}
    {e.g., "FR7 (real-time sync) has high complexity — worth reviewing scope"}
    {e.g., "D-003 chose SSE over WebSocket — affects Stories 2.3, 3.1"}
    {e.g., "Epic 2 has 8 stories — close to the split threshold"}

  ─────────────────────────────────────────────────
  Next: {next_phase_name}

  Options:
    continue       — proceed to {next_phase_name}
    review         — open the artifact for detailed review
    edit           — make changes before proceeding
    /refine {phase}   — run a refinement pass on this phase
    /sprint-plan --restart-from={phase} — redo this phase
═══════════════════════════════════════════════════
```

Wait for user input before proceeding to the next phase.

**Phase-specific summary content**:

| Phase | "What was produced" highlights |
|-------|-------------------------------|
| Discovery | Tech stack, project type, existing artifacts found, new_repo flag |
| Requirements | FR count, NFR count, constraint count, open questions count |
| Sprint Scoping | FRs in scope vs deferred, estimated stories, sprint size, velocity basis |
| UX Design | Component count, screen count, interaction patterns |
| Architecture | Decision count by significance, consensus iterations used |
| Epic Design | Epic count, FR coverage %, dependency chain shape |
| Story Decomposition | Story count per epic, total stories, health flags |
| Story Enrichment | Stories enriched, avg file count per story, tech stack referenced |
| Validation | Pass/fail status, critical findings, auto-fixed count |

**"Things to consider"** — generate these by scanning the phase output for:
- High-significance decisions (CRITICAL/HIGH)
- Open questions or assumptions
- Health flags (epic too large, orphan FRs, uncovered decisions)
- Complexity hotspots
- Anything that changed from previous phases (if resuming)

If the user says "continue" (or equivalent), proceed to the next phase.
If the user provides feedback or edits, incorporate them before proceeding.

---

### Phase Chain

Execute phases by reading the instruction file from `${CLAUDE_SKILL_DIR}/phases/` for each phase. The phase file contains all agent prompts, dispatch rules, and output formats. Do not duplicate phase content here — the phase files are authoritative.

| Phase | File | Agent(s) | Pause? | Steering | Output |
|-------|------|----------|--------|----------|--------|
| 0: Discovery | `phase-0-discovery.md` | explore (haiku) | No (step only) | Dormant | `discovery.md` |
| 1: Requirements | `phase-1-requirements.md` | analyst+architect+explore (parallel) | **Yes** | Active | `requirements.md` |
| 1B: Sprint Scoping | `phase-1b-sprint-scoping.md` | analyst (opus) | **Yes** (negotiation) | Active (CRITICAL) | `sprint-scope.md` |
| 1.5: UX Design | `phase-1.5-ux-design.md` | designer (sonnet) | Conditional | Active | `ux-design.md` |
| 2A: Architecture | `phase-2a-architecture.md` | planner+architect+critic (RALPLAN-DR) | **Yes** | **Maximally Active** | `architecture-decisions.md` |
| 2B: Epic Design | `phase-2b-epic-design.md` | planner+architect+critic (RALPLAN-DR) | No (step only) | Active | `epics.md` |
| 3: Stories | `phase-3-story-decomposition.md` | planner+writer (per epic, sequential) | No (step only) | Dormant | Updates `epics.md` |
| 4: Enrichment | `phase-4-story-enrichment.md` | executor+doc-specialist (parallel within epic) | No (step only) | Dormant | `stories/*.md` |
| 5: Validation | `phase-5-validation.md` | critic+verifier (parallel) | Informational | Dormant | `readiness-report.md` |

**Phase-specific orchestration notes** (only what's NOT in the phase files):

- **Phase 1.5 trigger**: Run if `has_frontend: true` AND `has_ux_artifacts: false` AND not `--skip-ux` AND not `--fast`. Otherwise skip (set `ux_design_phase: "skipped"`).
- **Phase 2A refinement loop** (thorough only): After architecture decisions finalize, check if any decision creates new requirements. If yes, loop back to Phase 1 (incremental re-run), then Phase 2A re-runs. Max 3 iterations tracked in `refinement_loops.requirements_architecture.count`.
- **Phase 3 epic ordering**: Process epics sequentially — later epics reference patterns from earlier ones.
- **Phase 4 parallelism**: Stories parallel within each epic, sequential across epics (forward intelligence).
- **Phase 5 auto-fix**: If validation fails, dispatch agents to fix gaps (max 2 fix iterations). Present readiness report to user as final checkpoint.

---

## 4. Decision Steering System

**Full specification**: Read `${CLAUDE_SKILL_DIR}/phases/decision-steering.md` for the complete Decision Steering system including significance classification, self-calibration, elicitation format, and autonomy state machine.

**Key rules for the orchestrator**:
- `thorough` mode starts in **GUIDED** — HIGH and CRITICAL decisions trigger user elicitation
- `fast` mode starts in **AUTONOMOUS** — all decisions auto-decided with `[AUTO-DECIDED]` markers
- User can transition to AUTONOMOUS by saying "choose for me and automate the rest"
- Store first 3 user significance overrides in `phase-state.json` under `significance_calibration`
- Steering is active in Phases 1, 1B, 1.5, 2A, 2B; dormant in Phases 0, 3, 4, 5

---

## 5. State Management

### 5a. phase-state.json

This is the **single source of truth** for all workflow state. Update it after every phase transition and significant event.

**Required updates**:
- `current_phase`: Set when entering a new phase
- `steering_mode`: Updated on user autonomy transitions
- `significance_calibration`: Appended on user overrides (max 3)
- `decisions_log`: Appended for every decision made
- `refinement_loops`: Incremented on Requirements-Architecture loops
- `refine_passes`: Incremented on `refine` invocations
- `stale_phases`: Phases downstream of a re-run phase are added here
- `epics_count`, `stories_total`, `stories_enriched`: Updated as artifacts are produced
- `validation_status`: Set in Phase 5

### 5b. Stale Phase Tracking

When a phase is re-run (via `--restart-from`, `--continue`, or refinement loop):
1. Mark all downstream phases as stale in `phase-state.json`.
2. Stale phases must be re-run before the workflow can complete.
3. The orchestrator automatically re-runs stale phases in order.

**Phase chain for stale propagation** (in order):
`discovery` → `requirements` → `sprint-scoping` → `ux-design` → `architecture` → `epic-design` → `story-decomposition` → `story-enrichment` → `validation`

When `requirements` is marked stale, `sprint-scoping`, `ux-design` (if it ran), and all downstream phases are marked stale.
When `sprint-scoping` is marked stale, `ux-design` (if it ran), `architecture`, and all downstream phases are marked stale.
When `ux-design` is marked stale, `architecture` and all downstream phases are marked stale.

### 5c. OMC State (optional)

If available, use `state_write` and `state_read` with `mode="sprint-plan"` for OMC lifecycle management:
- `active`: Whether a sprint planning session is in progress
- `current_sprint`: Which sprint directory is active
- `session_id`: Current session identifier

If OMC state tools are not available, skip — the workflow functions correctly using `phase-state.json` alone.

**Boundary rule**: `phase-state.json` is NEVER read by OMC hooks. OMC state is NEVER read for phase logic. They are independent.

---

## 6. Progress Reporting

After each phase: report phase name, artifacts written, decisions made, and next phase. Present Decision Steering elicitations BEFORE reporting the phase complete.

At workflow completion: report sprint number, mode, epic/story counts, decision counts, validation status, readiness report path, and next steps (`/sprint-exec`, `/refine`, `/sprint-plan --continue`).

---

## 7. Codebase Context Handling

Every project gets a codebase inventory and context sections — there is no brownfield/greenfield split. Phase 0 detects `new_repo: true` only for brand-new repositories (< 10 source files, no build manifests or source directories). This flag is informational.

1. **Phase 0**: Always produce "Existing Codebase Inventory" section in `discovery.md` — project structure, tech stack, existing patterns, module boundaries.
2. **Phase 1**: Always dispatch `explore` (haiku) in parallel to scan for existing implementations (skip only for new repos). Requirements must account for existing features.
3. **Phase 2A**: Architecture decisions must consider existing patterns when they exist — "aligned with existing pattern X" or "diverges from existing pattern X because Y." Divergence requires justification in the ADR.
4. **Phase 4**: Every story file includes a `## Codebase Context` section with existing files to modify, patterns to follow, and integration points. Write "N/A" if no existing codebase context applies.

---

## 8. Error Recovery

### 8a. Phase Idempotency
Any phase can be re-run from scratch. Re-running a phase overwrites its output file. Downstream phases are marked stale in `phase-state.json` and must be re-run.

### 8b. Restart
`--continue` resumes from the next incomplete phase (auto-detected or explicit). `--restart-from=<phase>` re-runs a completed phase and marks downstream as stale. Both verify prerequisite artifacts exist before starting.

### 8c. Agent Failure
If an agent dispatch fails:
1. Retry once with the same prompt.
2. If the retry fails, present the error to the user with options:
   - Retry with different parameters
   - Skip the agent (if optional, e.g., `explore` in Phase 1 for new repos)
   - Abort the workflow

### 8d. Stale Phase Recovery
When phases are marked stale:
1. After the current phase completes, check `stale_phases`.
2. Re-run stale phases in order before proceeding to new phases.
3. Remove phases from `stale_phases` as they complete.

### 8e. Session Resume
On resume (workflow was interrupted):
1. Read OMC state to find the active sprint.
2. Read `phase-state.json` to determine last completed phase.
3. Check for stale phases.
4. Resume from the next incomplete phase.

---

## 9. The `refine` Command

The `refine` command triggers RALPLAN-DR refinement on any phase output, or an interactive epic deep-dive. This is handled by the separate `/refine` skill, but the orchestrator must support it:

- Track `refine_passes` per phase in `phase-state.json`
- Max 2 refinement passes per phase/scope (respond with diminishing returns message after 2; `--force` overrides)
- Each consensus pass: Planner reviews -> Architect challenges -> Critic validates
- On consensus: apply changes to the phase artifact
- On no consensus after 3 iterations: present disagreements via Decision Steering
- Mark downstream phases as stale after a refinement pass modifies an artifact
- When `--propagate` is used and ADRs change: auto-run reconcile to ripple changes
