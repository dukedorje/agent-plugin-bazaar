## ADDED Requirements

### Requirement: Rsync runner

When a stage entry is declared, the system SHALL copy `src` to `dest`
with `rsync -a` before the prompt paste. The system SHALL pass
`--delete` only when that entry's `delete` is `true`. An empty
transport prefix SHALL copy between local paths. A non-empty prefix
SHALL be the SSH argv the pane already uses, and `dest` SHALL be on
that host. The runner SHALL return within `timeout_sec` (default 600
seconds). A missing `src`, a non-zero rsync, or a timeout SHALL return
non-zero, and the turn SHALL NOT paste. The system SHALL NOT contact
a host other than the one in that prefix.

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
