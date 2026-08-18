# add-paste-host

> **ACTIVE BUILD**

**Rigor:** change

Depends on: living `dossier` / ADR-008 and folded `add-paste-grammar`.

## Why

A paste now parses. Nothing yet records the result. Without a host
projection, the next node invents a ticket table or writes `ready`.
This change lets Taskmaster store a paste as a projection and read
it back. `/` stays the ready-set.

## What

- ADD: the host may persist parsed paste records as a projection
- The leftover `task` table is not this landing
- No `ready` column
- Dated export remains the work-graph source
- Citations store refs, not bytes
- Sibling stack: tables + `/paste` (not `/`)

## Impact

- Capabilities: MODIFIED `taskmaster`
- ADRs: none (ADR-008 already named the face)
- Sibling: `~/work/Taskmaster/taskmaster-web`

## User journey & surfaces

Duke, from `/paste` or a POST of the same form.

- **Working** — paste mixed text, submit, see the dossier and the
  intentions that cite it. `/` still only lights startable work nodes.
- **Empty** — parse fail; nothing written.
- **Failed** — records appear on `/` in signal colour, or land in
  `task`, or a `ready` column appears.
- **Off** — park; parse still works, nothing persists.

## Out of scope

- Ratatui — `add-paste-tui`
- Designed cards — `nod-paste-cards` (`/paste` is a ledger, not `/`)
- `bazaar-ja7` blob store
- Making SQLite the work-graph source
- IdentiKey
