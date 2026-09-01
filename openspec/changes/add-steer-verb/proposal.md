# add-steer-verb

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-31 (chat: write the skill and ship on main).

## Why

`intend` writes a DAG with architecture nodes behind `human-gate`.
`--ask` presents that DAG and stops. `advise` reviews a change that
already has SHALLs. Nothing is the conversation in between: the
human giving direction, with menus, so `change` can update the node
docs. `run --until ask` is a campaign stop face and forbids `/ask`
as a verb (`update-run-ask`).

## What

- Add verb **`steer`**: human-gated guidance on the current intend
  DAG. Menus always include a recommended option, skip, and
  decide-for-me. Depth follows density (`--lean` / `--explicit`).
- Residue: bead design/notes. If `openspec/changes/<id>/` already
  exists, also `steer.md`. No fourth store. No SHALLs.
- Not a default `/run` wave. Not `/ask`.
- Capabilities: ADDED on `verbs`. MODIFIED `packaging`,
  `default-loop`, shared-references list on `verbs`.

## Impact

- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`
- ADRs: will amend `ARCHITECTURE.md` (verb list) when this folds

## User journey & surfaces

Duke, from chat, after `/intend` on architecture.

1. Says `/steer` (or `/steer identikey-core-trr.1`).
2. **Working** — a handful of menus; recommended first; skip /
   decide-for-me on every question. Decisions land on beads.
3. **Empty** — no current DAG and no named id: print `map` index.
4. **Off** — skill missing; `intend --ask` still presents the DAG.

`No new UI because` the surfaces are `/steer` and the host
multiple-choice primitive (Grok `ask_user_question`, Claude
AskUserQuestion).

## Out of scope

- Default `/run` wave
- `/ask` or `/inbox`
- Writing SHALLs (that is `change`)
- Reviving sprint-plan Decision Steering files
