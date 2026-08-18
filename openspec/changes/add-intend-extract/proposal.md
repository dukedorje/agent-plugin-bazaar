# add-intend-extract

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-18 (`/activate` after intend `bazaar-yp8`).

## Why

`intend` starts from a blank page. The usual trail is already in
beads and epics — descriptions, comments, close reasons, signed
results — and the agent still orients as if none of that existed.
`--extract-from` names those items so observe arrives with records
of action and insight into the intent they imply.

## What

- `--extract-from <items>` on intend. Usual items: bead ids and
  epic ids (repeatable).
- Observe those records first, then state insight, then orient and
  split as today.
- No flag keeps blank-page observe (living specs, in-flight,
  LEARNINGS).
- `intend-dag.md` gains an Extract section.
- Capability: MODIFIED `verbs`.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat, on work that already has a trail.

1. Says `/intend --extract-from bazaar-db8` (or several ids).
2. **Working** — observe lists action records from those beads, then
   insight into intent, then the usual Orient / DAG.
3. **Empty** — no flag: today’s blank-page observe.
4. **Failed** — an id is missing or unreadable: say so, do not invent
   the trail, still orient on what did resolve.
5. **Off** — skill has no flag; intend still works as today.

`No new UI because` the surfaces are `/intend` and
`plugins/intention/references/intend-dag.md`.

## Out of scope

- Dossier id as an extract-from item — `add-intend-extract-dossier`
  / `bazaar-yp8.2` (blocked on gather)
- Gather / bytes — `bazaar-db8.3`, `bazaar-ja7`
- Promote wording — `update-dossier-promote` / `bazaar-db8.4`
- Dumping full transcripts into the DAG
