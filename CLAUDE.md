# Agent Plugin Bazaar

A marketplace of Claude Code plugins — skills, agents, and MCP integrations.

## Repository Structure

```
.claude-plugin/marketplace.json   # Marketplace registry (versions must match plugin.json)
plugins/
  sprint-plan/                    # Sprint planning workflow plugin
  ultra-research/                 # Multi-agent research swarm plugin
validate.sh                       # Pre-flight validation script
```

## Pre-Push Checklist

Before pushing any update, ALWAYS run:

```bash
./validate.sh
```

This checks:
- plugin.json validity and required fields
- Skill SKILL.md frontmatter (name, description)
- Agent .md frontmatter (name, description)
- Version consistency between plugin.json and marketplace.json

If validation fails, fix all errors before pushing.

## Version Bumping

When making changes to a plugin, bump its version. Default to a **patch** bump unless the change warrants more:

- **Patch** (0.2.1 → 0.2.2): Bug fixes, wording changes, small adjustments
- **Minor** (0.2.2 → 0.3.0): New skills, new agents, significant feature additions
- **Major** (0.3.0 → 1.0.0): Breaking changes to skill interfaces or agent contracts

Update the version in **both** files:
1. `plugins/<name>/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json`

Then run `./validate.sh` to confirm they match.

## Plugin Development

### Testing locally (without publishing)

```bash
claude --plugin-dir ./plugins/ultra-research
```

This loads the plugin from source. The local copy takes precedence over any installed marketplace version. Use `/reload-plugins` inside the session to pick up changes without restarting.

### Creating a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with at least `name` and `version`
2. Add skills in `plugins/<name>/skills/<skill-name>/SKILL.md`
3. Add agents in `plugins/<name>/agents/<agent-name>.md` (auto-discovered)
4. Add the plugin entry to `.claude-plugin/marketplace.json`
5. Run `./validate.sh`

## Plugin Conventions

- Skills use `subagent_type="<plugin-name>:<agent-name>"` to dispatch plugin-defined agents
- Agent .md files use YAML frontmatter with `name`, `description`, `model`, and optional `disallowedTools`
- Skill SKILL.md files use YAML frontmatter with `name`, `description`, and optional `user-invocable`, `argument-hint`, `model`
- OMC agent types (e.g., `oh-my-claudecode:executor`) are acceptable dependencies for plugins designed to run in the OMC ecosystem. Make OMC infrastructure calls (state_write, etc.) graceful — skip if unavailable.
