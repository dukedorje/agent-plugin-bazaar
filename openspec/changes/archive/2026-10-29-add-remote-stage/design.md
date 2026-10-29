# Design

## Seam

`run_pi` already holds `~/.intention/pi-tmux.lock` (or `PI_TMUX_LOCK`)
across `run_turn`. The stage runs inside that hold, after
`parse_pane` says idle, before `write_prompt`.

```
idle?  no  → pi-session-not-idle, no stage, no paste
stage? no  → today's write_prompt + paste
runner? no → pi-stage-failed, no paste
step nonzero → pi-stage-failed, no paste
else → write_prompt + paste
```

A dirty composer still wins: do not start a copy while someone is
typing. Lock-not-acquired still wins: the second spawn sends nothing.

## Declaration

`stage` is an optional array on the task packet. `cmd_stage` copies
it onto the spawn spec. Each item:

| Field | Required | Meaning |
|---|---|---|
| `src` | yes | Path on the conductor machine |
| `dest` | yes | Path on the session machine |
| `delete` | no | `true` prunes dest. Absent or `false` does not |

No default dest. The live Pi checkout is not implied. Direction is
conductor → session machine, using the SSH prefix the pane already
uses (`PI_TMUX_SSH` or local tmux). The reverse direction is out of
scope.

Who may set `delete`: the author of that packet step, by writing
`true`. The adapter must not read an env var, a tmux option, or a
default in code. A later child may pass `--delete` to rsync only
when this boolean is `true`.

## Runner

`add-rsync-before-keys` registers the copy runner. This change ships
the hook and the contract the runner must meet. A declared stage with
no runner is a failure, not a skip. Skipping would paste into a
machine that never received the tree.

The adapter calls one runner, in declaration order, and stops at the
first failure. Later entries do not start.

Each call receives:

- the step `{src, dest, delete}` with `delete` normalized to a boolean
  (`true` only when the entry says `true`; absent is `false`)
- the transport the pane already uses: `PI_TMUX_SSH` argv, or local
  tmux when `PI_TMUX_LOCAL=1`
- the tmux session name

The runner returns `0` or non-zero. It does not paste and it does not
write the prompt file. Non-zero stops the stage. The adapter then
returns `pi-stage-failed` with no `write_prompt` and no `submit`.

The runner owns its time bound. `run_turn` starts its clock only after
`submit` (`pi_tmux.py` around the post-submit loop), so that clock
does not cover the stage. The bound is the spawn `timeout_sec`
(default 600). On expiry the runner returns non-zero. Launch and
transport failures (`OSError`, timeout, non-zero) are caught at the
stage call site and become the same face. They must not escape
`run_pi`, and they must not be reported as `pi-session-unreachable`.
`run_pi` still releases the lock in `finally`. A runner that ignores
its bound holds the lock until it returns; this change does not add
a second cancellation framework.

Tests inject a fake runner. They do not rsync onto the dev VM.

## Validation

`cmd_stage` copies `stage` only when every entry is an object with
non-empty string `src` and `dest`, and `delete` is either absent or
a boolean. Anything else (missing `dest`, a string `delete`, extra
fields) is a failed declaration: the turn does not paste, and the
absence of a usable `stage` is not treated as "no stage". The face
is `pi-stage-failed`. The schema edit is the same shape; old packets
that omit `stage` stay valid. A full packet-validator rewrite is out
of scope. The stage check is enough.

## Schema

`taskPacket` refuses unknown properties. Adding `stage` is an edit
to `docs/contracts/agent-surface.schema.json` plus one sentence in
`docs/contracts/agent-surface.md`. Old packets stay valid because
the field is optional. This spec does not grow a second field table.

## Not this node

`block-store-identity` (the Pi VM's extra filesystem is a mounted
path the harness can read) stays unverified on `add-block-store-stage`.
This design does not cite it and does not list it under unverified
hypotheses. A dest path is not that door.

`INTENTION_CODEX_VIA_PI` is unchanged. Declaring `stage` does not
turn it on.
