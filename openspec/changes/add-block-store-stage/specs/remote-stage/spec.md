## ADDED Requirements

### Requirement: Block-store stage fails closed

The system SHALL run a block-store stage as a stage step on the
named session, after the idle check and before the paste. A step
that does not finish SHALL NOT write the prompt file and SHALL NOT
submit the paste. A prompt file that already existed SHALL stay as
it was.

#### Scenario: The store step does not finish

- GIVEN a stage entry that names `store` and `dest`
- AND a prompt file already on the session machine
- WHEN that step does not finish
- THEN that prompt file is unchanged
- AND the turn does not write a prompt
- AND the turn does not submit the paste

#### Scenario: No store declaration

- GIVEN a Pi spawn spec with no `store` entry
- WHEN the pane is idle
- THEN this requirement adds no session-side copy

### Requirement: Session store copy

The system SHALL treat `store` as a path on the session machine: the
guest mount of a host directory attached with virtiofs. The session
machine SHALL copy that path to `dest` on the same machine. The
conductor SHALL NOT read `store` as a local path. The system SHALL
pass a prune of `dest` only when that entry's `delete` is `true`.
A missing `store`, a non-zero copy, or a timeout SHALL return
non-zero within `timeout_sec`. The system SHALL NOT name a host
prefix or a virtiofs tag. Attaching the mount is boot-time
`extra_mounts` on a new guest and is outside this copy.

#### Scenario: The guest mount exists

- GIVEN a stage entry whose `store` exists on the session machine
- AND the copy exits 0
- WHEN the pane is idle and the lock is held
- THEN the session machine copied `store` to `dest`
- AND the turn pastes one line

#### Scenario: The guest mount is missing

- GIVEN a stage entry whose `store` is absent on the session machine
- AND a prompt file already on that machine
- WHEN the pane is idle and the lock is held
- THEN the copy returns non-zero
- AND that prompt file is unchanged
- AND the turn does not submit the paste
- AND the face blocker is `pi-stage-failed`

#### Scenario: The copy times out

- GIVEN a `store` entry whose copy exceeds `timeout_sec`
- WHEN the pane is idle and the lock is held
- THEN no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: A conductor src entry does not use this copy

- GIVEN a stage entry with `src` and `dest` and no `store`
- WHEN the turn runs
- THEN this requirement performs no session-side copy

## MODIFIED Requirements

### Requirement: Stage declarations are checked
<!-- base: b680e6958e473b95c902af364a7950ddc84e5555 openspec/specs/remote-stage/spec.md -->

The system SHALL copy `stage` from the task packet onto the spawn spec
only when every entry is one of these shapes. A conductor entry has a
non-empty string `src`, a non-empty string `dest`, no `store`, and a
`delete` value that is absent or boolean. A store entry has a
non-empty string `store`, a non-empty string `dest`, no `src`, and a
`delete` value that is absent or boolean. `src` remains a path on the
conductor machine. `store` is a path on the session machine. A
malformed entry SHALL NOT be treated as an absent `stage`, SHALL NOT
prune, and SHALL finish the turn as `pi-stage-failed` with no paste.
A packet that omits `stage` SHALL remain valid.

#### Scenario: Packet stage reaches the turn

- GIVEN a valid `stage` array on the task packet
- WHEN the spawn spec is written
- THEN `spec.json` carries that array
- AND a later idle turn passes those entries to the runner before the paste

#### Scenario: Malformed delete does not prune

- GIVEN a stage entry whose `delete` is a string
- WHEN the turn starts
- THEN no runner is asked to prune
- AND no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Missing dest is not "no stage"

- GIVEN a stage entry with `src` and no `dest`
- WHEN the turn starts
- THEN the turn does not take the no-declaration path
- AND no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Store and src together is malformed

- GIVEN a stage entry that names both `src` and `store`
- WHEN the turn starts
- THEN no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Store without dest is malformed

- GIVEN a stage entry with `store` and no `dest`
- WHEN the turn starts
- THEN the turn does not take the no-declaration path
- AND no paste is sent
- AND the face blocker is `pi-stage-failed`

### Requirement: Rsync runner
<!-- base: b680e6958e473b95c902af364a7950ddc84e5555 openspec/specs/remote-stage/spec.md -->

When a stage entry names `src` and does not name `store`, the system
SHALL copy `src` to `dest` with `rsync -a` before the prompt paste.
The system SHALL pass `--delete` only when that entry's `delete` is
`true`. An empty transport prefix SHALL copy between local paths. A
non-empty prefix SHALL be the SSH argv the pane already uses, and
`dest` SHALL be on that host. The runner SHALL return within
`timeout_sec` (default 600 seconds). A missing `src`, a non-zero
rsync, or a timeout SHALL return non-zero, and the turn SHALL NOT
paste. The system SHALL NOT contact a host other than the one in
that prefix. An entry that names `store` SHALL NOT be copied by this
requirement.

#### Scenario: A zero copy pastes

- GIVEN a stage entry whose `src` exists and a runner that exits 0
- WHEN the pane is idle and the lock is held
- THEN `rsync` was invoked with `-a` and without `--delete`
- AND the turn pastes one line

#### Scenario: A failed copy does not paste

- GIVEN a stage entry and a runner that exits non-zero
- WHEN the pane is idle and the lock is held
- THEN no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: No declaration does not rsync

- GIVEN a Pi spawn spec with no `stage` key
- WHEN the turn runs
- THEN `rsync` is not invoked
- AND the turn pastes one line

#### Scenario: Delete only when the entry says so

- GIVEN a stage entry with `delete` true
- WHEN the runner builds the rsync argv
- THEN the argv includes `--delete`
- AND an otherwise identical entry with `delete` false does not

#### Scenario: A store entry does not rsync src

- GIVEN a stage entry with `store` and `dest` and no `src`
- WHEN the turn runs
- THEN this requirement does not invoke `rsync` for a conductor `src`
