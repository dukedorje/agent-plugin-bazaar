# add-remote-stage

> **ACTIVE BUILD**

**Rigor:** architecture

Activated 2026-10-29 by campaign authority on `stage-before-keys`
(user: "activate and /run --go"). Bounds: that intention's goals and
non-goals, and the steer already given — spike before act for the
block store, push a conductor tree onto the VM, prune only when the
packet says so. The grant covers this dependency-ready node. It does
not cover `add-rsync-before-keys` or `add-block-store-stage`.

## Preparation

- Upstream: bazaar `fa04623`. `plugins/intention/scripts/pi_tmux.py`
  `run_turn` checks the pane is idle, then `write_prompt` and `submit`.
  `plugins/intention/scripts/spawn.py` `run_pi` holds the session lock
  around that call. No living `remote-stage` spec. The harness spec is
  the skill-host matrix, not this pane. `docs/LEARNINGS.md` has no
  stage/rsync note.
- Anchors: idle return in `run_turn` before `write_prompt`; `try_lock`
  in `run_pi` before `run_turn`. Packet schema is
  `docs/contracts/agent-surface.schema.json` `taskPacket`
  (`additionalProperties: false`).
- Outcome: revised. Astra `astra-arch-review` sent the first contract
  back (`reviews/2026-10-29-advise.md`, spawn
  `add-remote-stage-advise-1793316007-39014-d83d590b`). The revision
  stays inside the grant: it names the runner's inputs, failure shape,
  order, timeout owner, and the checks that prove the face. It does
  not add a copy command or a block-store door. Fresh advise is owed.
- Authority: the utterance above. Tracker is the chat DAG. Bazaar `bd`
  has no database; do not invent a campaign store.
- Descendants stay unscaffolded until this contract is a usable
  artifact. `block-store-identity` is not a hypothesis of this node.

## Why

A named tmux harness can be told to work before the tree it needs is
on that machine. Keys (the paste) must wait until a declared stage
has finished. A stage that fails must not type. A turn that declares
nothing must stay the one-file prompt that `fa04623` already ships.

## What

- New capability `remote-stage`.
- Optional `stage` on the task packet and on the spawn spec: a list of
  `{src, dest, delete?}`. `src` is a path on the conductor machine.
  `dest` is a path on the machine that owns the named tmux session.
  `delete` defaults off. Only an explicit `true` on that step may prune.
- Order, under the lock already held by `run_pi`: idle check, then
  every stage step, then today's `write_prompt` and one-line paste.
- A non-zero step, or a declared stage with no runner yet, ends the
  turn without a paste. Face blocker `pi-stage-failed`.
- No `stage` key, or an empty list, keeps today's prompt path.
- `INTENTION_CODEX_VIA_PI` stays opt-in. One named session. No second
  harness process. No Ctrl-C.
- The copy command itself is `add-rsync-before-keys`, not this change.
  Until that runner exists, a declared stage fails closed.
- The runner is called in declaration order with the pane's existing
  transport and session name. It returns zero or non-zero and owns
  the pre-paste time bound (`timeout_sec`, default 600). Timeout and
  transport errors become `pi-stage-failed`. A malformed entry is
  that same failure, not a silent skip.

## Impact

- Capabilities: ADDED `remote-stage`. The packet schema gains an
  optional `stage` array; `openspec/specs/agent-surface/spec.md` stays
  a pointer (edit `docs/contracts/`, not a second field table).
- ADRs: none. This does not add a verb.

## User journey & surfaces

No new UI because the human already watches the named tmux session.
The stage finishes before that composer receives the one-line paste.

Duke, from a conductor that spawns adapter `pi`.

1. **Working** — the packet lists `src` and `dest`, every step exits 0,
   then the pane receives today's paste.
2. **Empty** — the packet has no `stage`. The pane behaves as it does
   at `fa04623`.
3. **Failed** — a step exits non-zero, or no runner is registered.
   The composer stays idle. The face is `pi-stage-failed`.
4. **Off** — the pane is not idle, or the lock is held. No stage
   command runs, and no paste, as today (`pi-session-not-idle`,
   `pi-session-locked`).

## Out of scope

- `add-rsync-before-keys` — the conductor→VM copy. Not scaffolded
  until this contract is usable.
- `add-block-store-stage` — a filesystem door that is not a dest path.
  Open spike `block-store-identity` (unverified, low, no synthesis).
  Spike before act. Not scaffolded. Not activated.
- A second Pi, a sync onto the production hypervisor, Ctrl-C into the
  session, a default `INTENTION_CODEX_VIA_PI`.
- Pulling a tree from the VM back to the conductor.
- Setting a PI WEB theme. Deploying Mjolnir.
