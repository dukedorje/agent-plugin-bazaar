---
name: fold
description: >
  Fold an activated change into living specs and archive it. Amend
  ARCHITECTURE.md when shape changed. Append LEARNINGS.md for surprises.
  Use when a change's work has landed and you are asked to fold, archive,
  or finish the change.
user-invocable: true
argument-hint: "<change-id>"
---

# fold

Load `../../references/shared.md` and `../../references/fold-steps.md`.
Done is fold plus archive, not “the commit landed.”

## Procedure

Follow `fold-steps.md` in order. Refuse PENDING and PARKED. Do not
implement leftover tasks — send them back to `act`.

After archive, confirm `openspec/changes/<id>/` no longer exists and
`openspec/specs/<capability>/spec.md` carries every SHALL this change
claimed.

Handoff: report living spec paths and the archive path. If the shape
changed, the ADR amendment is part of the deliverable. Surprises go to
`docs/LEARNINGS.md`, one dated line each.
