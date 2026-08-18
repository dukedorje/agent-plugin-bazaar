# add-paste-tui — sibling client

Reasoning. Ratatui and Rust are not living SHALLs.

## Door

`POST /api/paste` with `{ "text", "save" }`. Same parse as
`bun run paste`. Save uses the existing projection tables.

## Crate

`~/work/Taskmaster/taskmaster-tui`. `TASKMASTER_URL` (default
`http://127.0.0.1:5173`). Piped stdin is the non-interactive
acceptance path. Interactive mode is Ratatui: buffer, preview, save.

## Not

An agent host. A local source of truth. A second grammar.
