# cut-sprint-plan-after-architecture

> **ACTIVE BUILD**

## Why

`sprint-plan` still splits a finished architecture into an intake epic, story beads, and a checkbox per acceptance. `intend` already splits a goal into a DAG of nodes, one acceptance surface each, with edges only where a later node needs a committed artifact. The later factory phases write that split a second time, and they write the contracts before any dependency has landed.

## What

- `sprint-plan` keeps phases 0, 1, 1B, 1.5, and 2A. When 2A is checked, the next command is `intend` on that change id.
- The factory does not mint an intake epic, a child epic, a story bead, or a per-acceptance checkbox, and it does not run `sprint-to-beads`.
- `sprint-to-beads` leaves the plugin. A request to materialize stories is answered with `intend`.
- `sprint-from-beads` still writes one change directory from an existing beads corpus. The split it proposes is intend nodes, not epics and story tasks.
- The living rule "a story is a bead and a checkbox" is removed. The unit of decomposition is the intend node.

## Impact

- Capabilities: MODIFIED default-loop (`sprint-plan is parked`, `Plan documents are the change directory`); REMOVED default-loop (`A story is a bead and a checkbox`); ADDED default-loop (intake ends at architecture, decomposition is an intend node, a beads corpus proposes nodes, `sprint-to-beads` is dropped).
- ADRs: none

## User journey & surfaces

No new UI because the surfaces are `/sprint-plan`, `/intend`, and `openspec/changes/<change-id>/`.

Working: the user names the factory. Discovery through architecture land in that change. The completion line is `intend <change-id>`. `intend` writes the DAG. `bd ready` lists nodes.

Empty: a change whose scope does not split stays one node. The factory does not invent an epic to hold it.

Failed: `bd` is missing or the change id is ambiguous. The factory stops with the phase unchecked and does not create story beads.

Off: a generic planning request never enters the factory. It starts at `intend`.

## Out of scope

- Migrating an intake that already finished phases 2B–5. That is a one-shot bridge prompt, not this change.
- `verify`, `done-validate`, and `review-fix`. They still look for `.omc/sprint-plan/`.
- Retargeting `/prd` and `/vision`. They still hand off to `/sprint-plan <change-id>`.
- Editing `openspec/specs/` before fold.
