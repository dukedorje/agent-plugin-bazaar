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
/plugin install intention@agent-plugin-bazaar
```

Default verbs: `intend`, `steer`, `change`, `advise`, `act`, `fold`, `brief`, `debrief`, `map`, `ready`, `run`.

How to use them — “run it by me”, current DAG, ready vs beads, `/run --until roll`: [plugins/intention/README.md](plugins/intention/README.md).

## Available Plugins

| Plugin | Description | Category |
|--------|-------------|----------|
| [intention](plugins/intention/) | intend, steer, change, advise, act, fold, brief, debrief, map, ready, run — intention to a running system | productivity |
| [morphist-tools](plugins/morphist-tools/) | PRD, vision, research, beads bridges. `/sprint-plan` is **parked** (revive: explicit multi-week factory) | productivity |
| [metacoding](plugins/metacoding/) | Typed code-graph for blast radius, callers, same-role queries. MCP + skill. Prefer harness LSP for live types. | integrations |

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
