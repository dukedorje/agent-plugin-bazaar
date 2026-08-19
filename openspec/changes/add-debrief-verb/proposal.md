# add-debrief-verb

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-19 (`/activate all` — only this landing needed it).

## Why

Brief compresses a unit before work. After a finish or a fail,
nothing expands the trail so a human can process takeaways before
the next Orient. Fold archives specs. LEARNINGS takes one dated
line. Neither is the opposite analog of brief.

## What

- Add verb **`debrief`**: expand a just-finished or failed unit
  (bead, change-id, or signed result).
- Output: what happened, context the brief did not have,
  takeaways, what the next intend should extract.
- Stop so a human can process. Do not implement. Do not fold.
- Durable residue is LEARNINGS (one line per hard-won fact) and
  the graph, not the debrief page.
- Not a default `/run` wave (brief is not one).
- Capabilities: ADDED on `verbs`. MODIFIED `packaging`,
  `default-loop`, shared-references list on `verbs`.

## Impact

- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`
- ADRs: will amend `ARCHITECTURE.md` (verb list) when this folds

## User journey & surfaces

Duke, from chat, after an act pass or fail.

1. Says `/debrief bazaar-6os.1` (or a result path).
2. **Working (finished)** — expansion of what landed, takeaways,
   what intend should extract next. Stops.
3. **Working (failed)** — same shape from the miss: what was
   tried, what broke, what to extract.
4. **Empty** — no unit named: ask for a bead, change-id, or
   result.
5. **Off** — skill missing; fold and LEARNINGS still work.

`No new UI because` the surfaces are `/debrief` and chat (or a
bead note).

## Out of scope

- Default `/run` wave — later, if ever
- Replacing LEARNINGS or fold
- Morphist retro / post-mortem
- Dossier extract-from (`bazaar-yp8.2`)
