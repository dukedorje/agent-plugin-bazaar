# add-dossier-objects

> **ACTIVE BUILD**

**Rigor:** architecture

Depends on: none. Same human-gate as `add-paste-objects` (paste is the
parse face of these objects, not a second object model).

## Why

`working-method` still has exactly seven kinds, and Taskmaster already
calls a Project “that graph with a public address.” Gathering — a
self-description plus citations, before an intention has much identity —
has no living name. Without one, the host will invent a ticket table or
a fourth store. This change names Dossier, says what a Project is, and
says what Values are, so later gather / promote / paste nodes do not
invent them in act.

## What

- ADD capability `dossier` (materialized at fold)
- MODIFY `working-method` so the kinds list is honest
- ADR-007 in `ARCHITECTURE.md` (owed; text is in `design.md`)
- Packet / result stay ADR-001. Dossier is not an agent. Project is
  not a ninth kind. Values are named preferences on a project split,
  not a function runtime

## Impact

- Capabilities: ADDED `dossier` (at fold) · MODIFIED `working-method`
- ADRs: ADR-007 (amend `ARCHITECTURE.md` after advise accept)

## User journey & surfaces

No new UI because the surfaces are `openspec/specs/`, `ARCHITECTURE.md`,
and the in-file banner.

- **Working** — a stranger asks what sits before an intention. They
  find Dossier in a living spec or accepted ADR, then Project as the
  named graph, then Values as named preferences.
- **Empty** — `openspec/specs/dossier/` does not exist until fold.
  That is correct.
- **Failed** — someone treats the leftover Taskmaster `task` table, or
  a pasted blob store, as the dossier. The delta names that a defect.
- **Off** — park this change; the seven kinds stay as they are.

## Out of scope

- Gather / citations / blob store — `add-dossier-gather`, `bazaar-ja7`
- Promote implementation — `add-dossier-promote`
- Host projection and cards — `add-dossier-host`, `nod-dossier-ui`
- Parse grammar, Ratatui, drizzle tables — `add-paste-objects` names
  the face; `add-paste-grammar` / `add-paste-tui` / `add-paste-host` build
- Value Function runtime, scores, or a constraints engine
- Forking packet-in / result-out
- Replacing `/` as the ready-set
- IdentiKey, MetaDev, Tatastu, sprint-plan
