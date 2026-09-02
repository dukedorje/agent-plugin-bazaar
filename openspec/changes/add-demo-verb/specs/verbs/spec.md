## ADDED Requirements

### Requirement: demo is the human trying the iteration

`demo` SHALL load a landed act (current intend DAG, named change-id,
or the Next command already on the change) and present a journey so
the human can try the feature. Slice one is the **internal** ring
only. It SHALL NOT deploy, fold, implement leftover tasks, or flip
an EYES / by-eye / human-verify box. It SHALL NOT be staging or
production. Mesoteric (staging) and exoteric (production) rings
SHALL be named as later, not built in this requirement.

#### Scenario: After act, before fold

- GIVEN a landed `act` on `add-run-wave-workflow` and Duke says
  `/demo`
- WHEN `demo` runs
- THEN he is given a journey to try the wave (e.g. `/run-wave`)
- AND no EYES box is checked
- AND no deploy ran

#### Scenario: Demo does not deploy

- GIVEN `/demo` on a kernel change with no host
- WHEN the skill runs
- THEN it does not ssh, publish, or unpark a P1 host

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `steer`, `change`, `advise`, `act`, `fold`,
`brief`, `debrief`, `map`, `ready`, `run`, `run-wave`, `consult`,
and `demo` SHALL load
`plugins/intention/references/shared.md` and SHALL NOT restate
packet fields or topology wirings. Adding a tenth law to a skill
body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`
