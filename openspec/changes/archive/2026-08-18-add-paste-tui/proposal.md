# add-paste-tui

> **ACTIVE BUILD**

**Rigor:** change

Depends on: living paste face (ADR-008), grammar, and host projection.

## Why

Parse and `/paste` exist. Duke’s first ask was a CLI you can paste
into. `bun run paste` only prints JSON. A sibling Ratatui client
should show the parse and confirm a write to the host. It is not a
third host and not a TUI-local database.

## What

- ADD: a sibling TUI may submit text to the host and show records
- JSON door on the Taskmaster host (`POST /api/paste`)
- Crate `~/work/Taskmaster/taskmaster-tui` (stack sketch, no
  marketplace SHALL for Rust or Ratatui)

## Impact

- Capabilities: MODIFIED `dossier`
- ADRs: none
- Sibling crate + host API

## User journey & surfaces

Duke, from a terminal.

- **Working** — `pbpaste | taskmaster-tui --save` prints the
  intention and nod-* records and a paste id. Interactive: edit,
  see parse, ctrl-s writes.
- **Empty** — bad paste; TUI shows the parse error; nothing saved.
- **Failed** — TUI stores its own SQLite, or is named an agent host.
- **Off** — park; `bun run paste` and `/paste` still work.

## Out of scope

- Replacing `/` or `/paste`
- A fourth store
- Unparking Prime / MetaDev
- Framework SHALLs in this marketplace
