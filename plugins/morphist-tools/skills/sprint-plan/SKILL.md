---
name: sprint-plan
description: >
  Named sprint-plan intake factory whose plan is openspec/changes/<change-id>/.
  Phases stop at architecture. The next command is intend on that change id.
  Use only when the user asks for /sprint-plan or names the factory in a planning
  session. Route generic planning requests to intend.
user-invocable: true
disable-model-invocation: true
argument-hint: "[product-idea-or-prd-path] [--fast] [--thorough] [--auto] [--step] [--sprint-size=SIZE] [--skip-ux] [--continue[=phase]] [--restart-from=phase] [--change=ID] [--product=NAME] [--lean|--standard|--full]"
---

# Sprint Plan — OpenSpec Intake Factory

Start this factory only on a user request for `/sprint-plan` or a planning
session that names sprint-plan. For generic planning, use `intend` and do
not start Phase 0. Mode flags alone do not select this factory.

The plan is one `openspec/changes/<change-id>/` directory. All plan narrative
and phase progress belong there: `proposal.md`, `tasks.md`, optional
`design.md`, and `specs/<capability>/spec.md` deltas. Keep the phase files
under `phases/`; load the relevant file when its phase runs.

Never create `docs/sprints/`, `.omc/sprint-plan/`, or `phase-state.json`.
Do not use OMC sessions, state tools, symlinks, continuation hooks, numbered
sprints, standalone phase reports, or cross-session decision logs as plan
storage. An ADR in `ARCHITECTURE.md` is allowed only when the shape changes.
The factory stops at architecture. It does not mint an intake epic, a
child epic, a story bead, or a per-acceptance checkbox. Splitting the
change is `intend`.

## Arguments and modes

Product input may be a brief path or inline text. If missing, ask what the
user wants to build before creating a change directory.

| Argument | Effect |
|---|---|
| `--fast` | Single pass, AUTONOMOUS steering, `--auto`, lean detail |
| `--thorough` | GUIDED steering, architecture consensus and refinement, full detail |
| `--auto` | Continue between phases; GUIDED decision questions still apply |
| `--step` | Pause after every phase |
| `--sprint-size=SIZE` | Scope appetite: focused, standard, or ambitious; no sprint number |
| `--skip-ux` | Skip UX elaboration and record why in `tasks.md` |
| `--continue[=phase]` | Resume the next unchecked phase, or after the named completed phase |
| `--restart-from=phase` | Reopen that phase and all downstream phase checkboxes |
| `--change=ID` | Select an existing change for continuation or restart |
| `--product=NAME` | Record the product association in `proposal.md` |
| `--lean`, `--standard`, `--full` | Pin detail level; `--ceremony=LEVEL` is equivalent |

`--thorough` wins over `--fast`; `--restart-from` wins over `--continue`;
`--step` wins over `--auto`. Explicit detail level wins over mode defaults.
Default: single pass with GUIDED steering and pauses at requirements,
scoping, and architecture. Lean means short sections in the
same change files, standard adds relevant rationale, full adds alternatives
and deeper validation. Detail level never changes the output destinations.
Escalate detail when HIGH/CRITICAL decisions demand it and record the reason
in `tasks.md`; do not silently downgrade an established level.

Do not create story beads, an intake epic, or a checkbox per acceptance.
Do not run `sprint-to-beads`. `--sprint=ID` no longer selects a numbered
sprint; use `--change=ID`.

## Initialization

1. Read the relevant living specs and repository instructions. For an
   existing change, read its disposition banner before editing it; intake
   does not grant activation or implementation authority.
2. For new intake, mint one verb-led kebab-case change id from the goal,
   such as `add-account-recovery`. Check for collisions; never overwrite an
   unrelated change. Set `CHANGE_ID` to that id and `SPEC_DIR` to
   `openspec/changes/<change-id>/`. All later phases reuse this directory.
3. Create `proposal.md` with a PENDING disposition and sections Why, What,
   Impact, User journey & surfaces, and Out of scope. Preserve an existing
   change's disposition; factory progress does not activate it.
4. Create `tasks.md` with the phase checklist below. Keep implementation
   and fold tasks separate from these intake phase boxes. Add mode, steering,
   detail level, product, and scope appetite as short notes in this file.
5. Add spec delta directories as requirements identify capabilities. Create
   `design.md` only for UI journeys or architecture that warrants it.

```markdown
## Intake phases
- [ ] Phase 0: Discovery — proposal.md Why
- [ ] Phase 1: Requirements — proposal.md What and spec deltas
- [ ] Phase 1B: Scoping — proposal.md Out of scope
- [ ] Phase 1.5: UX — design.md journey, only for UI; otherwise record skip reason
- [ ] Phase 2A: Architecture — design.md; ADR only if shape changes
```

## Phase routing

| Phase | Instruction file | Output |
|---|---|---|
| 0 Discovery | [phase-0-discovery.md](phases/phase-0-discovery.md) | `proposal.md` Why |
| 1 Requirements | [phase-1-requirements.md](phases/phase-1-requirements.md) | spec deltas and `proposal.md` What |
| 1B Scoping | [phase-1b-sprint-scoping.md](phases/phase-1b-sprint-scoping.md) | `proposal.md` Out of scope |
| 1.5 UX | [phase-1.5-ux-design.md](phases/phase-1.5-ux-design.md) | `design.md` journey, only for UI |
| 2A Architecture | [phase-2a-architecture.md](phases/phase-2a-architecture.md) | `design.md`; bounded ADR if shape changes |

Execute in phase order. Read each prior output from the change directory,
then edit the mapped file in place, preserving other sections. If delegating,
send a task packet with `CHANGE_ID`, `SPEC_DIR`, input anchors, exact allowed
outputs, and acceptance. Foreign harnesses receive packets, never host slash
commands. Require a final response containing outputs, paths, and blockers.

Check the matching phase box only after its output exists and required
steering is resolved. For a skipped conditional phase, record the reason next
to its checked box; no output file is needed. Do not open a phase after
2A. Do not create beads as the breakdown of this intake.

## Steering and continuation

Use [decision-steering.md](phases/decision-steering.md) for significant
choices. Store steering settings and calibration notes in `tasks.md` and
rationale in the phase's mapped narrative file. Present pending decisions
before marking a phase complete. At a pause report the change id, phase,
file paths, decisions, blockers, and next phase; wait for requested input.

For continuation, resolve `--change=ID` or the unambiguous current change
from session context. If ambiguous, ask which change; do not guess the most
recent folder. Read its files and resume at the first unchecked phase.
A named `--continue=phase` requires that phase's box and output to be valid;
do not skip earlier unchecked phases.

For restart, uncheck the selected phase and every downstream phase in
`tasks.md`, recording why. Keep existing narrative as input and reconcile it
in place. Reopen the downstream phase boxes when conclusions change.
A failed phase stays unchecked. Retry an agent failure once, then
report the blocker with recovery options. No separate state store is needed.

At completion, report the change directory, the phases whose boxes are
checked, and the next command: `intend <change-id>`. Stop there. Intake
completion does not mean implementation, activation, fold, or a DAG.
Never edit the living spec or archive as part of intake.
