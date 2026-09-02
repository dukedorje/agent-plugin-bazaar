## ADDED Requirements

### Requirement: map reprints the intend DAG with live residue

`map` SHALL print the intend-dag shape (intention, orient if known,
per-node goal/landing/deps, ready-set, needs activation, next) plus
live **Status**, **Wave**, and **Outcome** for each node. Status
SHALL come from the tracker. Wave SHALL name the last known stage
(change banner, advise verdict, act disposition, fold/archive).
Outcome SHALL be the signed result `distilled.summary` or the bead
close reason. It SHALL NOT implement, unpark, or invent a second
store. It SHALL NOT be a default `/run` wave.

No scope SHALL list open epics and their children. A named epic,
bead, or change-id SHALL focus that graph.

#### Scenario: Map an epic

- GIVEN epic `bazaar-6os` has a closed child `add-debrief-verb`
- WHEN `map bazaar-6os` runs
- THEN the page has a DAG node for that child
- AND Status is closed
- AND Outcome is the close reason or distilled summary

#### Scenario: Map invents no tracker

- GIVEN a proposal stores map state in a new file besides beads
  and openspec
- WHEN it is reviewed
- THEN it is rejected against this requirement

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`,
`debrief`, `map`, `ready`, and `run` SHALL load
`plugins/intention/references/shared.md` and SHALL NOT restate
packet fields or topology wirings. Adding a tenth law to a skill
body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`
