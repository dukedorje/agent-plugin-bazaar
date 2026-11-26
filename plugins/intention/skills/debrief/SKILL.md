---
name: debrief
description: >
  Expand a just-finished or failed unit with relevant context,
  takeaways, and what the next intend should extract. Opposite analog
  of brief. Use after an act pass or fail, or when asked to debrief.
  On an intention root or epic it is the campaign debrief: outcome,
  every decision made on the human's behalf with how to reverse it,
  architecture changes, and learnings written to LEARNINGS.md. Use at
  the end of orchestrate or run, or when asked what was decided.
user-invocable: true
argument-hint: "<bead-id | change-id | result-path | root-id>"
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
- An **intention root or epic** — the campaign debrief below.

If none is named, use this session's pinned intention when its work has
finished; otherwise ask for one. Do not invent a unit.

## One unit

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

## Campaign

The human was not watching the build. They want to know what they now
have, what was decided for them, and what they might want to change.
The decisions are the part they will act on, so those get the care.

1. **Read the record.** The root bead's notes (`START`, `DECISION`,
   `FACT`, grant and bounds). Each child: close reason, latest note,
   `steer.md`, review verdicts and round counts. `git log START..HEAD`.
   Archived changes for what folded. Do not work from memory of the
   chat; a resumed session does not have it, and the record does.
2. **Check each decision against the outcome.** Did what it rested on
   hold? What landed on top of it? That is what makes “to reverse”
   honest: name the nodes that would be redone.
3. **Write learnings.** For each hard-won fact that will still be true
   next month, append one dated line with a file reference to
   `docs/LEARNINGS.md` and commit it. Skip facts fold already recorded
   and facts that only mattered to this campaign. List what you added.
4. **Write the debrief** in chat, from the template. Then stop. If the
   human steers a decision differently, that is `steer` and a re-run of
   the nodes named under “to reverse”, not something debrief does.

Order the decisions by how much the human would want to look: costly
to undo and least certain first. Keep each to the few lines that let
them judge it. Leave out a decision's history; keep its reason.

```markdown
# debrief <root-id> — <the intention, one line>

**Outcome.** done | done with open items | stopped
What is true now that was not before, in a short paragraph. What the
human can go and try (demo commands for open EYES boxes).

## Landed
- <node> — what it does now (`<sha>`)

## Open
- <node> — parked | blocked | by-eye; why; what would move it

## Decisions I made for you (<n>)

### D4 · <node> — <fork, as a question>
**Chose** <choice> over <alternatives>.
**Why.** One or two sentences: the deciding reason.
**Rested on.** The fact or assumption it depends on; whether it held.
**To reverse.** Which nodes are redone and roughly how much work.
**Confidence.** solid | reasonable | worth a second look — and why,
if not solid.

## Architecture changes
What differs from the plan intend and steer set, and why. Cite the ADR
or `ARCHITECTURE.md` amendment.

## What the build taught us
Surprises and insights, including review loops that ran long and what
they were really about.

## Learnings written
- YYYY-MM-DD — <fact> (`<file>`) → `docs/LEARNINGS.md`

## Docs updated
- <path> — what changed. Or: none needed. Or: not checked.

## Feeds intend
What the next intention should start from, and anything deliberately
left out of this one.
```

## Must not

- Implement leftover work
- Fold, archive, or flip PENDING
- Become a story template or a second LEARNINGS store
- Enter `/run` as a default wave
- Re-decide anything in the debrief; report it and let the human steer
