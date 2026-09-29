## ADDED Requirements

### Requirement: Hook refreshes copied installs

The harness matrix SHALL document that copied installs follow `main`
through `scripts/sync-harness-plugins.py` and `.githooks`, enabled once
with `--install-hooks`. In-clone Grok / Hermes / Prime still load
`.agents/skills/` directly.

#### Scenario: Operator asks whether plugins auto-update

- GIVEN `plugins/intention/references/harness.md`
- WHEN they read Follow main
- THEN they see the hook, the script, `SYNC_HARNESS_PLUGINS=0`, and
  that version-pinned caches still get new files
