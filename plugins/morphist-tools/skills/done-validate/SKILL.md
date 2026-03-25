---
name: done-validate
description: Validate that executor agents actually produced work. Checks file existence, Dev Agent Record completeness, and acceptance criteria coverage.
user-invocable: true
argument-hint: "[--epic=N] [--story=N.M] [--update]"
---

# done-validate: Post-Execution Completion Validation

Verifies that executor agents actually produced work by checking file existence, Dev Agent Record completeness, and acceptance criteria coverage. Updates story frontmatter with validation results.

---

## 1. Parse Arguments

| Flag | Default | Behavior |
|------|---------|----------|
| `--epic=N` | — | Validate all stories in epic N |
| `--story=N.M` | — | Validate a single story |
| `--update` | off | Write validation results back to story frontmatter and execution_log |

If no arguments: validate all stories with `status: in-progress` or `status: done` that lack a `validation_failure` field (i.e., not yet validated).

---

## 2. For Each Story

Read the story file and perform these checks:

### 2a. Dev Agent Record Check

Check if the Dev Agent Record section has been filled in:
- If empty or missing content: note `"Agent completed without filling Dev Agent Record"`

### 2b. File Existence Check

Extract the File List from the Dev Agent Record.

- If the File List is empty, missing, or contains no entries:
  - Check `git status` for any uncommitted changes attributable to this story
  - If still no files found: outcome = `failed`, reason = `"zero files created"`
- If the File List has entries, spot-check that at least one listed file actually exists on disk:
  - If none exist: outcome = `failed`, reason = `"listed files do not exist"`

### 2c. Acceptance Criteria Check

Count the tasks/subtasks in the story. If all checkboxes are unchecked AND no files were modified, this is a false completion:
- outcome = `failed`, reason = `"acceptance criteria unchecked with no file changes"`

### 2d. Blocker Classification

Extract from the Dev Agent Record:
- `Blocker Type` field (default to `"none"`)
- `Blocker Detail` field (if present)

Architectural blockers: `library_incompatible`, `architecture_mismatch`, `dependency_missing`

### 2e. Determine Final Outcome

- If executor reported failure or threw an error: outcome = `failed`
- If any check in 2b-2c failed: outcome = `failed`
- If blocker_type is architectural: outcome = `blocked`
- Otherwise: outcome = `done`

---

## 3. Report Results

For each validated story, print:

```
Story {N.M}: {title}
  Outcome: {done|failed|blocked}
  Files: {count} listed, {count} verified on disk
  Dev Agent Record: {filled|empty}
  {if failed}Validation failure: {reason}{/if}
  {if blocked}Blocker: {blocker_type} — {blocker_detail}{/if}
```

Summary:
```
Validated {N} stories: {done_count} done, {failed_count} failed, {blocked_count} blocked
```

---

## 4. Update (if --update)

If `--update` is specified, write results back:

1. Update story frontmatter:
   - `status: {done|failed|blocked}`
   - `completed_at: {ISO 8601 timestamp}`
   - If validation failed: `validation_failure: {reason}`
   - If blocker: `blocker_type: {value}`, `blocker_detail: {detail}`

2. Append to `execution_log` in `phase-state.json`:
   ```json
   {
     "story": "N.M",
     "status": "done|failed|blocked",
     "started_at": "...",
     "completed_at": "...",
     "validation_failure": null | "{reason}",
     "blocker_type": "none|coding|library_incompatible|architecture_mismatch|dependency_missing|spec_unclear",
     "blocker_detail": null | "{detail}"
   }
   ```

3. Update `stories_completed` count in `phase-state.json`

Each story's status is persisted to disk immediately (not batched).
