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

## Procedure

1. Search `openspec/specs/` and in-flight `openspec/changes/` (not
   `archive/`). Prefer modifying an existing capability.
2. Verb-led `change-id`. If `intend` already named one, use that id.
3. Scaffold `openspec/changes/<id>/` using the templates. `design.md`
   only when the templates say so.
4. Banner is `> **PENDING**` unless the human already said activate
   (then `> **ACTIVE BUILD**`).
5. Journey section is mandatory: real surfaces, or
   `No new UI because <reason>`.
6. Deltas: `ADDED` / `MODIFIED` / `REMOVED`, each with a `#### Scenario:`.
   MODIFIED pastes the entire living requirement.
7. Checkboxes = owed work. Out-of-scope = bullets.
8. **Stop.** Do not implement unless ACTIVE BUILD (or vibe/brief write
   already granted). Do not fold. Handoff: `act` after activation,
   `fold` after act has landed.

Packets for this change set `capability` (spec directory name) and
`change_id`.
