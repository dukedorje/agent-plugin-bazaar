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

Read `openspec/AGENTS.md` and `openspec/specs/living-specs/spec.md`.
Do not invent a second layout.

## Skip

No change directory for: restore intended behavior, typo, formatting,
comment, non-breaking pin, test for already-specced behavior. Edit the
file. Stop.

## Procedure

1. Search `openspec/specs/` and `openspec/changes/` (not `archive/`). Prefer
   modifying an existing capability.
2. Verb-led `change-id` (`add-`, `update-`, `remove-`, `refactor-`).
3. Scaffold:

```
openspec/changes/<id>/
  proposal.md
  tasks.md
  design.md                 # only if cross-cutting
  specs/<capability>/spec.md
```

4. `proposal.md` starts with `> **PENDING**` unless the human already
   activated this id (then `> **ACTIVE BUILD**`). Include
   `## User journey & surfaces` or `No new UI because <reason>` naming
   the real surface.
5. Deltas: `ADDED` / `MODIFIED` / `REMOVED`. Each requirement has at least
   one `#### Scenario:`. MODIFIED pastes the **entire** living requirement.
6. Checkboxes are work this change owes. Out-of-scope is bullets.
7. Do not implement until ACTIVE BUILD (or vibe/brief with write already
   granted). Do not fold. That is `fold`.

Capability id = directory name under `openspec/specs/`. Packets for this
change set `capability` and `change_id`.
