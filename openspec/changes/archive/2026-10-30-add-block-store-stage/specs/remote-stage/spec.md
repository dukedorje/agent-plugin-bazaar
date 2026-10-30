## ADDED Requirements

### Requirement: Block-store stage fails closed

The system SHALL run a block-store stage as a stage step on the
named session, after the idle check and before the paste. A step
that does not finish SHALL NOT write the prompt file and SHALL NOT
submit the paste. A prompt file that already existed SHALL stay as
it was. An unready store mount is a step that does not finish.

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

The system SHALL treat `store` as a path on the session machine. That
path MAY be the mount root of the extra virtiofs store mount, or a
descendant that exists on that mount. The extra mount is a virtiofs
mount whose mountpoint is not the guest root `/`. The guest root is
itself virtiofs, so a filesystem-type check alone SHALL NOT count as
readiness. The system SHALL NOT name a host prefix or a virtiofs tag.
Attaching the mount is boot-time `extra_mounts` on a new guest and is
outside this copy.

Before any copy and before any prune, the session machine SHALL
confirm readiness: `store` exists, and the mount that contains it is
that extra virtiofs mount. An ordinary directory that merely exists
at the path, a path whose mount is the guest root, and the path `/`
SHALL be unready. The conductor SHALL NOT stat `store` as a local
path. An unready path SHALL return non-zero, SHALL start no copy,
and SHALL NOT prune `dest`, including when `delete` is `true`.

When the path is ready, the session machine SHALL copy that directory
tree to `dest` on the same machine. The copy SHALL use the same
directory shape as `rsync -a` of a source with no trailing slash: the
last component of `store` lands under an existing `dest`, or becomes
`dest` when `dest` is absent. One copy engine is enough. An empty
transport prefix runs that copy on the local session machine. A
non-empty prefix is the pane's existing SSH argv; the copy runs on
that host, and each path is one quoted argument (`shlex.quote`).
Example: `store` `/mnt/block-store/campaign` and `dest`
`/tmp/session-tree`, with SSH argv `ssh -o BatchMode=yes
root@guest.example`, sends those two paths as two arguments on that
host. A path that contains a space, such as
`/mnt/block-store/my tree`, stays one argument. The system SHALL
pass a prune of `dest` only when that entry's `delete` is `true` and
readiness has already succeeded. Mount inspection and the copy share
the entry's `timeout_sec` (default 600 seconds). A missing path, an
unready mount, a non-zero copy, or a timeout SHALL return non-zero
within that bound. A copy that has already started and then fails
is not required to restore `dest`.

#### Scenario: A descendant of the extra mount is ready

- GIVEN `store` `/mnt/block-store/campaign` exists on extra virtiofs mount root `/mnt/block-store`
- AND that mountpoint is not `/`
- AND the copy exits 0
- AND `dest` `/tmp/session-tree` is absent
- WHEN the pane is idle and the lock is held
- THEN the session machine copied the tree so `dest` is that directory
- AND the turn pastes one line

#### Scenario: The mount root itself is ready

- GIVEN `store` is the extra virtiofs mount root and that path exists
- AND the copy exits 0
- WHEN the pane is idle and the lock is held
- THEN the session machine copied `store` to `dest`
- AND the turn pastes one line

#### Scenario: An existing unattached directory does not prune

- GIVEN `store` `/mnt/block-store` exists as an ordinary directory on the guest-root mount
- AND that entry's `delete` is `true`
- AND `dest` already contains a file
- AND a prompt file already exists on the session machine
- WHEN the pane is idle and the lock is held
- THEN no copy starts
- AND `dest` is unchanged
- AND that prompt file is unchanged
- AND the turn does not submit the paste
- AND the face blocker is `pi-stage-failed`

#### Scenario: The guest root is not the store

- GIVEN `store` is `/`
- AND `/` is virtiofs
- WHEN the pane is idle and the lock is held
- THEN no copy starts
- AND the face blocker is `pi-stage-failed`

#### Scenario: The path is absent

- GIVEN a stage entry whose `store` is absent on the session machine
- AND a prompt file already on that machine
- WHEN the pane is idle and the lock is held
- THEN the step returns non-zero
- AND that prompt file is unchanged
- AND the turn does not submit the paste
- AND the face blocker is `pi-stage-failed`

#### Scenario: Inspection or the copy times out

- GIVEN a `store` entry whose mount inspection or copy exceeds `timeout_sec`
- WHEN the pane is idle and the lock is held
- THEN no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Quoted paths stay single arguments

- GIVEN a ready `store` `/mnt/block-store/my tree`
- AND `dest` `/tmp/session tree`
- AND a non-empty SSH prefix whose last item is the host
- WHEN the copy arguments are built
- THEN each path is one quoted argument on that host
- AND the conductor does not read `store` as a local path

#### Scenario: A conductor src entry does not use this copy

- GIVEN a stage entry with `src` and `dest` and no `store`
- WHEN the turn runs
- THEN this requirement performs no session-side copy

## MODIFIED Requirements

### Requirement: Stage declaration
<!-- base: b680e6958e473b95c902af364a7950ddc84e5555 openspec/specs/remote-stage/spec.md -->

The system SHALL accept an optional `stage` array on the task packet.
Each entry SHALL name exactly one source and `dest` (a path on the
machine that owns the named tmux session). A conductor source is
`src`, a path on the conductor machine, and that entry SHALL NOT name
`store`. A session source is `store`, a path on the session machine,
and that entry SHALL NOT name `src`. `delete` MAY be set `true` on
that entry. Absent `delete`, or `delete` `false`, SHALL NOT prune
`dest`. The system SHALL NOT invent a destination when `dest` is
missing. The system SHALL NOT read a prune flag from the environment.
An entry that names both sources, or neither source, is not a
declaration this requirement accepts.

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

#### Scenario: A store entry does not prune unless it says so

- GIVEN a stage entry with `store` and `dest` and no `delete`
- WHEN that entry is run
- THEN the runner is not asked to prune `dest`

### Requirement: Runner boundary
<!-- base: b680e6958e473b95c902af364a7950ddc84e5555 openspec/specs/remote-stage/spec.md -->

The system SHALL call the stage runner once per entry, in declaration
order, and SHALL stop at the first non-zero result. Later entries
SHALL NOT start. Each call SHALL receive that entry with exactly one
source selector, `dest`, and `delete` as a boolean. A conductor entry
passes `src` and does not pass `store`. A store entry passes `store`
and does not pass `src`. Each call SHALL also receive the transport
already configured for the pane (`PI_TMUX_SSH`, or local tmux when
`PI_TMUX_LOCAL=1`), and the tmux session name. The runner SHALL return
zero or non-zero. The runner SHALL own a time bound of the spawn
`timeout_sec` (default 600 seconds). The post-submit turn clock SHALL
NOT be that bound. Timeout, launch failure, and transport failure
SHALL become `pi-stage-failed` with no `write_prompt` and no `submit`,
and SHALL NOT be reported as `pi-session-unreachable`. The session
lock SHALL be released after the stage returns or fails.

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

#### Scenario: A store entry carries store

- GIVEN one stage entry with `store` and `dest` and no `src`
- WHEN the runner is called
- THEN the call includes `store`, `dest`, and `delete`
- AND the call does not include `src`

#### Scenario: A mixed list carries one selector each

- GIVEN a conductor entry and then a store entry
- AND the runner would return 0 for each
- WHEN the pane is idle and the lock is held
- THEN the first call includes `src` and not `store`
- AND the second call includes `store` and not `src`
- AND the turn pastes one line after both return 0

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
A packet that omits `stage` SHALL remain valid. The whole array SHALL
be rejected before any copy when any entry names both selectors, names
neither, or is otherwise malformed.

The same shapes SHALL be what these surfaces accept and pass through.
The closed `stage` item in `docs/contracts/agent-surface.schema.json`
SHALL be one of two objects with `additionalProperties` false: a
conductor object whose required fields are `src` and `dest`, or a
store object whose required fields are `store` and `dest`, each with
optional boolean `delete`. The `stage` row in
`docs/contracts/agent-surface.md` SHALL say the same. `validate_stage`
SHALL accept only those shapes. `cmd_stage` in
`plugins/intention/scripts/spawn.py` SHALL copy a valid array onto the
spawn spec and SHALL keep a malformed array off the no-declaration
path. `run_turn` SHALL normalize a conductor entry as `src`, `dest`,
and boolean `delete`, and a store entry as `store`, `dest`, and
boolean `delete`. The default runner registered from `run_pi` SHALL
apply the rsync requirement only to conductor entries and the session
store copy only to store entries.

#### Scenario: Packet stage reaches the turn

- GIVEN a valid `stage` array on the task packet
- WHEN the spawn spec is written
- THEN `spec.json` carries that array
- AND a later idle turn passes those entries to the runner before the paste

#### Scenario: A store-only list reaches the turn

- GIVEN a stage array of one entry with `store` and `dest` and no `src`
- WHEN the spawn spec is written
- THEN `spec.json` carries that entry
- AND a later idle turn passes `store`, not `src`, to the runner before the paste

#### Scenario: A mixed list reaches the turn

- GIVEN a well-formed conductor entry followed by a well-formed store entry
- WHEN the spawn spec is written
- THEN `spec.json` carries both entries in that order
- AND the runner sees the conductor entry before the store entry

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
- THEN no copy starts
- AND no paste is sent
- AND the face blocker is `pi-stage-failed`

#### Scenario: Neither selector is malformed

- GIVEN a stage entry with `dest` and no `src` and no `store`
- WHEN the turn starts
- THEN no copy starts
- AND the turn does not take the no-declaration path
- AND the face blocker is `pi-stage-failed`

#### Scenario: A later malformed entry starts no copy

- GIVEN a valid store entry followed by an entry that names neither `src` nor `store`
- WHEN the turn starts
- THEN no copy starts
- AND no paste is sent
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
