---
name: steer
description: >
  Human-gated guidance pass on the current intend DAG. Elicit
  architecture and direction with menus: recommended option first,
  always skip and decide-for-me. Records decisions on beads (and
  steer.md if a change dir exists) so change can update the node
  docs. Use after intend, before change, when asked to steer,
  give guidance, run architecture by me, or activate human-gate
  nodes. Not /ask (that is a run stop face).
user-invocable: true
argument-hint: "[<epic | bead | change-id>] [--lean|--explicit]"
---

# steer

The hole between `intend` and `change` on architecture / instrument /
human-gate nodes. Intend wrote basic docs per node. You sit with the
human, decide direction, and record it. `change` then updates those
docs (proposal, design, deltas). You do not write SHALLs. You do not
implement.

Load `../../references/shared.md` if it exists next to this plugin.
Read the citation table from disk. Do not paste those files.

```
intend → steer → change → advise → act → fold
```

`--ask` on intend presents the DAG and stops. This verb *is* the
conversation that stop was waiting for. `run --until ask` may halt
*for* steer. Do not name this `/ask`.

## Inputs

- Current DAG (`map --current`), or a named epic / bead / change-id.
- `--lean` / `--explicit` override elicitation depth. Default follows
  the highest node's density (lean / standard / explicit).
- No scope and no pin → print `map` index and stop. Do not invent a DAG.

## Depth

| Depth | Elicit |
|---|---|
| `lean` | Only forks that would change the DAG or a landing |
| `standard` | HIGH / CRITICAL forks (hard to reverse, protocol, auth, crypto, ownership) |
| `explicit` | Every remaining architecture fork (grill) |

MEDIUM / LOW auto-decide, log `[AUTO]`, do not menu. Ambiguous or
sensitive always includes the human (already a member).

## Procedure

1. **Scope.** Pin if they named an id (`map --current`). Load that DAG
   plus the architecture / instrument / human-gate nodes that still
   need direction. Read bead descriptions, living specs, in-flight
   changes. Do not re-intend unless there is no current DAG and they
   asked to plan — then hand off to `intend`.
2. **Forks.** Name 1–4 options each. Recommended first, with why.
   Group related forks into one menu. At most a handful of menus per
   turn; leftover forks wait.
3. **Menu.** Use the host multiple-choice primitive (Grok
   `ask_user_question`, Claude AskUserQuestion). If the host has none,
   print the template below and wait. Every question includes:
   - **Recommended** option first, labeled
   - **Skip** — leave undecided; do not block siblings
   - **Decide for me** — take the recommendation and continue
   Hosts add **Other**. "Decide for me and automate the rest" switches
   remaining forks to lean auto-log.
4. **Record.** For each decided fork, `bd update <id> --append-notes`
   (and `--design` when it is the node's design). If
   `openspec/changes/<id>/` exists (not `archive/`), write or append
   `steer.md` using the template. No `.omc/`. No session file besides
   the existing map pin. No SHALLs.
5. **Activate?** Direction on an architecture node is not a banner
   flip. If a PENDING change already exists and they accepted a
   direction, say so and leave the banner; they still activate (or
   already did by shipping). Do not `act`.
6. **Stop.** Print what was decided, skipped, auto-logged. Handoff:
   `change` reads bead design / `steer.md` and updates the node docs.
   Architecture / instrument then `advise` (reader Grok). Never `fold`.

## Menu template (when the host has no picker)

```markdown
## <fork title>

**What.** One sentence.
**Why it matters.** What later nodes cannot undo.

| Option | Means |
|---|---|
| **<A> (Recommended)** | … |
| <B> | … |
| Skip | Leave open; siblings may proceed |
| Decide for me | Take the recommendation |
```

## `steer.md` (only inside an existing change dir)

```markdown
# steer <change-id>

**When.** YYYY-MM-DD
**Depth.** lean | standard | explicit

## Decided
- <fork>: <choice> (user | auto | decide-for-me)
  Why: …

## Skipped
- <fork> — still open

## Feeds change
One paragraph `change` should take as direction. No SHALLs.
```

## Must not

- Implement, fold, or `act`
- Write SHALLs or living-spec deltas (`change` does)
- Invent `/ask` or a fourth store
- Enter `/run` as a default wave
- Revive sprint-plan / phase-state.json / sprint ADRs
- Re-intend a current DAG unasked
