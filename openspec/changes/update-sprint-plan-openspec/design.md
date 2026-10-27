# update-sprint-plan-openspec

## Phase map

The factory still runs in phase order. Plan narrative and phase
progress land in the change directory. Two outputs are not the plan:
an ADR in `ARCHITECTURE.md` when the shape changes, and a child bead
or child change id from epic split. Story beads stay in
`update-sprint-plan-beads`.

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

`disable-model-invocation` stays. The factory starts when the user
asks for `/sprint-plan` or for a planning session that names the
factory. A generic planning request starts at `intend` and does not
start Phase 0. The description names the change directory as the plan
and points other planning at `intend`. It stops saying PARKED once
this change lands.

## Change id

The factory mints one verb-led change id at intake. Later phases edit
that directory. They do not number sprints.
