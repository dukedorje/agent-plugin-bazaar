# add-paste-grammar

> **ACTIVE BUILD**

**Rigor:** change

Depends on: living `dossier` / ADR-008 (folded `add-paste-objects`).

## Why

ADR-008 names what a paste becomes. Nothing yet turns text into those
records. Without a deterministic grammar, host and TUI invent two
parsers. This change lands one fixture and one command.

## What

- ADD a living requirement: the same paste yields the same records;
  a missing item title fails
- Implement the parser in the Taskmaster sibling app (stack sketch,
  no framework SHALL here)
- One mixed fixture (gathering + intend-dag) and one lone-task
  fixture

## Impact

- Capabilities: MODIFIED `dossier`
- ADRs: none
- Sibling: `~/work/Taskmaster/taskmaster-web` (`src/lib/paste.ts`)

## User journey & surfaces

Duke, from a shell in `taskmaster-web`, or from a test.

- **Working** — pipe a mixed paste; JSON names a dossier and
  intentions that cite it. Pipe a lone task list; JSON has work
  nodes and no dossier.
- **Empty** — blank input fails (no title).
- **Failed** — an item heading is empty; the parse fails.
- **Off** — leave the change parked; paste stays named but unparsed.

`No new UI because` the surface is the fixture command, not `/`.

## Out of scope

- Persist / drizzle tables — `add-paste-host`
- Ratatui — `add-paste-tui`
- Cards — `nod-paste-cards`
- `bazaar-ja7` store choice
- Selecting an existing intention in the kernel tracker (parse may
  mark `select`; it does not write beads)
