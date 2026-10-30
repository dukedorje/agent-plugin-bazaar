# add-block-store-stage

> **ACTIVE BUILD**

**Rigor:** architecture

Activated 2026-10-29 by an explicit "activate" on this node, inside
the `stage-before-keys` grant. Steer on 2026-10-30 named the
store. Fresh advise is still owed before `act`.

## Preparation

- Upstream: living `remote-stage` at `e07a40c`, rsync runner at
  `2d4438c`, steer at `06f8e4c`. Hook returns on stage failure
  without deleting a prompt file already on disk.
- Outcome: `src` stays a conductor path. `store` is a path on the
  session machine, the guest mount of a virtiofs host directory.
  The session machine copies `store` to `dest`. A missing mount
  fails closed. Host prefix and tag stay in the Mjolnir allowlist
  landing. Authority is the same grant.

## Why

The stage hook and the rsync runner copy a conductor path onto the
session machine. The block store is a host directory the guest
sees only after virtiofs attaches it. That guest path is not a
conductor `src`. The 2026-10-29 look found no such mount on the
live Pi VM. New guests get the share at boot. This change copies
from the mount. It does not attach the mount.

## What

- Capability `remote-stage`.
- A stage entry names either conductor `src` or session `store`,
  plus `dest`. The session machine copies `store` to `dest` under
  the lock already held for the paste. Failure does not write a
  prompt and does not submit.
- The host prefix, the virtiofs tag, and hot-add stay outside this
  change. Hot-add is deferred bead `mjolnir-uull`.

## Impact

- Capabilities: MODIFIED `remote-stage` (declaration check and
  rsync runner), ADDED session store copy
- ADRs: none. The packet grows an optional `store` string on a
  stage entry. `src` stays the conductor path.

## User journey & surfaces

No new UI because the outcome still reaches the named Pi pane: idle
check, stage, then the one-line paste.

1. **Working** — the store step finishes, then the paste runs.
2. **Empty** — no store declaration. The rsync runner and the
   one-file prompt stay as they are.
3. **Failed** — the store step does not finish. The turn does not
   write a prompt and does not submit the paste. A prompt file
   already on the machine stays as it was.
4. **Off** — the pane is not idle, or the lock is held. The store
   step does not start.

## Out of scope

- The Recrypt LAN share (`lan-files`). A path is not that share's
  authorization subject.
- Restarting the live Pi session, or deploying Mjolnir, unless a
  later steer says so.
- A second Pi, a production-hypervisor sync, and turning
  `INTENTION_CODEX_VIA_PI` on by default.
- A live copy onto `10.237.227.19` as a test.
