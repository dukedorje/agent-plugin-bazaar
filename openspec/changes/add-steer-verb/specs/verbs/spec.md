## ADDED Requirements

### Requirement: steer elicits human direction before change

`steer` SHALL load the current intend DAG (or a named epic / bead /
change-id) and elicit architecture and direction through
multiple-choice menus. Every menu SHALL include a recommended
option, skip, and decide-for-me. It SHALL record decisions on the
node's bead (`design` / notes). If `openspec/changes/<id>/` exists
and is not archived, it SHALL also write `steer.md` there. It SHALL
NOT write SHALLs, implement, fold, or `act`. It SHALL NOT invent
`/ask` or a fourth store. It SHALL NOT be a default `/run` wave.

Elicitation depth SHALL follow the highest node's density, or
`--lean` / `--explicit`. `standard` SHALL menu only HIGH / CRITICAL
forks. Skip SHALL leave a fork open and SHALL NOT block siblings.

#### Scenario: Architecture node after intend

- GIVEN `map --current` is `mjolnir-mesh-st1` and
  `identikey-core-trr.1` needs direction
- WHEN `steer` runs
- THEN the human is offered menus with a recommended option, skip,
  and decide-for-me
- AND decided forks are appended on the bead
- AND no living-spec SHALL was written

#### Scenario: Steer invents no tracker

- GIVEN a proposal stores steer state in a new file besides beads
  and `openspec/changes/<id>/steer.md`
- WHEN it is reviewed
- THEN it is rejected against this requirement

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `steer`, `change`, `advise`, `act`, `fold`,
`brief`, `debrief`, `map`, `ready`, and `run` SHALL load
`plugins/intention/references/shared.md` and SHALL NOT restate
packet fields or topology wirings. Adding a tenth law to a skill
body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`
