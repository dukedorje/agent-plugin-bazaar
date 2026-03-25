---
name: release
description: Orchestrate project releases — version bumps, release notes, validation, tagging, and CI. Each repo defines its own release process in .release.json.
user-invocable: true
argument-hint: "[patch|minor|major|<version>] [--init] [--dry-run] [--notes-only] [--no-push]"
---

# release: Project Release Orchestrator

Reads a repo-local `.release.json` definition and orchestrates the full release process: version bumping, release notes generation, validation, git tagging, pushing, and GitHub release creation.

Each project defines its own release steps — the skill adapts to any repo structure.

---

## 1. Parse Arguments

| Argument | Behavior |
|----------|----------|
| `patch` / `minor` / `major` | Bump by semver level |
| `<version>` (e.g., `2.0.0`) | Set exact version |
| `--init` | Create or update `.release.json` for this repo |
| `--dry-run` | Show what would happen without making changes |
| `--notes-only` | Generate release notes without executing the release |
| `--no-push` | Run everything locally but don't push or create GitHub release |

If no version argument and not `--init` or `--notes-only`: read the commits since last tag and suggest a semver level.

---

## 2. Init Mode (`--init`)

If `--init` is specified, or `.release.json` does not exist, guide the user through creating one.

### 2a. Scan the Repo

Detect project characteristics:
- **Version files**: Search for version strings in `package.json`, `plugin.json`, `marketplace.json`, `Cargo.toml`, `pyproject.toml`, `setup.py`, `version.go`, `*.gemspec`, etc.
- **Validation scripts**: Look for `validate.sh`, `test` scripts in `package.json`, `Makefile` targets, CI config
- **Changelog**: Check for `CHANGELOG.md`, `CHANGES.md`, `HISTORY.md`
- **CI**: Check for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- **Git tags**: Check existing tag format (`v1.0.0` vs `1.0.0`)

### 2b. Present Findings & Generate Config

Present what was found and generate `.release.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "version_files": [
    {
      "path": "plugins/morphist-tools/.claude-plugin/plugin.json",
      "pattern": "\"version\": \"$VERSION\"",
      "type": "json",
      "key": "version"
    },
    {
      "path": ".claude-plugin/marketplace.json",
      "pattern": "\"version\": \"$VERSION\"",
      "type": "json",
      "key": "plugins[0].version"
    }
  ],
  "tag_prefix": "v",
  "tag_format": "${TAG_PREFIX}${VERSION}",
  "branch": "main",
  "validation": [
    {
      "name": "Plugin validation",
      "command": "./validate.sh",
      "required": true
    }
  ],
  "pre_release": [],
  "post_release": [],
  "release_notes": {
    "style": "grouped",
    "group_by": "type",
    "types": {
      "feat": "Features",
      "fix": "Bug Fixes",
      "refactor": "Refactoring",
      "docs": "Documentation",
      "chore": "Maintenance"
    },
    "include_authors": false,
    "include_pr_links": true,
    "header_template": "## What's Changed\n\n",
    "footer_template": "\n**Full Changelog**: https://github.com/${REPO}/compare/${PREV_TAG}...${TAG}"
  },
  "github_release": {
    "enabled": true,
    "draft": false,
    "prerelease": false,
    "title_template": "${TAG} — ${TITLE}"
  },
  "ci_trigger": null
}
```

Ask the user to review and confirm. Write `.release.json` to the repo root.

### 2c. Schema Reference

| Field | Type | Description |
|-------|------|-------------|
| `version_files` | array | Files containing version strings to bump |
| `version_files[].path` | string | File path relative to repo root |
| `version_files[].type` | string | `json`, `toml`, `yaml`, `text`, `regex` |
| `version_files[].key` | string | JSON/TOML/YAML key path (for structured files) |
| `version_files[].pattern` | string | Regex or literal pattern (for `text`/`regex` type) |
| `tag_prefix` | string | Tag prefix, typically `v` |
| `tag_format` | string | Tag format template |
| `branch` | string | Branch to release from |
| `validation` | array | Commands to run before release (all must pass) |
| `validation[].command` | string | Shell command |
| `validation[].required` | boolean | If true, failure aborts release |
| `pre_release` | array | Commands to run after version bump but before commit |
| `post_release` | array | Commands to run after tag push (e.g., deploy triggers) |
| `release_notes.style` | string | `grouped` (by commit type), `flat` (chronological), `custom` |
| `github_release.enabled` | boolean | Whether to create a GitHub release |
| `github_release.draft` | boolean | Create as draft |
| `ci_trigger` | object/null | CI trigger config (e.g., workflow dispatch) |

---

## 3. Release Execution

If `.release.json` exists and a version argument is provided, execute the release.

### 3a. Pre-flight Checks

1. Read `.release.json`
2. Verify on correct branch: `git branch --show-current` must match `branch` field
3. Verify clean working tree: `git status --porcelain` must be empty
4. Verify no unpushed commits: `git log origin/{branch}..HEAD` should be empty (warn if not)
5. Determine current version from the first `version_files` entry
6. Calculate new version from argument (semver bump or exact)
7. Find previous tag for release notes range

If any pre-flight check fails, report and stop (unless `--dry-run`).

### 3b. Generate Release Notes

1. Get commits since last tag: `git log {prev_tag}..HEAD --oneline --no-merges`
2. Parse commit messages by conventional commit format if `style: "grouped"`:
   - `feat:` → Features
   - `fix:` → Bug Fixes
   - `refactor:` → Refactoring
   - `docs:` → Documentation
   - Other → Maintenance
   - If commits don't follow conventional format, infer type from content
3. For each commit, check for associated PR: `gh pr list --search "{commit_hash}" --json number,title`
4. Build release notes from template

If `--notes-only`: print the generated notes and stop.

### 3c. Version Bump

For each entry in `version_files`:

- **json**: Read file, update key at path, write back (preserve formatting)
- **toml**: Read file, update key, write back
- **yaml**: Read file, update key, write back
- **text/regex**: Find pattern, replace `$VERSION` with new version

If `--dry-run`: show what would change without writing.

### 3d. Run Validation

For each entry in `validation`:
```bash
{command}
```

If any `required: true` validation fails, abort the release and report the error.

### 3e. Run Pre-Release Hooks

For each entry in `pre_release`:
```bash
{command}
```

### 3f. Commit & Tag

```bash
git add {all version_files paths}
git commit -m "Bump to {version}"
git tag {tag_format with version substituted}
```

If `--dry-run`: show commands without executing.

### 3g. Push

If `--no-push`: stop here and report what was done locally.

```bash
git push origin {branch}
git push origin {tag}
```

### 3h. GitHub Release

If `github_release.enabled`:

```bash
gh release create {tag} \
  --title "{title_template with substitutions}" \
  --notes "{generated release notes}" \
  {--draft if draft: true} \
  {--prerelease if prerelease: true}
```

### 3i. Post-Release Hooks

For each entry in `post_release`:
```bash
{command}
```

### 3j. CI Trigger (optional)

If `ci_trigger` is configured:

```json
{
  "ci_trigger": {
    "type": "github_workflow",
    "workflow": "release.yml",
    "inputs": { "version": "$VERSION" }
  }
}
```

Execute: `gh workflow run {workflow} -f version={version}`

---

## 4. Report

Print a release summary:

```
═══════════════════════════════════════════════════
  RELEASE COMPLETE: {tag}
═══════════════════════════════════════════════════

  Version: {prev_version} → {new_version}
  Tag: {tag}
  Branch: {branch}

  Version files updated:
    {list each file}

  Validation: {pass/fail}
  Git: committed, tagged, pushed
  GitHub Release: {url or "skipped"}
  CI: {triggered or "not configured"}

  Release notes:
  {abbreviated release notes}
═══════════════════════════════════════════════════
```

---

## 5. Dry-Run Mode

When `--dry-run` is active, execute every step but:
- Don't write files (show diffs instead)
- Don't commit or tag
- Don't push
- Don't create GitHub release
- Do generate release notes (show them)
- Do run validation (to catch issues early)

Report what WOULD happen at each step.

---

## 6. Notes-Only Mode

When `--notes-only`:
1. Determine version range (last tag to HEAD)
2. Generate release notes
3. Print them
4. Stop (no version bump, no commit, no tag)

Useful for previewing release notes before committing to a release.
