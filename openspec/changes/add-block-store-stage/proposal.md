# add-block-store-stage

> **ACTIVE BUILD**

**Rigor:** architecture

Activated 2026-10-29 by an explicit "activate" on this node, inside
the `stage-before-keys` grant. The look below is recorded. Direction
is still a steer. `act` stays blocked while `block-store-identity`
is open.

## Why

The stage hook and the rsync runner copy a conductor path onto the
session machine. A block store connected to that machine is a
different source. On the dev guest that store is not a mounted path
today, so this node cannot reuse rsync until steer names the store.
Attaching one can be a Mjolnir change.

## What

- Capability `remote-stage`.
- One stage step whose source is the named store, under the lock
  already held for the paste. Failure does not paste.
- Mjolnir work, if steer wants a share attached, is a downstream
  landing in that repo. This change does not boot a VM.

## Impact

- Capabilities: MODIFIED `remote-stage`
- ADRs: none in this repo until steer adds a packet field

## User journey & surfaces

No new UI because the outcome still reaches the named Pi pane: idle
check, stage, then the one-line paste.

1. **Working** — the store step finishes, then the paste runs.
2. **Empty** — no store declaration. The rsync runner and the
   one-file prompt stay as they are.
3. **Failed** — the store step does not finish. No prompt file, no
   paste.
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
