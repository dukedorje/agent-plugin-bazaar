# Agent Plugin Bazaar

A marketplace of Claude Code plugins — skills, agents, and MCP integrations.

## Repository Structure

```
.claude-plugin/marketplace.json   # Marketplace registry (versions must match plugin.json)
plugins/
  morphist-tools/                 # Consolidated toolkit: sprint planning, PRD, research
    .claude-plugin/plugin.json
    agents/                       # Auto-discovered agent definitions
    skills/                       # All skills (sprint-plan, prd, ultra-research, etc.)
    templates/                    # Shared templates for sprint planning
validate.sh                       # Pre-flight validation script
```

## Pre-Push Checklist

Before pushing to the GitHub remote, ALWAYS:

1. Bump the version intelligently (see below), commit the bump, then push
2. Run `./validate.sh` before the version bump commit
3. Fix all errors before pushing

**Do NOT bump the version on every change or every commit.** Only bump when pushing to the remote.

## Version Bumping

Bump the plugin version **only when pushing to the remote**. Assess all commits being pushed since the last version bump to determine the appropriate bump level:

- **Patch** (1.0.0 → 1.0.1): Bug fixes, wording changes, small adjustments
- **Minor** (1.0.1 → 1.1.0): New skills, new agents, significant feature additions
- **Major** (1.1.0 → 2.0.0): Breaking changes to skill interfaces or agent contracts

Update the version in **both** files:
1. `plugins/morphist-tools/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json`

Then run `./validate.sh` to confirm they match. Commit the version bump separately, then push.

## Validation

```bash
./validate.sh                    # Validate all plugins
./validate.sh morphist-tools     # Validate a specific plugin
```

Checks:
- plugin.json validity and required fields
- Skill SKILL.md frontmatter (name, description)
- Agent .md frontmatter (name, description)
- Version consistency between plugin.json and marketplace.json

## Plugin Development

### Testing locally (without publishing)

```bash
claude --plugin-dir ./plugins/morphist-tools
```

This loads the plugin from source. The local copy takes precedence over any installed marketplace version. Use `/reload-plugins` inside the session to pick up changes without restarting.

### Adding a new skill

1. Create `plugins/morphist-tools/skills/<skill-name>/SKILL.md` with frontmatter
2. If the skill needs custom agents, add them to `plugins/morphist-tools/agents/`
3. Bump version and run `./validate.sh`

## Design Principles

### Progressive Disclosure & Context Efficiency

Skills should be **small, single-purpose, and focused**. Avoid monolithic skill prompts that try to orchestrate everything in one context window. Instead:

- **Thin dispatchers over monoliths**: Orchestration skills should read state, determine what to do next, and delegate to agents — not embed full agent prompts inline. Each agent runs in its own context window.
- **Pass file paths, not file contents**: When dispatching agents, pass the path to read rather than injecting the full content into the prompt. Agents can read files themselves. This saves thousands of tokens from the orchestrator's context.
- **Extract reusable concerns into separate skills**: If a skill contains an inline sub-workflow (verification, blocker triage, review), extract it into its own skill that can be invoked independently. This enables progressive disclosure — users see only the skills they need.
- **Lean on OMC for execution infrastructure**: Don't reimplement parallelism, persistence loops, or verification pipelines. Use OMC's executor agents, ralph/ultrawork for persistence, and team for multi-agent coordination. Morphist-tools' value is in *planning* (sprint-plan, PRD, architecture decisions, story specs), not in being its own execution engine.
- **Default to autonomy**: Elicitation gates should default to `high` severity threshold, not `all`. Most decisions are low-severity and should auto-resolve. Users who want maximum control can opt in with `--stop-at=all`.
- **Context checkpointing**: Long-running skills should checkpoint progress after each major unit of work so that resume is seamless if the context window is exhausted.

### OMC Integration Strategy

Morphist-tools depends on OMC for execution infrastructure. The integration boundary is:

- **Morphist-tools owns**: Sprint planning, PRD generation, story specs, architecture decisions, verification criteria, retrospectives — the *what* and *why*
- **OMC owns**: Agent dispatch, parallelism, persistence loops, model routing, verification execution — the *how*
- **Integration point**: Sprint-exec translates story specs into task definitions that OMC's execution primitives (executor, team, ultrapilot) can process

## Conventions

- Skills dispatch plugin agents via `subagent_type="morphist-tools:<agent-name>"`
- Agent .md files use YAML frontmatter with `name`, `description`, `model`, and optional `disallowedTools`
- Skill SKILL.md files use YAML frontmatter with `name`, `description`, and optional `user-invocable`, `argument-hint`, `model`
- OMC agent types (e.g., `oh-my-claudecode:executor`) are acceptable dependencies. Make OMC infrastructure calls (state_write, etc.) graceful — skip if unavailable.

## Skills Reference

| Skill | Description |
|-------|-------------|
| `sprint-plan` | Multi-phase sprint planning workflow |
| `prd` | Interactive PRD workshop |
| `sprint-exec` | Execute validated sprint stories (thin dispatcher) |
| `done-validate` | Post-execution validation — checks file existence, Dev Agent Record, AC coverage |
| `blocker-triage` | Architectural blocker analysis, downstream impact, resolution options |
| `exec-report` | Epic/sprint progress report generation (internal) |
| `scope` | Sprint scope negotiation — IN/STRETCH/DEFER split, standalone or as Phase 1B |
| `sprint-validate` | Full adversarial validation of sprint artifacts — produces readiness report |
| `refine` | Refine any artifact with consensus, or deep-dive into an epic before execution |
| `retro` | Sprint retrospective generation |
| `ultraresearch` | Multi-agent research swarm |
| `sprint-review` | Review epic implementations against specs and architecture |
| `reconcile` | Cross-story/epic code style reconciliation |
| `review-fix` | Validate and fix issues from reviews and reconciliation |
| `status` | Quick sprint overview: phase, artifacts, statuses (alias for update-status --show) |
| `update-status` | Manually view/update epic and story statuses |
| `replan` | Scoped mid-sprint replanning for broken assumptions |
| `post-mortem` | Incident post-mortem — documents root cause and lessons in story docs for future agents |
| `verify` | Quick independent epic completion check (auto-runs between epics) |
| `audit` | Deep story investigation — gap analysis, fix plans, what's broken and how to fix it (--tdd for test gates) |
| `backlog` | Persistent cross-sprint backlog for follow-ups, tech debt, ideas, and deferred work |
| `log` | Work log annotations with auto-detected sprint/epic/story context |
| `doc` | Create permanent documentation in docs/ from sprint artifacts or topics |
| `help` | Sprint-plan usage guide |
