# Plugin Authoring Guide

## Quick Start

```bash
# Create your plugin directory
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/skills/my-skill

# Create the plugin manifest
cat > plugins/my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What your plugin does",
  "author": { "name": "Your Name" },
  "license": "MIT",
  "skills": "./skills/"
}
EOF

# Create a skill
cat > plugins/my-plugin/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: When Claude should auto-invoke this skill
user-invocable: true
argument-hint: "[arg1] [arg2]"
---

Your skill instructions here. Use $ARGUMENTS for user input.
EOF
```

## Plugin Components

A plugin can include any combination of these:

### Skills (`skills/`)

The primary way to add slash commands. Each skill is a directory containing a `SKILL.md` with YAML frontmatter.

**Frontmatter options:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill name (defaults to directory name) |
| `description` | string | When to auto-invoke (used by Claude for matching) |
| `user-invocable` | bool | Whether users can invoke via `/name` |
| `disable-model-invocation` | bool | If true, only users can trigger it |
| `argument-hint` | string | Shown in autocomplete |
| `allowed-tools` | string | Comma-separated tools Claude can use |
| `model` | string | Model override (haiku, sonnet, opus) |
| `context` | string | `fork` runs in isolated subagent |
| `agent` | string | Agent type (Explore, Plan, etc.) |

### Agents (`agents/`)

Markdown files defining specialized subagent system prompts. Named by filename (e.g., `reviewer.md` becomes the `reviewer` agent).

### Hooks (`hooks/hooks.json`)

Event-driven automation. Available events:

- `SessionStart` / `SessionEnd`
- `UserPromptSubmit`
- `PreToolUse` / `PostToolUse`
- `Stop`, `Notification`, `PreCompact` / `PostCompact`

Hook types: `command` (shell), `prompt` (LLM decision), `agent` (subagent).

### MCP Servers (`.mcp.json`)

External tool servers via the Model Context Protocol. Use `${CLAUDE_PLUGIN_ROOT}` for paths.

### LSP Servers (`.lsp.json`)

Language server connections for code intelligence.

## Path Variables

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin install directory (read-only) |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory (survives updates) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Current skill's directory |

## Testing Your Plugin

```bash
# Validate the marketplace
claude plugin validate .

# Test locally by adding to your project's .claude/settings.local.json:
{
  "plugins": {
    "my-plugin": {
      "source": "/absolute/path/to/plugins/my-plugin",
      "scope": "local"
    }
  }
}

# Reload after changes
/reload-plugins
```

## Publishing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for submission instructions.
