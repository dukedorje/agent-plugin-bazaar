# update-plugin-follow-main

> **ACTIVE BUILD**

## Why

Claude, Grok, and Codex cache plugins by version or git SHA. `autoUpdate`
and `ref = main` do not recopy `intention/0.5.0` when files change on
`main`. Harnesses on this machine kept shipping last week's verbs.

## What

- Mirror `plugins/<name>` into harness caches after a `main` commit,
  merge, or checkout (`scripts/sync-harness-plugins.py`, `.githooks`).
- Align `.grok-plugin/marketplace.json` versions with plugin.json
  (intention was stuck at 0.4.0). List morphist-tools on the Grok index.
- `validate.sh` checks the Grok index.

## Impact

- Capabilities: MODIFIED packaging, MODIFIED harness
- ADRs: none

## User journey & surfaces

No new UI because the surface is already the harness plugin load.
After `git pull` / commit on `main`, Grok, Claude, and Codex load this
clone's current `plugins/` without a manual `plugin update`.

## Out of scope

- Bumping plugin versions on every commit (the hook recopies the same
  version directory).
- Hermes / Prime global `skills add` copies (they should scan this
  clone's `.agents/skills/`).
- Remote machines that never pull this clone (they still need their own
  hook or a session-start marketplace pull plus version bump).
