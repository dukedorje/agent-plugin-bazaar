# add-rsync-before-keys

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-10-29 by the same campaign grant as `stage-before-keys`
("activate and /run --go"). The architecture artifact is usable:
living `openspec/specs/remote-stage/spec.md`, folded in `baf808a`.
This node was blocked until that contract existed. `add-block-store-stage`
stays unscaffolded. Its spike `block-store-identity` is still open.

## Preparation

- Upstream: `baf808a` (living remote-stage) and `f1e3a74` (the hook).
  `pi_tmux.STAGE_RUNNER` is still `None`, so a declared stage fails
  closed. `run_pi` holds the lock and passes `stage` into `run_turn`.
- Outcome: still valid. Direction is conductor → session machine.
  `--delete` only when the entry says `true`.
- Authority: the grant above. Bounds unchanged: no second Pi, no sync
  onto the production hypervisor, no default `INTENTION_CODEX_VIA_PI`,
  no block-store protocol.

## Why

The hook refuses to paste when a stage is declared and no runner is
registered. The runner that copies a conductor directory onto the
session machine is this change.

## What

- Register an rsync runner on `pi_tmux.STAGE_RUNNER` before `run_pi`
  calls `run_turn`.
- `rsync -a`. Add `--delete` only when that entry's `delete` is `true`.
- Local transport (empty SSH prefix): both paths are local. Remote
  transport: the prefix `run_turn` already passes, with the host as
  the destination of `dest`.
- The runner bounds itself with `timeout_sec` and returns non-zero on
  timeout, missing `src`, or a non-zero rsync. The hook then does not
  paste.
- Tests use a fake `rsync` on `PATH` or a local temp dir. They do not
  contact the dev VM.

## Impact

- Capabilities: ADDED on `remote-stage` (the copy runner). The hook
  requirements stay as folded.
- ADRs: none.

## User journey & surfaces

No new UI because the human still watches the named tmux session.
The copy finishes before that composer receives the paste.

1. **Working** — `src` is a directory on the conductor, `dest` is the
   path on the session machine, rsync exits 0, then the paste runs.
2. **Empty** — no `stage`. No rsync. Today's one-file prompt.
3. **Failed** — rsync exits non-zero or times out. No paste.
   Blocker `pi-stage-failed`.
4. **Off** — the pane is not idle, or the lock is held. rsync does
   not start.

## Out of scope

- `add-block-store-stage` and spike `block-store-identity`.
- Pulling files back from the VM.
- A live rsync onto `10.237.227.19` or the production hypervisor.
- A second Pi, Ctrl-C, or turning `INTENTION_CODEX_VIA_PI` on by default.
