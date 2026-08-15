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

Read `openspec/specs/living-specs/spec.md`. Done is fold plus archive, not
"the commit landed."

## Procedure

1. Take `openspec/changes/<id>/` (must be `ACTIVE BUILD`, not PARKED).
2. Apply deltas to `openspec/specs/<capability>/spec.md`:
   - ADDED: append the requirement
   - MODIFIED: replace the whole named requirement with the pasted block
   - REMOVED: delete that requirement
3. Every task checkbox this change owed is checked, or left unchecked with
   a note. Handoffs are bullets.
4. Move the change directory to
   `openspec/changes/archive/YYYY-MM-DD-<id>/`.
5. If the shape of the system changed, **amend** `ARCHITECTURE.md`. Do not
   delete the previous ADR text.
6. Surprises → one line in `docs/LEARNINGS.md`.
7. A `SHALL` left only in the archive is not living truth. Confirm the
   living spec carries it.

Do not fold PENDING or PARKED. Do not leave a fully-checked change in
`openspec/changes/<id>/`.
