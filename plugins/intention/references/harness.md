# Harness matrix

H1 reduce. Fan-out members are the five named hosts. This file is the
compatibility matrix. It does not add a second skill tree.

Canonical files: `plugins/intention/skills/<verb>/SKILL.md`.
In this repo, `.agents/skills/<verb>` is a symlink to those directories.

## Matrix

| Host | Loads in this clone? | How | Invoke | Packet-only worker? | Gap |
|---|---|---|---|---|---|
| **Grok** | yes | `.agents/skills/` (native scan). Marketplace: `.grok-plugin/` + `grok plugin install intention --trust` | skill name / `/intend`. Conductor uses `spawn_subagent` / `workflow` (`run-wave`) for Grok-shaped work; `spawn.py` for Claude/Sol | When Grok is MetaDev’s `grok-headless-exec`: **yes**, give a packet | `skills` 1.5.22 `--agent grok` writes `.grok/skills/` (also scanned; higher priority than `.agents/`). Do not run that *in this repo* |
| **Claude** | yes (plugin) | `claude --plugin-dir ./plugins/intention` or marketplace `intention` | `/intend` or skill match | no — it *is* a skill host | `skills add -a claude-code` writes `.claude/skills/` copies; do **not** do that in *this* repo |
| **Codex** | yes | project `.agents/skills/` (same symlinks). Global: `~/.codex/skills/` | `$intend` / `@intention:intend` / skill name — **never** `/intend` | When Codex is a foreign worker from Claude/Grok: **yes**, packet | No slash API |
| **Hermes** | yes if it scans `.agents/skills/`; else `.hermes/skills/` | `skills` 1.5.22 `--agent hermes-agent` → `.hermes/skills/` / `~/.hermes/skills/` | skill name | When spawned as a worker: packet | none for install |
| **Prime** | yes via `.agents/skills/` | closest CLI flag is `--agent pi` (`.pi/skills/`, `~/.pi/agent/skills/`) | skill name | When spawned as a worker: packet | still no `--agent prime` |

Foreign worker rule (every row): if the host is *assigned work by another conductor*, it receives a task packet. It never receives a Claude slash command.

## Install elsewhere (other repos)

Prefer the Vercel `skills` CLI as the fan-out installer. Point it at the
plugin directory so it does not also vacuum morphist-tools:

```bash
skills add /path/to/agent-plugin-bazaar/plugins/intention \
  --skill intend --skill steer --skill change --skill advise --skill act --skill fold --skill brief --skill debrief --skill map --skill ready --skill run \
  --agent claude-code --agent codex --agent grok --agent hermes-agent \
  -y
```

`--agent codex` still fills project `.agents/skills/` (Codex + anyone else
that scans that tree). `--agent grok` / `--agent hermes-agent` fill those
hosts’ own dirs. Claude still wants `-a claude-code`. Prime: `--agent pi`
or rely on `.agents/skills/`.

Do **not** use `--all` on the bazaar repo root: it will offer sprint-plan
and every other skill.

GitHub, once you are installing from the network:

```bash
skills add dukedorje/agent-plugin-bazaar --full-depth \
  --skill intend --skill steer --skill change --skill advise --skill act --skill fold --skill brief --skill debrief --skill map --skill ready --skill run \
  --agent claude-code --agent codex --agent grok --agent hermes-agent \
  -y
```

`--full-depth` is required if discovery stops before `plugins/intention/skills/`.

## What we do not do in this repo

- Run `skills add` here. It would copy into `.claude/skills/` and fight
  ADR-003’s single tree.
- Invent Codex slash commands.

## Check

```bash
skills add ./plugins/intention --list
# → act, brief, change, fold, intend
```
