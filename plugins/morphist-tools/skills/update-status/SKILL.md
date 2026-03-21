---
name: update-status
description: Manually update epic or story status in sprint artifacts. Use when automatic status tracking didn't work or to correct statuses after manual intervention.
user-invocable: true
argument-hint: "[--epic=N --status=done] [--story=N.M --status=done] [--show]"
---

# update-status: Manual Epic & Story Status Manager

Manually view and update epic and story statuses in sprint planning artifacts. Use this when automatic status tracking from `/sprint-exec` didn't work correctly, or when you've done manual work outside the normal workflow.

---

## 1. Initialization

### 1a. Locate Sprint Artifacts

Read `.omc/sprint-plan/current/phase-state.json` to confirm an active sprint exists.

If the file does not exist, halt:
```
No sprint found. Run /sprint-plan first to create a sprint.
```

Read `.omc/sprint-plan/current/epics.md` to get the epic list.

### 1b. Parse Arguments

Parse `$ARGUMENTS` for the following flags:

| Flag | Description |
|------|-------------|
| `--show` | Display current status of all epics and stories (default if no other flags) |
| `--epic=N` | Target epic N |
| `--story=N.M` | Target story N.M |
| `--status=VALUE` | New status to set. Valid values below. |
| `--sync` | Recalculate epic statuses from their story statuses |

Valid status values:
- For stories: `ready-for-dev`, `in-progress`, `done`, `failed`, `blocked` (`blocked` is set automatically by sprint-exec when an architectural blocker is detected — `library_incompatible`, `architecture_mismatch`, `dependency_missing` — and can also be set manually for external dependencies)
- For epics: `pending`, `in-progress`, `done`, `partial`, `failed`

If no arguments are provided, default to `--show`.

If `--status` is provided without `--epic` or `--story`, halt:
```
Please specify what to update: --epic=N or --story=N.M
```

---

## 2. Show Mode (`--show`)

Gather status from all sources and display a unified view.

### 2a. Collect Story Statuses

Use Glob to find all story files in `.omc/sprint-plan/current/stories/`.

For each story file, read frontmatter to extract:
- `status` (ready-for-dev, in-progress, done, failed, blocked)
- `started_at` (if present)
- `completed_at` (if present)

### 2b. Collect Epic Statuses

Read `phase-state.json` for the `epic_status` map (may be absent in older sprints).

Also scan `epics.md` for any `Status:` lines under epic headings.

### 2c. Load Decision Graph

Read `.omc/sprint-plan/current/decision-graph.md` if it exists. For each epic, extract the ADRs that affect its stories (any ADR whose story list includes a story in that epic).

### 2d. Display Status Dashboard

```
═══════════════════════════════════════════════════
  SPRINT STATUS DASHBOARD
═══════════════════════════════════════════════════

  Epic 1: {title}
  Status: {epic_status or "not tracked"}
    Story 1.1: {title} — {status}
    Story 1.2: {title} — {status}
    Story 1.3: {title} — {status}
    ADRs: D-003 (ky HTTP client), D-012 (Zod validation)

  Epic 2: {title}
  Status: {epic_status or "not tracked"}
    Story 2.1: {title} — {status}
    Story 2.2: {title} — {status}
    ADRs: D-003 (ky HTTP client), D-007 (Zustand state)

  ─────────────────────────────────────────────────
  Summary:
    Epics:   {done}/{total} done
    Stories: {done}/{total} done, {failed} failed, {blocked} blocked

  phase-state.json execution_status: {value or "not set"}
═══════════════════════════════════════════════════
```

If the decision graph file does not exist, omit the ADRs lines (do not error).

When `--story=N.M` is used with `--show` (or when displaying a single story), render the decision graph for that specific story:

```
Story {N.M}: {title} — {status}
  ADRs:
    D-003: ky for HTTP client
    D-012: Server-side validation with Zod
```

If any epic has stories that are all `done` but the epic itself isn't marked `done`, flag it:
```
  ⚠ Epic {N} has all stories done but epic status is "{current}" — use --sync to fix
```

---

## 3. Update Story Status (`--story=N.M --status=VALUE`)

1. Resolve the story file path: `.omc/sprint-plan/current/stories/{N}-{M}-*.md`
   - Use Glob to find the matching file
   - If no match found, halt: `Story {N.M} not found in current sprint.`
2. Read the story file
3. Update the frontmatter `status` field to the new value
4. If setting to `done`:
   - Add `completed_at: {ISO 8601 timestamp}` if not already present
5. If setting to `in-progress`:
   - Add `started_at: {ISO 8601 timestamp}` if not already present
6. If setting to `ready-for-dev`:
   - Remove `completed_at`, `started_at`, and `validation_failure` if present
7. Write the updated story file
8. Update the `execution_log` in `phase-state.json`:
   - If an entry for this story exists, update its `status`
   - If no entry exists, add one with the current timestamp
9. Display confirmation:
   ```
   Updated Story {N.M}: {title} → {new_status}
   ```
10. After updating the story, recalculate the parent epic's status (same logic as section 5) and update it if changed.

---

## 4. Update Epic Status (`--epic=N --status=VALUE`)

1. Read `phase-state.json`
2. Initialize `epic_status` map if it doesn't exist
3. Set `epic_status["{N}"]` to the new value
4. Write `phase-state.json`
5. Update `epics.md`:
   - Find the `## Epic {N}` heading
   - If a `Status: ` line exists within the next few lines (before the next `###`), update it
   - If no `Status:` line exists, insert `Status: {value}` on the line after the `## Epic {N}` heading
6. Display confirmation:
   ```
   Updated Epic {N}: {title} → {new_status}
   ```

---

## 5. Sync Mode (`--sync`)

Recalculate all epic statuses from their constituent story statuses.

For each epic:
1. Find all stories belonging to that epic
2. Read each story's frontmatter `status`
3. Determine epic status:
   - All stories `done` (or `done` + skipped-as-already-done) → epic = `"done"`
   - Mix of `done` and `failed` → epic = `"partial"`
   - All `failed` → epic = `"failed"`
   - Any `in-progress` → epic = `"in-progress"`
   - All `ready-for-dev` or `blocked` → epic = `"pending"`
4. Update `epic_status` in `phase-state.json`
5. Update `Status:` line in `epics.md`

Also recalculate `execution_status` in `phase-state.json`:
- If all epics are `done`: set to `"complete"`
- If current status is `"halted"` and not all epics are done: preserve `"halted"` (do not downgrade — the halt was intentional and requires replanning before resuming)
- If any epic is `in-progress` or `partial`: set to `"in-progress"`
- Otherwise: leave as-is

Display the results:
```
═══════════════════════════════════════════════════
  STATUS SYNC COMPLETE
═══════════════════════════════════════════════════

  Epic 1: {title} → {status} ({done}/{total} stories done)
  Epic 2: {title} → {status} ({done}/{total} stories done)

  execution_status: {value}

  {count} epic(s) updated.
═══════════════════════════════════════════════════
```

---

## 6. Edge Cases

- **Older sprints without `epic_status`**: The `epic_status` field may not exist in `phase-state.json` for sprints created before this feature. `--sync` and `--show` handle this gracefully by initializing the field.
- **Missing story files**: If a story is referenced in `epics.md` but has no file, report it as `missing` in `--show` and skip it during `--sync`.
- **Manual overrides**: Setting an epic to `done` when stories are still `failed` is allowed (user knows best). Display a warning but proceed:
  ```
  Warning: Epic {N} has {count} failed stories but is being marked done. Proceeding.
  ```
