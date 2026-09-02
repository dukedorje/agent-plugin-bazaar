# Agents

Process memory: [`openspec/AGENTS.md`](openspec/AGENTS.md).
Agent surface: [`docs/contracts/agent-surface.md`](docs/contracts/agent-surface.md).
Verbs: `intend` · `steer` · `change` · `advise` · `act` · `fold` ·
`brief` · `debrief` · `map` · `status` · `run` · `run-wave` in
`.agents/skills/` (same files as `plugins/intention/skills/`).
How: [`plugins/intention/README.md`](plugins/intention/README.md)
(current DAG, run-it-by-me, status unions OpenSpec + beads).
Board: `python3 scripts/status.py` (OpenSpec **and** `bd ready`).
Harness matrix: [`plugins/intention/references/harness.md`](plugins/intention/references/harness.md).

Do **not** write or read `.omc/` for work (Claude or Grok). Tracker is
beads. Intent, briefs, and packets live on beads (or `groups/` for a
group). OMC session files are not project memory.

A group is an agent. Foreign harnesses get a task packet, never a slash
command. Living truth is `openspec/specs/`. In-flight work is
`openspec/changes/` — read the disposition banner.
