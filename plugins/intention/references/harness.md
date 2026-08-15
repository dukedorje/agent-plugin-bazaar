# Harness matrix

H1 reduce. Fan-out members are the five named hosts. This file is the
compatibility matrix. It does not add a second skill tree.

Canonical files: `plugins/intention/skills/<verb>/SKILL.md`.
In this repo, `.agents/skills/<verb>` is a symlink to those directories.

## Matrix

| Host | Loads in this clone? | How | Invoke | Packet-only worker? | Gap |
|---|---|---|---|---|---|
| **Grok** | yes | `.agents/skills/` (native scan). Marketplace: `.grok-plugin/` + `grok plugin install intention --trust` | skill name / `/intend` | When Grok is MetaDev’s `grok-headless-exec`: **yes**, give a packet | Vercel `skills` 1.4.8 has **no** `--agent grok` |
| **Claude** | yes (plugin) | `claude --plugin-dir ./plugins/intention` or marketplace `intention` | `/intend` or skill match | no — it *is* a skill host | `skills add -a claude-code` writes `.claude/skills/` copies; do **not** do that in *this* repo (duplicates the tree) |
| **Codex** | yes | project `.agents/skills/` (same symlinks). Global: `~/.codex/skills/` | `$intend` / `@intention:intend` / skill name — **never** `/intend` | When Codex is a foreign worker from Claude/Grok: **yes**, packet | No slash API |
| **Hermes** | yes if it scans `.agents/skills/` (common); else global `~/.hermes/skills/` | symlink or copy the five dirs into `~/.hermes/skills/` | skill name | When spawned as a worker: packet | Vercel `skills` 1.4.8 has **no** `--agent hermes-agent` |
| **Prime** | yes via `.agents/skills/` | Prime/Pi also reads `~/.pi/agent/skills/` and may read `~/.prime/agent/skills/` | skill name | When spawned as a worker: packet | Not a `skills` CLI `--agent`. `pi` is the closest flag (`~/.pi/agent/skills/`) |

Foreign worker rule (every row): if the host is *assigned work by another conductor*, it receives a task packet. It never receives a Claude slash command.

## Install elsewhere (other repos)

Prefer the Vercel `skills` CLI as the fan-out installer. Point it at the
plugin directory so it does not also vacuum morphist-tools:

```bash
skills add /path/to/agent-plugin-bazaar/plugins/intention \
  --skill intend --skill change --skill act --skill fold --skill brief \
  --agent claude-code --agent codex \
  -y
```

`--agent codex` installs into **project** `.agents/skills/`. Grok, Codex,
and Prime in that repo will see them. Claude still wants `-a claude-code`
(`.claude/skills/`) or a marketplace install.

Do **not** use `--all` on the bazaar repo root: it will offer sprint-plan
and every other skill.

GitHub, once you are installing from the network:

```bash
skills add dukedorje/agent-plugin-bazaar --full-depth \
  --skill intend --skill change --skill act --skill fold --skill brief \
  --agent claude-code --agent codex \
  -y
```

`--full-depth` is required if discovery stops before `plugins/intention/skills/`.

## What we do not do in this repo

- Run `skills add` here. It would copy into `.claude/skills/` and fight
  ADR-003’s single tree.
- Add Grok/Hermes to the `skills` CLI. That is upstream (vercel-labs/skills).
- Invent Codex slash commands.

## Check

```bash
skills add ./plugins/intention --list
# → act, brief, change, fold, intend
```
