---
name: change
description: >
  Scaffold or edit an OpenSpec-lite change: proposal, tasks, deltas,
  in-file disposition, journey or "No new UI because". Skip for restore-only
  work. Use when adding or changing behavior, or when asked to open a change
  / write a spec delta.
user-invocable: true
argument-hint: "<change-id or description>"
---

# change

Load `../../references/shared.md` and `../../references/change-templates.md`.
Read `openspec/AGENTS.md` and `openspec/specs/living-specs/spec.md`.
Do not invent a second layout.

## Skip

If `shared.md` says direct fix: edit the file, stop, do not scaffold.

## Frontier preparation

Load `../../references/preparation.md`. When preparing an existing node,
read upstream results and reconcile its contract before activation or act.
A still-valid contract is a valid outcome; do not manufacture delta edits.
Record the preparation note, apply step 4 activation policy to existing
PENDING proposals as well, and return to the conductor. For a new node,
use the procedure below after reconciling the inputs.

## Procedure

1. Search `openspec/specs/` and in-flight `openspec/changes/` (not
   `archive/`). Prefer modifying an existing capability.
2. Verb-led `change-id`. If `intend` already named one, use that id.
3. Scaffold `openspec/changes/<id>/` using the templates. `design.md`
   only when the templates say so.
4. Banner is `> **PENDING**` unless the human already activated this scope
   or recorded campaign authority covers this dependency-ready, prepared
   node (then `> **ACTIVE BUILD**`). Follow preparation.md limits; changed
   commitments require a human decision, not automatic activation.
5. Journey section is mandatory: real surfaces, or
   `No new UI because <reason>`.
6. Deltas: `ADDED` / `MODIFIED` / `REMOVED`, each with a `#### Scenario:`.
   MODIFIED pastes the entire living requirement. On every MODIFIED or
   REMOVED requirement, record the living file you pasted from:

   ```bash
   python3 <this-skill-dir>/../fold/scripts/fold_base.py stamp openspec/changes/<id>
   ```

   The stamp writes `<!-- base: <blob> openspec/specs/<capability>/spec.md -->`
   under the requirement heading. The blob is the living spec file as it
   is now. Do not hand-write a commit you did not just hash.
7. Checkboxes = owed work. Out-of-scope = bullets.
8. **Stale base.** When `run` says `reason: stale-base`, do not fold.
   Re-paste each named requirement from the living spec as it is now,
   then re-apply only this change's own edits on top. Keep clauses that
   exist now and that this change did not mean to remove. Stamp again.
   If this change is architecture or instrument and that rewrite changes
   the contract, add the owed task `Fresh advise after preparation`.
   A change-rigor union that only restores upstream clauses does not.
   Then return to the conductor. The same run folds after the paste matches.
9. **Spike.** Load `../../references/from-sprint-exec.md`. If
   `design.md` cites an unverified hypothesis, add
   `## Unverified hypotheses` with one bullet each (id, claim,
   confidence, verification, synthesis path). Report that spike is an
   option. Do not start it.
10. **Stop.** Do not implement unless ACTIVE BUILD (or vibe/brief write
   already granted). Do not fold. Handoff: `act` after activation,
   `fold` after act has landed. An open spike list is a steer fork
   before that act.

Packets for this change set `capability` (spec directory name) and
`change_id`.
