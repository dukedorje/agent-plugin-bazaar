---
name: sprint-from-beads
description: >
  Read an existing beads corpus and write one OpenSpec change: proposal.md,
  design.md, and tasks.md. Propose an intend DAG of nodes for cuts that are
  real artifact dependencies. Does not create epic or story beads, and does
  not backfill story acceptance as the work list. Rewrites of non-empty bead
  fields stay gated.
  Triggers on: sprint from beads, migrate beads to a change, plan over existing beads,
  beads to a proposal, structure my beads.
user-invocable: true
argument-hint: "[--scope=<epic-id|label|open|all|query>] [--into=<change-id>] [--ceremony=lean|standard|full] [--accept-rewrites] [--no-rewrites] [--dry-run] [--db=PATH]"
model: opus
---

# sprint-from-beads

Read beads you already have and write the narrative they imply. The split
you propose is an intend DAG, not a new epic tree and not a story list.

Outputs:

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/design.md`
- `openspec/changes/<change-id>/tasks.md` — the proposed nodes and edges, not a checkbox per acceptance
- An intend DAG in the report, and `bd create --type node` when that type exists

Do not create epic beads. Do not create task beads as the breakdown. Do not
backfill acceptance criteria onto existing beads and call that the work
list. Do not create `docs/sprints/`, `.omc/`, or `phase-state.json`. Do not
run `sprint-plan` unless the user asked for the factory.

The DAG shape is `plugins/intention/references/intend-dag.md`. A node is one
acceptance surface and one landing (`add-<id>`, brief, or direct fix). An
edge exists only when the later node cannot start until the earlier one has
committed a usable artifact. A parent epic is not an edge.

## Authority

This skill reads beads the user authored. It does not silently overwrite them.

- Existing beads stay. Parents and dependency edges stay.
- A rewrite of a non-empty field is proposed, never applied silently.
  `--no-rewrites` skips those proposals. `--accept-rewrites` applies them.
  The default is to ask.
- Creating node beads is additive. It is not a rewrite of the corpus.

## 1. Initialize

Run `bd status` (pass `--db` when given). If there is no database, stop.
There is nothing to read.

| Flag | Default | Behavior |
|---|---|---|
| `--scope=` | `open` | An epic id plus its children, a label, `open`, `all`, or a `bd` query |
| `--into=` | confirm | Verb-led change id. Confirm it before writing when it was not passed |
| `--ceremony=` | auto | `lean`, `standard`, or `full`. A handful of beads is `lean` |
| `--accept-rewrites` | off | Apply proposed rewrites of non-empty fields |
| `--no-rewrites` | off | Skip those proposals |
| `--dry-run` | off | Print the plan and stop |
| `--db=PATH` | auto | Pass `--db PATH` on every `bd` call |

If scope is the default `open` and the corpus is more than 30 beads, report
the count and ask for a narrower scope or `--scope=all`. Do not guess.

## 2. Read

1. `bd list --json` for the scoped set.
2. `bd show <id> --json` for parent and fields. Do not trust `parent_id` from
   `bd list`. The parent is `bd show`, corroborated by a hierarchical id.
3. `bd dep list` for edges that already exist. Keep them. Do not recreate them.

Note epics, tasks, and orphans only as evidence of what the corpus already
says. Do not cluster orphans into new epics.

## 3. Propose

Scale depth to ceremony. `lean` is a short proposal and a short design note.
`standard` and `full` add rationale.

From the corpus and the code it names, write:

- **Why and What** for `proposal.md`. At `lean`, a few sentences are enough.
- **Architecture** for `design.md` when the beads assume a shape (store, auth,
  a library). Skip a long design when nothing consequential is implied, and
  say so in the file. Do not create decision beads.
- **Nodes** for the cuts that are real artifact dependencies. Merge beads that
  are the same acceptance surface. Leave descendants of an unlanded node
  provisional. One acceptance surface per node, taken from the beads you
  merged. Drop test tier, complexity, and a checkbox per old acceptance.

If a bead's claim is an unverified hypothesis, put one spike line on that
node. Do not run `spike`.

## 4. Gate

`--dry-run` prints the change id, the three files that would be written, the
DAG, and any rewrite proposals. Then it stops.

Otherwise write the three files. Create the change directory if needed. Do
not archive it. Do not edit a change already under `archive/`. Disposition
is PENDING. Factory progress does not activate it.

Then handle rewrites of non-empty fields:

- `--no-rewrites` — skip, and count them.
- `--accept-rewrites` — apply them.
- default — show the diffs and ask. Apply only the chosen subset.

Create node beads with `bd create --type node` when that type is accepted.
Title is the kebab node id. If the type is rejected, leave the DAG in the
report and say to run `setup`. On each source bead, `bd note` the node it
informed. Do not close those beads.

## 5. Report

```
Beads → openspec/changes/{change-id}/  (ceremony: {level})

  Corpus:  {n} beads read
  Docs:    proposal.md, design.md, tasks.md
  Nodes:   {list of node ids, edges, and landings}
  Notes:   {source bead} → {node id}
  Rewrites:{r} proposed, {applied} applied, {skipped} skipped

Next: intend {change-id}
```

Stop. Do not act, fold, or start `sprint-plan`.

## Limits

Inference is a draft. The user reviews the DAG before `steer`. Re-running
reads the same corpus and must not duplicate node beads: reuse a node whose
title is already that kebab. This skill does not undo a prior migration and
does not delete beads.
