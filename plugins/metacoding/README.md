# metacoding

Typed code-graph for agents: callers, neighbors, implementers, FTS over
AST-blind spots, optional CTKR same-role queries. Skill is the decision
layer. MCP is the graph API.

Live types / hover / diagnostics stay on the harness LSP (Grok's `t`
server). This plugin does not try to replace that.

Requires a running MetaCoding index. The plugin does not ship the
ladybugdb native binary — install the CLI separately.

## Install the CLI + index

```bash
bun add -g @identikey/metacoding
# bunx is not supported (skips native binary install)

export PATH="$HOME/.bun/bin:$HOME/.cache/.bun/bin:$PATH"
metacoding index . --scip     # CALLS/REFERENCES/IMPLEMENTS need SCIP
metacoding status
```

`--scip` indexers ship bundled. Re-run (or `metacoding watch .`) when
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

MCP command is `metacoding serve` (must be on PATH). CTKR tools also
need `METACODING_CTKR_DATA_DIR` pointing at a `.metacoding/` whose
`ctkr/` dir is populated.

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
