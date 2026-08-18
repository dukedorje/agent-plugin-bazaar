# add-paste-objects

> **ACTIVE BUILD**

**Rigor:** architecture

Depends on: living `dossier` / ADR-007 (folded from
`add-dossier-objects`). This is the parse face of those objects, not
a second kinds ADR.

## Why

Duke wants to paste sectioned text, split it by category, and keep
typed records — a “task” section has a fixed attribute set; cards
show each record; a Ratatui client is the paste door. Without a named
face, that tool becomes a fourth store, a leftover `task` table, or a
third host. Advise sent back a mapping that treated gathering and
intend-dag as independent piles, which would drop ADR-007
provenance. This change names the face, the mixed-paste cite, and
where truth lives. It does not write a parser, a TUI, or a card page.

## What

- ADD parse-face, mixed-paste provenance, and authority requirements
  onto `dossier`
- ADD a taskmaster rule: parsed records and dossiers are not ready-set
  rows
- ADR-008 in `ARCHITECTURE.md` (owed; text is in `design.md`)

## Impact

- Capabilities: MODIFIED `dossier` · MODIFIED `taskmaster`
- ADRs: ADR-008 (amend `ARCHITECTURE.md` after advise accept)

## User journey & surfaces

No new UI because the surfaces are `openspec/specs/` and
`ARCHITECTURE.md`. The paste TUI and cards are later nodes.

- **Working** — someone asks what a paste becomes. They find:
  existing work objects; a mixed paste’s intentions cite the
  dossier; a lone task list does not invent one; bytes via
  `bazaar-ja7`.
- **Empty** — no parser, no Ratatui crate, no card route. Correct.
- **Failed** — a mixed paste drops the cite, a lone task list
  becomes a dossier, a TUI-local DB, a `ready` column, or the
  scaffold `task` table is treated as this face. The delta names
  those defects.
- **Off** — park this change; paste stays unspecified.

## Out of scope

- Parser / fixtures — `add-paste-grammar`
- Host tables and routes — `add-paste-host`
- Ratatui crate — `add-paste-tui` (sibling sketch, no marketplace SHALL)
- Cards — `nod-paste-cards`
- Sitting `bazaar-ja7` (this change only says bytes wait on it)
- Value Functions, emerge implementation — `add-dossier-promote`
- IdentiKey
- Replacing `/` as the ready-set
- Unparking Prime / MetaDev as an agent TUI
