# add-paste-objects

> **ACTIVE BUILD**

**Rigor:** architecture

Depends on: `add-dossier-objects`. Same human-gate. This is the parse
face of those objects, not a second kinds ADR.

## Why

Duke wants to paste sectioned text, split it by category, and keep
typed records — a “task” section has a fixed attribute set; cards
show each record; a Ratatui client is the paste door. Without a named
face, that tool becomes a fourth store, a leftover `task` table, or a
third host. This change names the face and where truth lives. It does
not write a parser, a TUI, or a card page.

## What

- ADD parse-face and authority requirements onto `dossier`
- ADD a taskmaster rule: parsed records and dossiers are not ready-set
  rows
- ADR-008 in `ARCHITECTURE.md` (owed; text is in `design.md`)

## Impact

- Capabilities: MODIFIED `dossier` (ADDing while the parent is
  in-flight) · MODIFIED `taskmaster`
- ADRs: ADR-008 (amend `ARCHITECTURE.md` after advise accept)

## User journey & surfaces

No new UI because the surfaces are `openspec/specs/` and
`ARCHITECTURE.md`. The paste TUI and cards are later nodes.

- **Working** — someone asks what a paste becomes. They find: existing
  work objects, attributes with the object, bytes via `bazaar-ja7`.
- **Empty** — no parser, no Ratatui crate, no card route. Correct.
- **Failed** — a TUI-local DB, a `ready` column, or the scaffold
  `task` table is treated as this face. The delta names that a defect.
- **Off** — park this change; paste stays unspecified.

## Out of scope

- Parser / fixtures — `add-paste-grammar`
- Host tables and routes — `add-paste-host`
- Ratatui crate — `add-paste-tui` (sibling sketch, no marketplace SHALL)
- Cards — `nod-paste-cards`
- Sitting `bazaar-ja7` (this change only says bytes wait on it)
- Value Functions, promotion implementation, IdentiKey
- Replacing `/` as the ready-set
- Unparking Prime / MetaDev as an agent TUI
