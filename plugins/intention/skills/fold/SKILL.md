---
name: fold
description: >
  Fold an activated change into living specs and archive it. Amend
  ARCHITECTURE.md when shape changed. Append LEARNINGS.md for surprises.
  Use when a change's work has landed and you are asked to fold, archive,
  or finish the change. May run in the background on the designated
  folder (latest Opus), like advise.
user-invocable: true
argument-hint: "<change-id>"
---

# fold

Load `../../references/shared.md` and `../../references/fold-steps.md`.
Done is fold plus archive, not “the commit landed.”

This is the last hole in the loop, parallel to `advise` (a designated
agent, packet, background ok):

```
intend → steer → change → advise → act → fold
```

## Skip

PENDING or PARKED → stop. Do not fold. Do not implement leftover
tasks — send them back to `act`. Branch name is not a skip.
Fold on current HEAD by default. A branch transition is allowed when the user
requests it, the task explicitly targets one, or the workflow requires a known
transition. Resolve the exact target and protect dirty worktree changes first;
never invent a branch merely to fold. Before persisting, check whether the
current branch backs an open PR. Do not add an unrelated fold commit to that PR
branch; move to the task's appropriate branch first.

## Procedure

1. **Target.** Change-id from the user, the run card `focus`, or
   `change_id` on a packet. Open `openspec/changes/<id>/` (not
   `archive/`).
2. **Load.** `proposal.md` banner, `tasks.md`, `specs/**/spec.md`,
   living `openspec/specs/` for those capabilities.
3. **Assign.** `python3 plugins/intention/scripts/ladder.py assign --shape fold`
   (folder). Default is latest Opus (`opus-fold`). Human pick always
   wins — Grok is allowed. Same session may fold inline only when it
   *is* that route.
4. **Packet.** Folder receives `permission: write` on the living-spec
   and archive paths. Foreign harnesses get a packet file, never a
   slash command. Conductor may **spawn in the background** and keep
   the tab moving (`spawn.py stage` then `spawn.py run --adapter claude`
   when the route is Claude). Do not inline fold on a Grok tab unless
   the human picked Grok.
5. **Apply** `fold-steps.md` in order.
6. **Signed result** (`permission: write`): living spec paths +
   archive path. `disposition: pass` when every SHALL this change
   claimed is in `openspec/specs/` and `openspec/changes/<id>/` is
   gone. Leftover work is `task-red` — do not fold it away.
7. **Stop.** Do not `act`. Do not start the next change.

Handoff: report living spec paths and the archive path. If the shape
changed, the ADR amendment is part of the deliverable. Surprises go to
`docs/LEARNINGS.md`, one dated line each.

The designated folder agent is `intention:folder` (latest Opus). Dispatch
`subagent_type="intention:folder"` when the host supports plugin
agents; otherwise the ladder route + packet.
