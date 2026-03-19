# agent-plugin-bazaar

A curated marketplace of Claude Code plugins — skills, agents, hooks, and MCP integrations.

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add dukejones/agent-plugin-bazaar
```

Then browse and install plugins:

```
/plugin
```

Or install directly:

```
/plugin install sprint-plan@agent-plugin-bazaar
```

## Available Plugins

| Plugin | Description | Category |
|--------|-------------|----------|
| [sprint-plan](plugins/sprint-plan/) | Multi-phase sprint planning workflow with Decision Steering and RALPLAN-DR consensus | productivity |

## Creating a Plugin

See the [Plugin Authoring Guide](docs/authoring.md) for a full walkthrough.

Quick version:

1. Create `plugins/your-plugin/.claude-plugin/plugin.json`
2. Add your components (skills, agents, hooks, MCP servers)
3. Add a `README.md`
4. Register in `.claude-plugin/marketplace.json`
5. Open a PR

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting plugins.

## Security

See [SECURITY.md](SECURITY.md) for our security policy.

## License

MIT
