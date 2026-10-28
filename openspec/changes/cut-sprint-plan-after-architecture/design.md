# Design

## Handoff

`sprint-plan` fills one change through architecture. `intend` is the only splitter after that. The factory's completion report names the change id and the command `intend <change-id>`. It does not open Phase 2B.

`intend` reads that change the way it already reads `openspec/changes/*/proposal.md`. It does not receive story beads, an intake epic, or a checkbox list as its work breakdown.

## What a node is

A node is one acceptance surface and one landing: `add-<id>`, a brief, or a direct fix. An edge means the later node cannot start until the earlier one has committed a usable artifact. Descendants of an unlanded node stay provisional. The bead type is `node`.

An epic bead is not created to parent that graph. `bd ready` follows blockers.

## Beads already on disk

`sprint-from-beads` writes `proposal.md`, `design.md`, and `tasks.md` for one change, then proposes nodes for the cuts that are real artifact dependencies. It does not create epic beads, does not create task beads as the breakdown, and does not backfill story acceptance as the work list. Existing beads are read. Rewrites of non-empty fields stay gated.

## Dropped materializer

`sprint-to-beads` is removed from `plugins/morphist-tools/skills/`. `CONVENTIONS.md` records the drop. A person who asks to materialize stories is pointed at `intend` on the change. The skill file is not left in place as a parked procedure. An agent that opens it would follow the old materializer.
