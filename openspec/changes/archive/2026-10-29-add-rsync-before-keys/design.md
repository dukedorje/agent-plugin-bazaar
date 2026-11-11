# Design

The hook in `f1e3a74` calls `STAGE_RUNNER(step, ssh_argv, session, timeout_sec)`
and treats non-zero as `pi-stage-failed`. This change fills that global.
It does not change the order, the lock, or the face.

`ssh_argv` is `[]` for `PI_TMUX_LOCAL=1`. Then:

```
rsync -a [--delete] <src> <dest>
```

When `ssh_argv` is non-empty it is the same argv the pane uses
(`ssh` plus options plus the host). The host is the last argument.
The runner drops that host into `rsync -e` and writes the destination
as `host:dest`:

```
rsync -a [--delete] -e <ssh argv without the host> <src> <host>:<dest>
```

`--delete` is included only when the normalized step has `delete`
true. No environment variable adds it.

`subprocess` timeout is `timeout_sec`. Timeout returns non-zero.
A missing `src` returns non-zero without inventing a destination.
The session name is unused by rsync. The runner does not send keys.

Tests put a fake `rsync` first on `PATH`, or copy between temp dirs
with a local prefix. They do not SSH to the dev VM.
