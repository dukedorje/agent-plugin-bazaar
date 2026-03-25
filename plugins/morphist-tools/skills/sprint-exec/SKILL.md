---
name: sprint-exec
description: Execute validated sprint stories by dispatching executor agents. Default: next epic. Use --full-auto for all remaining epics, --next-story for one story at a time.
user-invocable: true
argument-hint: "[--epic=N] [--story=N.M] [--next-story] [--full-auto] [--dry-run] [--concurrency=N]"
---

# sprint-exec: Story Execution Orchestrator

You are the `sprint-exec` skill for the sprint-plan plugin. You read validated story files and dispatch executor agents to implement them.

---

## 1. Initialization

### 1a. Read Readiness Report

Read `.omc/sprint-plan/current/readiness-report.md`.

If the file does not exist, halt:
```
No readiness report found. Run /sprint-plan first to complete validation, or run /sprint-plan --continue to resume where you left off.
```

Check the `validation_status` field in the report. It must be `pass` or `pass-with-warnings`.

If `validation_status` is any other value (e.g., `fail`), halt:
```
Sprint has not passed validation. Run `/sprint-plan --continue` to resume, or `/sprint-plan --restart-from=validation` to re-run validation.
```

If `validation_status` is `pass-with-warnings`, display the warnings before proceeding:
```
Note: Sprint passed validation with warnings:
{list warnings from report}

Proceeding with execution...
```

### 1b. Read Phase State

Read `.omc/sprint-plan/current/phase-state.json`.

Extract:
- `sprint_number` (or `sprint` field): the current sprint identifier
- Epic count: determine from `current/epics.md` (count `## Epic` headings)

### 1c. Parse Arguments

Parse `$ARGUMENTS` for the following optional flags:

| Flag | Default | Behavior |
|------|---------|----------|
| `--epic=N` | — | Execute only epic N |
| `--story=N.M` | — | Execute only story N.M |
| `--next-story` | off | Execute only the next unfinished story (first `ready-for-dev` story in the first incomplete epic) |
| `--auto` | off | Execute ALL remaining epics sequentially. Stops on epic failure or architectural blockers (asks user). Does not stop on individual story failures within an epic. |
| `--full-auto` | off | Execute ALL remaining epics without stopping for ANY user confirmation. Auto-resolves failures (proceed to next epic) and blockers (accept partial). |
| `--stop-at=LEVEL` | varies | Decision severity threshold for pausing. Values: `critical`, `high`, `medium`, `all`. Default: `high` (default mode), `high` (`--auto`), `critical` (`--full-auto`). |
| `--dry-run` | off | Show execution plan without dispatching agents |
| `--concurrency=N` | unlimited | Max executor agents running simultaneously within an epic |

**Default scope** (no scope flags): execute only the **next incomplete epic** — the first epic whose `epic_status` is not `"done"`. This keeps execution incremental and controllable.

**Scope precedence**: `--story` > `--next-story` > `--epic` > default (next epic) > `--auto` (all remaining, stop on failure) > `--full-auto` (all remaining, never stop).

If `--story=N.M` is specified, `--epic` is inferred from the story number (N).

If `--next-story` is specified, determine the target by:
1. Find the first epic whose `epic_status` is not `"done"`
2. Within that epic, find the first story with `status: ready-for-dev` (or `in-progress` if resuming)
3. Execute only that single story
4. If no unfinished stories remain, report: `All stories are complete. Nothing to execute.`

### 1c-2. Decision Severity & Stop Threshold

During execution, decision points arise at blocker triage, verification failures, and executor-reported concerns. Each decision point has a severity:

| Severity | Examples |
|----------|----------|
| `critical` | Architectural blocker (`library_incompatible`, `architecture_mismatch`), all stories in epic failed, verification FAIL on a core story |
| `high` | Multiple story failures in an epic, verification FAIL on non-core stories, executor flagged `blocker_type: dependency_missing` |
| `medium` | Single story failure, verification CONCERNS, executor completion notes contain "workaround" or "TODO" |
| `low` | Verification all-PASS with minor notes, individual story retry succeeded |

**Stop behavior by mode**:

| Mode | Default `--stop-at` | Stops for | Auto-resolves |
|------|---------------------|-----------|---------------|
| Default (next epic) | `high` | `critical` + `high` | `medium` + `low` (proceeds automatically) |
| `--auto` | `high` | `critical` + `high` | `medium` + `low` (proceeds automatically) |
| `--full-auto` | `critical` | Only `critical` if explicitly set via `--stop-at=critical` | Everything by default |

`--stop-at` overrides the default for any mode. For example:
- `--auto --stop-at=critical` — runs all epics, only stops on critical issues
- `--full-auto --stop-at=high` — full auto but still stops on high-severity decisions
- `--stop-at=all` — default next-epic mode but pauses on every decision point (maximum control)
- `--stop-at=medium` — auto-resolves only low-severity items

When a decision point is **below the stop threshold**, auto-resolve using the least-disruptive option:
- Blocker triage: accept partial (option 3)
- Verification failure: proceed with concerns logged
- All-epic failure: proceed to next epic

Log all auto-resolved decisions to `execution_log` with `"auto_resolved": true` and the severity level.

---

### 1d. Check Existing Execution Status

If `execution_status` already exists in `phase-state.json`:
- If `"complete"`: Inform the user and suggest targeted re-runs:
  ```
  This sprint has already been fully executed (execution_status: complete).
  Use --story=N.M to re-run a specific story, --epic=N for an epic, or --full-auto to re-run all.
  ```
  Stop here unless an explicit scope flag was provided (`--story`, `--epic`, or `--full-auto`).
- If `"in-progress"`: Resume from where execution left off — skip stories already in `execution_log` with status `done`. Also check `epic_status` to skip epics already marked `"done"`.
- If `"halted"`: Inform the user that execution was previously halted for replanning:
  ```
  Sprint execution was halted for replanning.
  Reason: {halt_reason from phase-state.json}
  Halted at: {halted_at from phase-state.json}

  Resume execution? Stories/epics already marked done will be skipped.
  Use --story=N.M to re-run a specific story, or confirm to resume all remaining.
  ```
  Wait for user confirmation. Then resume using the same logic as `"in-progress"` — skip stories already in `execution_log` with status `done`, and skip epics already marked `"done"` in `epic_status`.

### 1e. Update Phase State

**Important**: Do NOT modify `current_phase`. It must remain at `"validation"` (its Phase 5 value). Only add sibling fields.

Update `phase-state.json` by adding or updating these sibling fields alongside `current_phase`:

```json
{
  "current_phase": "validation",
  "stale_phases": [],
  "execution_status": "in-progress",
  "execution_log": [],
  "epic_status": {}
}
```

The `epic_status` object tracks per-epic completion state. Keys are epic numbers (as strings), values are `"pending"` | `"in-progress"` | `"done"` | `"partial"` | `"failed"`. Initialize all epics (in scope) to `"pending"`. Preserve existing `epic_status` if resuming.

Preserve the existing `execution_log` array if resuming a partial execution.

### 1f. Register with OMC State

If OMC state tools are available, register the session (non-blocking — skip if unavailable):
```
state_write({ mode: "sprint-exec", sprint: "{sprint_number}" })
```

---

## 2. Dry-Run Mode

If `--dry-run` was specified, print the execution plan and stop (do not dispatch any agents):

```
--- Sprint Exec Dry Run ---
Sprint: {sprint_number}

Execution Plan:
Epic 1: {epic_title}
  Story 1.1: {story_title} [ready-for-dev] → will execute
  Story 1.2: {story_title} [blocked] → will SKIP
  Story 1.3: {story_title} [done] → will SKIP (already done)

Epic 2: {epic_title}
  Story 2.1: {story_title} [ready-for-dev] → will execute
  Story 2.2: {story_title} [ready-for-dev] → will execute

Concurrency: {concurrency_limit or "unlimited"} stories per epic; epics run sequentially.
To execute: /sprint-exec (remove --dry-run)
```

Stop here if `--dry-run`.

---

## 3. Load Stories

### 3a. Read Epic Ordering

Read `current/epics.md` to determine:
- The ordered list of epics
- The stories belonging to each epic (by heading structure)

### 3b. Resolve Story Files

Stories are located at:
```
.omc/sprint-plan/current/stories/{epic}-{story}-{slug}.md
```
For example, story 2.3 "User Authentication" → `.omc/sprint-plan/current/stories/2-3-user-authentication.md`

Use Glob to find story files matching the pattern `current/stories/{epic}-*` for a given epic.

For each story, read its frontmatter to get current `status`.

### 3c. Filter by Scope

Apply scope filtering based on parsed arguments (in precedence order):
- If `--story=N.M`: only include that single story
- If `--next-story`: only include the next unfinished story (see section 1c for resolution logic)
- If `--epic=N`: only include stories in epic N
- If `--auto`: include all stories across all remaining epics (stops on epic failure/blockers)
- If `--full-auto`: include all stories across all remaining epics (never stops)
- Default (no scope flags): only include stories in the **next incomplete epic** — the first epic whose `epic_status` is not `"done"` in `phase-state.json`. If all epics are `"done"`, report completion and stop.

Within the filtered set, apply status filtering:
- Skip stories with `status: blocked` (log as skipped)
- Skip stories with `status: done` (already complete — log as skipped unless re-run requested)
- Include stories with `status: ready-for-dev` or `status: in-progress` (in-progress means a previous run was interrupted)

---

## 4. Execution Loop

Process epics SEQUENTIALLY. Within each epic, dispatch eligible stories in PARALLEL, respecting `--concurrency=N` if set. When concurrency is limited, dispatch up to N stories at once, and as each completes, dispatch the next eligible story until all stories in the epic are done.

### 4a. Pre-Epic: Update Epic Status

Before processing any stories in an epic:

1. Update `epic_status` in `phase-state.json`: set epic N to `"in-progress"`
2. Update `epics.md`: add or update a `Status: in-progress` line under the `## Epic N` heading (insert after the `### Goal` section if not present)

### 4b. Pre-Dispatch: Update Story Status

Before dispatching an executor for a story:

1. Read the story file
2. Update frontmatter:
   - `status: in-progress`
   - `started_at: {ISO 8601 timestamp}`
3. Write the updated story file back

### 4c. Dispatch Story Executors (Parallel Within Epic)

For each story in the current epic (all in parallel via simultaneous Agent calls):

```python
Agent(
    subagent_type="oh-my-claudecode:executor",
    model="sonnet",  # default; escalate to opus on retry after failure
    prompt="""
You are implementing a story from the sprint plan.

Working directory: {working_directory}
Sprint directory: .omc/sprint-plan/current/
Story file: {story_file_path}
Story: {story_title} ({story_id})
Acceptance criteria count: {ac_count}
Key architecture decisions: {decision_ids_csv}

Instructions:
1. Read the story file at {story_file_path} — it contains the full specification and acceptance criteria.
2. Implement every requirement in the story.
3. Follow the architecture decisions and file list specified.
4. When complete, fill in the "Dev Agent Record" section at the bottom of the story file with:
   - Agent Model Used
   - Completion Notes (what you did)
   - Any problems encountered
   - Blocker Type (if you could NOT complete the story, classify why):
     - `none` — completed successfully
     - `coding` — normal bug or implementation difficulty (retry-able)
     - `library_incompatible` — a specified library/framework does not support the required use case
     - `architecture_mismatch` — an architecture decision doesn't hold in practice
     - `dependency_missing` — depends on something that doesn't exist or isn't ready yet
     - `spec_unclear` — the story spec is ambiguous or contradictory
   - Blocker Detail (if Blocker Type is not `none`): 1-2 sentences explaining what specifically doesn't work and why
   - Files created or modified (File List)
5. Do not modify any section of the story file above the Dev Agent Record.
6. IMPORTANT: If you encounter a fundamental blocker (library doesn't work, architecture assumption is wrong),
   do NOT silently work around it or deliver a partial solution. Set the Blocker Type and Detail clearly
   so the orchestrator can surface it for a human decision.
7. If the story frontmatter contains a `tdd_tests` field, run those tests after implementation.
   All listed tests must pass before the story is considered done. Do not delete or weaken tests.
   Report test results in the Completion Notes.
""",
)
```

**Context efficiency**: Do NOT inject the full story file content into the executor prompt. The executor agent can read the file itself. Pass only the file path and a brief summary (title, AC count, key decision IDs) to orient the agent. This saves 2,000-4,000 tokens per story from the orchestrator's context window.

### 4d. Post-Completion: Validate & Update Story Status

**IMPORTANT**: Update story status **immediately** as each individual agent returns — do NOT batch updates until the end of the epic. This ensures that if the session is interrupted mid-epic, completed stories are already persisted as `done` and won't be re-executed on resume.

As each story executor completes, run the `/done-validate --story=N.M --update` skill to:
1. Check Dev Agent Record completeness
2. Verify file existence (done-validation gate)
3. Check acceptance criteria coverage
4. Extract blocker classification
5. Determine final outcome (`done` | `failed` | `blocked`)
6. Update story frontmatter and `execution_log` in `phase-state.json`

See the `done-validate` skill for full validation logic. Each story's status is persisted to disk immediately (not batched). This is the source of truth for resume (section 1d) and for `/sprint-review`.

### 4e. Handle Failures Within an Epic

If an executor fails on a story:
- Mark `status: failed` on the story frontmatter
- Log the failure to `execution_log`
- Continue dispatching/completing remaining stories in the epic (do not abort the epic for one failure)

If ALL stories in an epic fail:
- If `--full-auto`: automatically proceed to the next epic (option 1). Log the auto-decision to `execution_log`:
  ```json
  { "type": "auto_proceed", "epic": N, "reason": "all stories failed, --full-auto active" }
  ```
- If `--auto` or default: halt and ask the user. Both default and `--auto` use `--stop-at=high`, which stops on epic-level failures.
- Otherwise (if `--stop-at=all` was explicitly set), also halt and ask:
  ```
  All stories in Epic {N} failed. Possible causes: missing dependencies, environment issues, or ambiguous story spec.

  Options:
  1. Proceed to Epic {N+1} anyway (stories from this epic will be missing)
  2. Abort execution (use /sprint-exec --epic=N to retry this epic)
  3. Retry individual stories with opus: /sprint-exec --story=N.M

  How would you like to proceed?
  ```
  Wait for user input.

### 4f. Post-Epic: Update Epic Status

After all stories in an epic have completed (or been skipped), determine and persist the epic's status:

1. Determine epic outcome:
   - If all stories are `done` (or `done` + skipped-as-already-done): epic status = `"done"`
   - If some stories are `done` and some `failed`: epic status = `"partial"`
   - If all stories `failed`: epic status = `"failed"`
   - If all stories were skipped (blocked or already done): epic status = `"done"`
2. Update `epic_status` in `phase-state.json`: set epic N to the determined status
3. Update `epics.md`: set `Status: {done|partial|failed}` under the `## Epic N` heading

This must happen **before** the progress report so that the persisted state is accurate if the session is interrupted.

### 4f-2. Context Checkpoint

After updating epic status, write a resume checkpoint to `phase-state.json`:

```json
{
  "resume_point": {
    "last_completed_epic": N,
    "next_epic": N+1,
    "timestamp": "{ISO 8601}"
  }
}
```

This checkpoint enables seamless resume if the context window is exhausted mid-sprint. When the user types "continue" or re-invokes `/sprint-exec`, the skill reads `resume_point` and skips directly to the next epic without re-processing completed work. Combined with `epic_status` and `execution_log`, this provides full resume fidelity.

### 4g. Blocker Triage

After updating epic status, check whether any failed stories in this epic have architectural blockers (`blocker_type` is `library_incompatible`, `architecture_mismatch`, or `dependency_missing`).

If there are **no architectural blockers**, skip to 4h.

If there **are** architectural blockers:
- If `--full-auto`: invoke `/blocker-triage --epic={N} --auto-accept`
- Otherwise: invoke `/blocker-triage --epic={N}`

See the `blocker-triage` skill for the full flow (impact analysis, 4-option resolution, architecture decision updates). If blocker-triage results in a halt (option 4), stop execution. Otherwise continue to 4h.

### 4h. Verification Gate

After blocker triage (or skipping it), invoke `/verify --epic={N}` to run independent verification of the epic's completed stories.

Skip this step if:
- The epic had zero completed stories (all failed or blocked)
- The scope is `--next-story` (single-story execution doesn't trigger epic-level verification)

**Gate behavior**:
- All stories PASS: proceed normally
- CONCERNS only: show results, proceed (concerns are non-blocking)
- Any FAIL + `--full-auto`: log failures to `verification_log` in `phase-state.json`, proceed
- Any FAIL + default or `--auto` (`--stop-at=high`): pause and ask:
  ```
  Verification found failures in Epic {N}. Fix before proceeding?

  1. Proceed to Epic {N+1} anyway
  2. Re-run failed stories: /sprint-exec --story=N.M
  3. Deep audit: /audit --epic={N}
  ```
  Wait for user input.

---

### 4i. Epic Progress Report

After all stories in an epic complete (or are skipped), generate the progress report using the `exec-report` skill (internal). See the `exec-report` skill for the full format.

### 4j. Background Code Review (optional)

After reporting epic completion, dispatch the `sprint-review` skill in the background to review the epic's work while the next epic starts executing. This is non-blocking — execution continues immediately.

Skip this step if the epic had zero completed stories or if all stories failed.

This is equivalent to running `/sprint-review --epic={N}` in the background. Use the same agent dispatch defined in the sprint-review skill (section 3), with `run_in_background=True`.

Review results accumulate in `current/reviews/` and are available for the user to check at any time. They do NOT block execution. The user can also run `/sprint-review` manually at any point.

### 4k. Notification (optional)

If OMC notification tools are configured (via `/configure-notifications`), send a notification on epic completion. This is non-blocking — skip gracefully if notifications are not set up.

Message format:
```
Sprint {sprint_number} — Epic {N} complete: {epic_title}
{done_count}/{total_count} stories done, {failed_count} failed
Review: .omc/sprint-plan/current/reviews/epic-{N}-review.md
```

Also send a notification on full sprint execution completion (section 6).

---

## 5. Retry Behavior

When `--story=N.M` is used (typically for retrying a failed story):
- Use `model="opus"` for the executor agent instead of `"sonnet"`
- Include additional context in the prompt about the previous failure if available in the execution_log

```python
Agent(
    subagent_type="oh-my-claudecode:executor",
    model="opus",  # escalated model for retry
    prompt="""
You are retrying a story implementation that previously failed.

Working directory: {working_directory}
Sprint directory: .omc/sprint-plan/current/
Story file: {story_file_path}
Story: {story_title} ({story_id})

Previous failure context:
{failure_notes_from_execution_log_if_available}

Instructions:
1. Read the story file at {story_file_path} — it contains the full specification and acceptance criteria.
2. Implement every requirement in the story.
3. Follow the architecture decisions and file list specified.
4. When complete, fill in the "Dev Agent Record" section at the bottom of the story file with:
   - Agent Model Used
   - Completion Notes (what you did and how you resolved any previous issues)
   - Any problems encountered
   - Blocker Type: `none` | `coding` | `library_incompatible` | `architecture_mismatch` | `dependency_missing` | `spec_unclear`
   - Blocker Detail: (if Blocker Type is not `none`) what specifically doesn't work and why
   - Files created or modified (File List)
5. Do not modify any section of the story file above the Dev Agent Record (except the Blocker Resolution section if present).
6. If a "Blocker Resolution" section exists in the story, read it carefully — it contains
   guidance from the user about an alternative approach to use instead of the original spec.
""",
)
```

---

## 6. Completion

After all epics (in scope) have been processed:

1. Update `phase-state.json`: set `execution_status: "complete"`
2. Write the final state back
3. Generate the sprint completion report using the `exec-report` skill (internal). See the `exec-report` skill for the full format.

---

## 7. Known Limitations

- **Parallel story isolation**: Stories executing in parallel within an epic cannot reference each other's Dev Agent Records during execution. Each executor works from the story file as it existed at dispatch time. Cross-epic intelligence works correctly because epics are sequential — by the time Epic 2 starts, all Epic 1 Dev Agent Records are written and available.
- **Re-execution**: Re-running `/sprint-exec` on already-done stories requires explicitly passing `--story=N.M`. The skill will not overwrite `done` stories by default.
- **Blocked stories**: Stories with `status: blocked` are always skipped. To unblock a story, manually update its frontmatter status to `ready-for-dev` and re-run `/sprint-exec --story=N.M`.
