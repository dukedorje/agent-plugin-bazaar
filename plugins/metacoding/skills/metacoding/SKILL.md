---
name: metacoding
description: >-
  Reach for the MetaCoding typed graph instead of grep when editing a symbol,
  sizing blast radius, tracing callers/implementers/neighbors, hunting
  strings/DI/reflection, or asking "what plays the same role." Use during
  ordinary coding, review, and thinking partnership — not only when the user
  says "graph." Triggers: edit, blast radius, who calls, implementers,
  neighbors, code_search, same role, role-equivalent, ctkr, DI, reflection,
  structural, metacoding. Live types/hover/diagnostics stay on the harness
  LSP (Grok: t server). Empty graph_callers usually means no SCIP index.
user-invocable: true
argument-hint: "[symbol or question]"
license: MIT
metadata:
  homepage: https://github.com/WorldTreeNetwork/MetaCoding
  package: "@identikey/metacoding"
---

# MetaCoding graph

Read-only typed graph + FTS (+ optional CTKR). Not a language server.

Live types, hover, go-to-def, find-refs, diagnostics: harness LSP.
Grok: `t__lsp_hover` / `t__lsp_find_references` / `t__ast_grep_search`.
Do not prefer MetaCoding `lsp_*` in Grok.

## Call the tools

Claude: MCP tools are first-class (`graph_callers`, `graph_neighbors`, …).
Grok: two-hop — `search_tool` query `metacoding graph_callers`, then
`use_tool` name `metacoding__graph_callers` (server `metacoding`, tool
`graph_callers`). Same pattern for every tool below.

Unsure of the live surface: `describe_api`.

MCP down: `metacoding status` then `metacoding query '<cypher>'`.
Index once per repo: `metacoding index . --scip` (SCIP is what fills
CALLS / REFERENCES / IMPLEMENTS). Global install: `bun add -g @identikey/metacoding`
(`bunx` will not work).

## Route

| Need | Tool |
|---|---|
| What touches this / what this touches | `graph_neighbors` (`direction` in/out/both, `edge_kinds`) |
| Who depends on this | `graph_callers` (needs SCIP) |
| What implements / extends this | `graph_implementers` |
| Strings, DI keys, routes, reflection, comments | `code_search` (FTS5: phrase, `x*`, `NEAR`) |
| Snapshot diff | `graph_diff` (needs `--per-commit-identity`) |
| No typed tool fits | `graph_cypher` — last resort |
| Same structural role (raw typed-edge shape) | `ctkr.role_equivalent` |
| Learned structural neighbors | `ctkr.nearest_symbols` |
| Recurring typed subgraphs | `ctkr.motif_search` |
| Labeled patterns | `ctkr.pattern_search` |

`role_equivalent` vs `nearest_symbols`: hom-profile counts vs learned
embeddings. Cross-repo role: `cross_repo_only: true`. Disambiguate
`qualified_name` with `scope: "<repo>"`.

Compose: `code_search` a string → `graph_callers` up the stack →
`graph_neighbors` for the typed neighborhood.

## Gotchas

- Empty `graph_callers`: Tree-sitter-only index. Re-index `--scip`, or
  fall back to harness find-refs (live buffer, not the graph).
- `graph_diff` empty for an old sha: that snapshot was never indexed.
- `ctkr.*` data-dir errors: set `METACODING_CTKR_DATA_DIR` to a
  `.metacoding/` that has a populated `ctkr/` dir. No implicit fallback.
- `graph_*` accept symbol id (16-char hash) or `qualified_name`.
- Always-on Grok habit file: copy `rules/metacoding.md` to
  `~/.grok/rules/metacoding.md`.

Docs: [mcp-surface](https://github.com/WorldTreeNetwork/MetaCoding/blob/main/docs/design/mcp-surface.md),
[ctkr](https://github.com/WorldTreeNetwork/MetaCoding/blob/main/docs/design/ctkr.md).
