# Contributing

Thanks for your interest in contributing to claude-code-marketplace!

## Submitting a Plugin

### Bundled Plugins (recommended for small plugins)

1. Fork this repo
2. Create your plugin directory under `plugins/your-plugin-name/`
3. Include at minimum:
   - `.claude-plugin/plugin.json` — plugin manifest
   - At least one component (skill, agent, hook, MCP server, or LSP server)
   - `README.md` — usage instructions
4. Add an entry to `.claude-plugin/marketplace.json`
5. Run validation: `claude plugin validate .`
6. Open a PR

### External Plugins (recommended for large or actively developed plugins)

1. Fork this repo
2. Add an entry to `.claude-plugin/marketplace.json` with a GitHub source:
   ```json
   {
     "name": "your-plugin",
     "source": {
       "source": "github",
       "repo": "your-org/your-plugin",
       "ref": "v1.0.0",
       "sha": "full-commit-sha"
     },
     "description": "What it does",
     "version": "1.0.0",
     "category": "category-name",
     "keywords": ["relevant", "tags"],
     "license": "MIT"
   }
   ```
3. Open a PR

## Plugin Requirements

- Must include a valid `.claude-plugin/plugin.json`
- Must have a `README.md` with usage instructions
- Must specify a license
- Must not contain secrets, credentials, or API keys
- Hooks must not exfiltrate data or make unauthorized network requests
- Skills must not contain prompt injection attempts

## Categories

Use one of the existing categories, or propose a new one:

- `git` — Git workflow automation
- `code-quality` — Linting, formatting, review
- `integrations` — External service connections
- `productivity` — Developer workflow tools
- `testing` — Test generation and management
- `documentation` — Doc generation and maintenance
- `security` — Security scanning and hardening
- `examples` — Template and reference plugins

## Versioning

Follow [semantic versioning](https://semver.org/). Bump the version in both your `plugin.json` and the marketplace entry when releasing updates.

## Security

See [SECURITY.md](./SECURITY.md) for our security policy and how to report vulnerabilities.
