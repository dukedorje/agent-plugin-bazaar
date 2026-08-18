# add-dossier-objects

> **ACTIVE BUILD** → folded and archived 2026-08-17.

**Rigor:** architecture

Depends on: none. Same human-gate as `add-paste-objects` (paste is the
parse face of these objects, not a second object model).

## Why

`working-method` still has exactly seven kinds, and Taskmaster already
calls a Project “that graph with a public address.” Gathering — a
self-description plus citations — has no living name. Without one, the
host will invent a ticket table or a fourth store. Advise sent back a
1:1 promote that did not say what it created. Duke: intentions come
out of a dossier; several may emerge from the compiled assets over
time; keep provenance.

## What

- ADD capability `dossier` (materialized at fold)
- MODIFY `working-method` so the kinds list is honest
- Name emerge + cardinality + provenance (not one-shot consume)
- Values are not work nodes and not ready-set rows
- ADR-007 in `ARCHITECTURE.md` (owed; text is in `design.md`)
- Packet / result stay ADR-001. Dossier is not an agent. Project is
  not a ninth kind

## Impact

- Capabilities: ADDED `dossier` (at fold) · MODIFIED `working-method`
- ADRs: ADR-007 (amend `ARCHITECTURE.md` after advise accept)

## User journey & surfaces

No new UI because the surfaces are `openspec/specs/`, `ARCHITECTURE.md`,
and the in-file banner.

- **Working** — a stranger asks what sits before an intention. They
  find Dossier. They find that several intentions may emerge from it
  over time, each citing the gathering. Project is the named graph of
  an intention. Values are named preferences, not ready rows.
- **Empty** — `openspec/specs/dossier/` does not exist until fold.
  That is correct.
- **Failed** — the first intention consumes the dossier, or an
  emerged intention has no citation back. The delta names that a
  defect.
- **Off** — park this change; the seven kinds stay as they are.

## Out of scope

- Gather / citations / blob store — `add-dossier-gather`, `bazaar-ja7`
- Emerge implementation — `add-dossier-promote` (that id still means
  emerge-with-provenance, not 1:1 consume)
- Host projection and cards — `add-dossier-host`, `nod-dossier-ui`
- Parse grammar, Ratatui, drizzle tables — `add-paste-objects` names
  the face; `add-paste-grammar` / `add-paste-tui` / `add-paste-host` build
- Value Function runtime, scores, or a constraints engine
- Forking packet-in / result-out
- Replacing `/` as the ready-set
- IdentiKey, MetaDev, Tatastu, sprint-plan
