# Agents

Process memory: [`openspec/AGENTS.md`](openspec/AGENTS.md).
Agent surface: [`docs/contracts/agent-surface.md`](docs/contracts/agent-surface.md).
Verbs: `intend` · `change` · `act` · `fold` · `ready` · `brief` in `.agents/skills/`
(same files as `plugins/intention/skills/`).
Ready-set: `python3 scripts/ready.py` and `bd ready`.
Harness matrix: [`plugins/intention/references/harness.md`](plugins/intention/references/harness.md).

Do **not** write or read `.omc/` for work (Claude or Grok). Tracker is
beads. Intent, briefs, and packets live on beads (or `groups/` for a
group). OMC session files are not project memory.

A group is an agent. Foreign harnesses get a task packet, never a slash
command. Living truth is `openspec/specs/`. In-flight work is
`openspec/changes/` — read the disposition banner.
