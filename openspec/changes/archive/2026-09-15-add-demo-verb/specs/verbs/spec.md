## ADDED Requirements

### Requirement: demo is the human trying the iteration

`demo` SHALL present a journey so the human can try a landed act.
Slice one is the **internal** ring only. Journey source SHALL be the
change's proposal `User journey & surfaces` section and/or the Next
command on its owed boxes. The change dir SHALL be
`openspec/changes/<id>/` if present, else
`openspec/changes/archive/*-<id>/`. Slice one SHALL NOT be a fold
gate; the fold predicate stays the single rule from
`update-run-ooda`. Bare `/run` MAY fold the change first. Residue
SHALL be at most a bead comment or a signed result with
`permission: read`. It SHALL NOT write `demo.md`, mint an owed box,
or add a `demo` token to the EYES / by-eye / human-verify vocabulary
(`run.py` `EYES_RE`). It SHALL NOT deploy, fold, implement leftover
tasks, or flip an EYES / by-eye / human-verify box. It SHALL NOT be
staging or production. Mesoteric (staging) and exoteric (production)
rings SHALL be named as later, not built in this requirement. Not
every act owes a demo.

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

#### Scenario: Demo invents no tracker

- GIVEN a proposal stores demo state in `openspec/changes/<id>/demo.md`,
  a new owed box, or an EYES / by-eye / human-verify token
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: Demo resolves archive

- GIVEN `add-run-wave-workflow` has been folded to
  `openspec/changes/archive/*-add-run-wave-workflow/`
- WHEN `/demo add-run-wave-workflow` runs
- THEN the journey is read from the archived proposal and/or the
  Next command on its owed boxes
- AND demo does not print Empty

#### Scenario: Empty — nothing landed to try

- GIVEN no inflight `openspec/changes/<id>/` and no
  `openspec/changes/archive/*-<id>/` for the named id (and no
  current intend DAG landing)
- WHEN `/demo` runs
- THEN it prints `/status` and stops
- AND it writes no box, no `demo.md`, and does not fold

#### Scenario: Demo is not a fold gate

- GIVEN a fold-legal ACTIVE BUILD change
- WHEN bare `/run` walks `--until roll`
- THEN fold may run before anyone types `/demo`
- AND that is legal for this slice

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
