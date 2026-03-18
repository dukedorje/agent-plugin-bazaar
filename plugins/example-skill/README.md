# example-skill

A template plugin demonstrating the Claude Code plugin format.

## Components

| Component | Path | Description |
|-----------|------|-------------|
| Skill | `skills/hello/SKILL.md` | A simple greeting skill |
| Agent | `agents/example-agent.md` | An example subagent definition |
| Hook | `hooks/hooks.json` | SessionStart hook that logs a message |

## Usage

After installing the marketplace:

```
/example-skill:hello World
```

## Creating Your Own Plugin

Copy this directory as a starting point. See the [Plugin Authoring Guide](../../docs/authoring.md) for details.
