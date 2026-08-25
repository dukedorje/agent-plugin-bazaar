# add-map-verb

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-24 (chat: let's make map).

## Why

`intend` prints the only page that shows the lay of the land — goal,
orient, every node, ready-set, next. `ready` is the queue. Nothing
reprints that page later with live status and how a node went.

## What

- Add verb **`map`**: observe-only reprint of the intend-dag shape
  plus Status, Wave, and Outcome.
- Optional scope: epic, bead, or change-id. No scope lists open
  epics and their children.
- Residue from beads + banners + last advise + signed
  `distilled.summary` / close reason. No fourth store.
- Not a `/run` wave. Not `debrief` (one unit, deep).
- Capabilities: ADDED on `verbs`. MODIFIED `packaging`,
  `default-loop`, shared-references.

## Impact

- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`
- ADRs: will amend the verb list in `ARCHITECTURE.md` at fold

## User journey & surfaces

Duke, from chat.

1. Says `/map` or `/map bazaar-6os`.
2. **Working** — intend-shaped page with live status and outcomes.
3. **Empty** — no beads and no inflight changes: say so.
4. **Off** — skill missing; `bd show` / `ready` still work.

`No new UI because` the surfaces are `/map` and
`plugins/intention/skills/map/scripts/map.py`.

## Out of scope

- Making map a `/run` wave
- Replacing `ready` or `debrief`
- A second tracker
