---
name: debrief
description: >
  Expand a just-finished or failed unit with relevant context,
  takeaways, and what the next intend should extract. Opposite analog
  of brief. Use after an act pass or fail, or when asked to debrief.
user-invocable: true
argument-hint: "<bead-id | change-id | result-path>"
---

# debrief

Opposite analog of `brief`. Brief compresses a unit before work.
Debrief expands a unit after it finished or failed, so a human can
process the learning before the next Orient.

Load `../../references/shared.md` if it exists next to this plugin.
You do not implement. You do not fold. You do not flip a banner.

## Inputs

- A **bead id** — `bd show` (include `--all` if it may be closed).
- A **change-id** — `openspec/changes/<id>/` or its archive.
- A **signed result** — `groups/<id>/result.json` or a review result.

If none is named, ask for one. Do not invent a unit.

## Procedure

1. **Read the unit.** Title, acceptance, comments, close reason,
   signed result (`distilled` first). Do not dump the transcript.
2. **Read the brief residue** if one exists (bead description).
   Note what the brief did not have.
3. **Read `docs/LEARNINGS.md`** only for facts that already touch
   this subsystem. Do not rewrite the file yet.
4. **Write the debrief** in chat (or a bead comment if they named
   a bead). Use the template. Stop. A human processes it.
5. **LEARNINGS.** Offer one dated line per hard-won fact. Append
   only facts that belong there, with a file reference. The debrief
   page is not durable truth.

## Template

```markdown
# debrief <id>

**Unit.** finished | failed
**What happened.** Two or three sentences. What is true now.

## Context
What the brief (or the packet) did not have. Cite files.

## Takeaways
- <thing a human should sit with>
- <thing the next intend should extract>

## Feeds intend
One line the next `/intend --extract-from <id>` should start from.

## LEARNINGS candidates
- YYYY-MM-DD — <one hard-won fact> (`<file>`)
```

## Must not

- Implement leftover work
- Fold, archive, or flip PENDING
- Become a story template or a second LEARNINGS store
- Enter `/run` as a default wave
