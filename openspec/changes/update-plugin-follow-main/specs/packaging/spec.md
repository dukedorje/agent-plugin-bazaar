## ADDED Requirements

### Requirement: Installed copies follow main

When this repository's `main` branch is updated in a clone, a git hook
SHALL run `scripts/sync-harness-plugins.py` and mirror `plugins/<name>`
into installed Claude, Grok, and Codex plugin caches under the user's
home directory. Missing harnesses SHALL be skipped, not failed. Version
directories that already exist SHALL receive the new files even when the
plugin version string did not change. `.claude-plugin/marketplace.json`
and `.grok-plugin/marketplace.json` SHALL list the same version as each
plugin's `plugin.json`. `SYNC_HARNESS_PLUGINS=0` SHALL disable the hook.
In-clone `.agents/skills/` symlinks remain the live tree and do not need
a copy.

#### Scenario: Commit on main refreshes a version-pinned Claude cache

- GIVEN `~/.claude/plugins/cache/agent-plugin-bazaar/intention/0.5.0`
  with stale files and plugin.json still `0.5.0`
- WHEN `main` is committed or merged in this clone with hooks enabled
- THEN that cache directory contains the clone's current
  `plugins/intention` files and `.in_use` is left in place

#### Scenario: Grok marketplace version matches the plugin

- GIVEN `plugins/intention/.claude-plugin/plugin.json` version `0.5.0`
- WHEN `validate.sh` runs
- THEN `.grok-plugin/marketplace.json` lists `intention` at `0.5.0`
