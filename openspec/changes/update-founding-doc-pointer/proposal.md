# update-founding-doc-pointer

> **ACTIVE BUILD**

Depends on: `add-working-loop`, `add-working-objects`,
`add-working-split` folded.

## Why

Once the method has living specs, the founding novel must stop being
the source. It said it would be split. This change is that cut.

## What

Rewrite `docs/from-intention-to-running.md` as a short pointer to
`working-method` (and the already-folded capabilities). Keep a trail
of the first DAG. Do not delete history — amend.

## Impact

- Capabilities: none (doc is reasoning; names change-ids)
- ADRs: none
- Files: `docs/from-intention-to-running.md`

## User journey & surfaces

No new UI because the surface is the founding doc. Working: a stranger
reads one page and is sent to living specs. Empty: the 600-line novel
remains. Failed: the pointer still contains SHALLs. Off: leave PENDING
until the three children fold.

## Out of scope

- Folding the three children (do those first)
- Site explainers / interactive pieces beyond the pointer
