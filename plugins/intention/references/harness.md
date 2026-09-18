# Harness matrix

H1 reduce. Fan-out members are the five named hosts. This file is the
compatibility matrix. It does not add a second skill tree.

Canonical files: `plugins/intention/skills/<verb>/SKILL.md`.
In this repo, `.agents/skills/<verb>` is a symlink to those directories.

## Matrix

| Host | Loads in this clone? | How | Invoke | Packet-only worker? | Gap |
|---|---|---|---|---|---|
| **Grok** | yes | `.agents/skills/` (native scan). Marketplace: `.grok-plugin/` + `grok plugin install intention --trust` | skill name / `/intend` / `/run-wave`. Conductor uses `spawn_subagent` / `workflow` (`run-wave`) for Grok-shaped work; `spawn.py` for Claude/Sol | When Grok is MetaDev’s `grok-headless-exec`: **yes**, give a packet | `skills` 1.5.22 `--agent grok` writes `.grok/skills/` (also scanned; higher priority than `.agents/`). Do not run that *in this repo* |
| **Claude** | yes (plugin) | `claude --plugin-dir ./plugins/intention` or marketplace `intention` | `/intend` or skill match | no — it *is* a skill host | `skills add -a claude-code` writes `.claude/skills/` copies; do **not** do that in *this* repo |
| **Codex** | yes | project `.agents/skills/` symlinks in this clone; elsewhere install `intention@agent-plugin-bazaar` so the complete bundle is retained | `$intend` / `@intention:intend` / skill name — **never** `/intend` | When Codex is a foreign worker from Claude/Grok: **yes**, packet | Start a new thread after plugin install/update |
| **Hermes** | yes if it scans `.agents/skills/`; else `.hermes/skills/` | `skills` 1.5.22 `--agent hermes-agent` → `.hermes/skills/` / `~/.hermes/skills/` | skill name | When spawned as a worker: packet | none for install |
| **Prime** | yes via `.agents/skills/` | closest CLI flag is `--agent pi` (`.pi/skills/`, `~/.pi/agent/skills/`) | skill name | When spawned as a worker: packet | still no `--agent prime` |

Foreign worker rule (every row): if the host is *assigned work by another conductor*, it receives a task packet. It never receives a Claude slash command.

## Install elsewhere (other repos)

Codex uses the marketplace bundle because Intention skills depend on sibling
references, scripts, workflows, and agents:

```bash
codex plugin marketplace add /path/to/agent-plugin-bazaar
codex plugin add intention@agent-plugin-bazaar
```

Do not install Intention into Codex with `skills add -g`: that copies the
skill directories without their sibling runtime files and can shadow the
complete plugin. Claude and Grok should use their native plugin installers.
Hermes and Prime should load the checkout's `.agents/skills/` symlinks until
they have a bundle-aware installer.

## What we do not do in this repo

- Run `skills add` here. It would copy into `.claude/skills/` and fight
  ADR-003’s single tree.
- Invent Codex slash commands.

## Check

```bash
skills add ./plugins/intention --list
# → act, brief, change, fold, intend
```
