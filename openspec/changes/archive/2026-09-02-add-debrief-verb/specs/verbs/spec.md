## ADDED Requirements

### Requirement: debrief expands a finished or failed unit

`debrief` SHALL take a just-finished or failed unit (bead id,
change-id, or signed result) and emit an expansion: what happened,
context the brief did not have, takeaways, and what the next
`intend` should extract. It SHALL stop so a human can process. It
SHALL NOT implement, fold, or treat the debrief page as durable
truth. Hard-won facts SHALL go to `docs/LEARNINGS.md` as one dated
line each. It SHALL NOT be a default `/run` wave.

#### Scenario: Finished unit

- GIVEN a closed bead or a signed result with `disposition: pass`
- WHEN `debrief` runs on that id
- THEN the output names what landed, takeaways, and what intend
  should extract
- AND no product paths were edited

#### Scenario: Failed unit

- GIVEN a signed result with `disposition` other than `pass`, or a
  parked / task-red node
- WHEN `debrief` runs on that id
- THEN the output names what was tried, what broke, takeaways, and
  what intend should extract
- AND the banner of any in-flight change is unchanged

#### Scenario: Debrief is not a spec

- GIVEN a debrief page from last week
- WHEN an agent cites it as current behavior
- THEN that citation is wrong; living spec, ADR, or LEARNINGS.md is
  the residue

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`,
`debrief`, `ready`, and `run` SHALL load
`plugins/intention/references/shared.md` and SHALL NOT restate
packet fields or topology wirings. Adding a tenth law to a skill
body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`
