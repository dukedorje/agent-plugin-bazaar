# remote-stage

What **is** built: a declared stage on the named Pi tmux session runs
after the idle check and before the paste. A failed or unregistered
stage does not type. No declaration keeps the one-file prompt. Folded
from `add-remote-stage` on 2026-10-29.

## Purpose

Keys wait until every declared stage entry has finished under the
session lock already held for the paste.

## ADDED Requirements

### Requirement: Stage declaration

The system SHALL accept an optional `stage` array on the task packet.
Each entry SHALL name `src` (a path on the conductor machine) and
`dest` (a path on the machine that owns the named tmux session).
`delete` MAY be set `true` on that entry. Absent `delete`, or
`delete` `false`, SHALL NOT prune `dest`. The system SHALL NOT
invent a destination when `dest` is missing. The system SHALL NOT
read a prune flag from the environment.

#### Scenario: No declaration

- GIVEN a Pi spawn spec with no `stage` key
- WHEN the pane is idle and the session lock is held
- THEN the turn copies the prompt file and pastes one line, as it
  does without this capability

#### Scenario: Empty list

- GIVEN a Pi spawn spec whose `stage` is an empty array
- WHEN the pane is idle and the session lock is held
- THEN the turn copies the prompt file and pastes one line

#### Scenario: Delete only when the entry says so

- GIVEN a stage entry with `src` and `dest` and no `delete`
- WHEN that entry is run
- THEN the runner is not asked to prune `dest`

### Requirement: Stage before the paste

When `stage` is non-empty, the system SHALL run every entry after the
idle check and before `write_prompt`, while the Pi session lock is
held. The system SHALL use the named tmux session already configured
for the paste. The system SHALL NOT start a second harness process.
The system SHALL NOT send Ctrl-C. A non-zero entry SHALL finish the
turn without `write_prompt` and without `submit`, and the face
blocker SHALL be `pi-stage-failed`. A non-empty `stage` with no
runner registered SHALL finish the same way. Every entry exiting 0
SHALL continue into the prompt-file copy and the one-line paste.

#### Scenario: A failed step does not paste

- GIVEN a non-empty `stage` and a runner that returns non-zero
- WHEN the pane is idle and the lock is held
- THEN the composer receives no paste
- AND the face blocker is `pi-stage-failed`

#### Scenario: A zero step pastes

- GIVEN a non-empty `stage` and a runner that returns 0 for each entry
- WHEN the pane is idle and the lock is held
- THEN the turn pastes the one line that names the prompt file

#### Scenario: No runner fails closed

- GIVEN a non-empty `stage` and no runner registered
- WHEN the pane is idle and the lock is held
- THEN the composer receives no paste
- AND the face blocker is `pi-stage-failed`

#### Scenario: Dirty composer runs nothing

- GIVEN a non-empty `stage`
- WHEN the pane is not idle
- THEN no stage entry runs
- AND no paste is sent

#### Scenario: Lock not held runs nothing

- GIVEN a non-empty `stage`
- WHEN the session lock is not acquired
- THEN no stage entry runs
- AND no paste is sent

### Requirement: Runner boundary

The system SHALL call the stage runner once per entry, in declaration
order, and SHALL stop at the first non-zero result. Later entries
SHALL NOT start. Each call SHALL receive that entry (`src`, `dest`,
and `delete` as a boolean), the transport already configured for the
pane (`PI_TMUX_SSH`, or local tmux when `PI_TMUX_LOCAL=1`), and the
tmux session name. The runner SHALL return zero or non-zero. The
runner SHALL own a time bound of the spawn `timeout_sec` (default
600 seconds). The post-submit turn clock SHALL NOT be that bound.
Timeout, launch failure, and transport failure SHALL become
`pi-stage-failed` with no `write_prompt` and no `submit`, and SHALL
NOT be reported as `pi-session-unreachable`. The session lock SHALL
be released after the stage returns or fails.

#### Scenario: First failure stops the list

- GIVEN two stage entries and a runner that returns non-zero for the first
- WHEN the pane is idle and the lock is held
- THEN the second entry is not started
- AND no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Timeout does not paste

- GIVEN a non-empty `stage` and a runner that exceeds `timeout_sec`
- WHEN the pane is idle and the lock is held
- THEN no paste is sent
- AND the face blocker is `pi-stage-failed`

### Requirement: Stage declarations are checked

The system SHALL copy `stage` from the task packet onto the spawn spec
only when every entry has a non-empty string `src`, a non-empty string
`dest`, and a `delete` value that is absent or boolean. A malformed
entry SHALL NOT be treated as an absent `stage`, SHALL NOT prune, and
SHALL finish the turn as `pi-stage-failed` with no paste. A packet
that omits `stage` SHALL remain valid.

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
