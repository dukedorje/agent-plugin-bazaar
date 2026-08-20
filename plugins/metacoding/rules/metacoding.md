# MetaCoding graph

Typed graph for structure and blast radius. Live types, hover, diagnostics: harness LSP (Grok: `t` server), not MetaCoding `lsp_*`.

- Before editing an exported symbol: `graph_callers`.
- Strings / DI / routes / reflection: `code_search`, not grep.
- "Anything like this elsewhere?": `ctkr.role_equivalent`.
- Empty callers usually means the repo was indexed without `--scip`, not that nothing calls it.

Grok: `search_tool` query `metacoding graph_callers`, then `use_tool` `metacoding__graph_callers`.
If MCP is down: `metacoding status`, then `metacoding query`.
Serve: `$METACODING_ROOT` checkout, else PATH `metacoding` (not bunx).
