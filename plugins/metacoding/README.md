# metacoding

Typed code-graph for agents: callers, neighbors, implementers, FTS over
AST-blind spots, optional CTKR same-role queries. Skill is the decision
layer. MCP is the graph API.

Live types / hover / diagnostics stay on the harness LSP (Grok's `t`
server). This plugin does not try to replace that.

Requires a MetaCoding index. The plugin does not ship ladybugdb; it
launches `serve` via `scripts/serve.sh`.

## Where `serve` runs from

Order:

1. `$METACODING_ROOT` if it is a MetaCoding checkout (`src/cli/bin.ts`)
2. cwd / git-root, if *that* tree is the MetaCoding repo
3. `metacoding` on PATH (`bun add -g @identikey/metacoding` — not `bunx`)

Dev against a clone (this is what you want instead of npm):

```bash
export METACODING_ROOT=/home/dorje/projects/MetaCoding   # your checkout
```

Grok expands `${VAR}` in MCP config. User-level override that *replaces*
the plugin server (fields are not merged):

```toml
# ~/.grok/config.toml
[mcp_servers.metacoding]
command = "bun"
args = ["run", "/home/dorje/projects/MetaCoding/src/cli/bin.ts", "serve"]
```

## Index

```bash
# from a checkout:
bun "$METACODING_ROOT/src/cli/bin.ts" index . --scip
# or published:
metacoding index . --scip
metacoding status
```

`--scip` fills CALLS / REFERENCES / IMPLEMENTS. Re-run or `watch` when
the tree moves.

## Install this plugin

Claude:

```
/plugin marketplace add dukejones/agent-plugin-bazaar
/plugin install metacoding@agent-plugin-bazaar
```

Or from a checkout: `claude --plugin-dir ./plugins/metacoding`.

Grok:

```bash
grok plugin marketplace add dukedorje/agent-plugin-bazaar
grok plugin install metacoding --trust
```

MCP is `scripts/serve.sh` (see above). CTKR tools also need
`METACODING_CTKR_DATA_DIR` pointing at a `.metacoding/` whose `ctkr/`
dir is populated.

## Always-on Grok rule (optional)

Grok will not inject SessionStart stdout into the model. The skill
description is already in the catalog; for a hard habit, copy the rule:

```bash
mkdir -p ~/.grok/rules
cp plugins/metacoding/rules/metacoding.md ~/.grok/rules/metacoding.md
```

(from a bazaar checkout, after install the same file lives next to the
skill.)

## Reach for it

- Before editing an exported symbol: `graph_callers`
- Strings / DI / reflection: `code_search`
- "Anything like this elsewhere?": `ctkr.role_equivalent`
- Grok: `search_tool` → `use_tool metacoding__graph_callers`
- MCP down: `metacoding status` / `metacoding query`

## License

MIT. Graph engine: [WorldTreeNetwork/MetaCoding](https://github.com/WorldTreeNetwork/MetaCoding).
