# update-sprint-plan-openspec

## Phase map

The factory still runs in phase order. Each phase writes into the change
directory. It does not invent a sibling document.

| Phase | Lands in |
|---|---|
| 0 Discovery | `proposal.md` Why |
| 1 Requirements | spec deltas, and `proposal.md` What |
| 1B Scoping | `proposal.md` Out of scope |
| 1.5 UX | `design.md` journey, and only when there is a UI |
| 2A Architecture | `design.md`, plus an ADR in `ARCHITECTURE.md` when the shape changes |
| 2B Epics | child beads, or child change ids when a capability splits |
| 3–4 Stories | not this change (`update-sprint-plan-beads`) |
| 5 Validation | remaining `tasks.md` boxes; `advise` when the rigor is architecture |

## State

`tasks.md` is the phase cursor. A checked box is a finished phase for
this change. There is no `phase-state.json` and no `.omc/` session.

## Invocation

`disable-model-invocation` stays. The user asks for the factory or for
a planning session that names it. Unrelated work still starts at `intend`.
The description stops saying PARKED once this change lands.

## Change id

The factory mints one verb-led change id at intake. Later phases edit
that directory. They do not number sprints.
