# add-taskmaster-host

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

`taskmaster.dev` has been unparked since 2026-08-15 and has a full
stack sketch in `docs/taskmaster/`, but no accepted architecture. That
leaves two ways to be wrong at once: the SaaS drifts into this
marketplace and the kernel grows a web tier, or the sketch's volatile
parts (framework, adapter, dev-server exception, look tokens) get
promoted into living specs and start lying the moment they flip.

Both are closed by deciding one thing — Taskmaster is a **sibling
host** of the agent surface — and by keeping the stack out of
`openspec/`.

## What

- ADR-006 in `ARCHITECTURE.md`: sibling host, consumes ADR-001, ready
  is derived, stack is not kernel truth, capability lands at fold
- A stack-neutral delta for a new capability `taskmaster`
- `docs/taskmaster/ARCHITECTURE.md` restated as the amendable sketch of
  record, now anchored to an accepted ADR
- Founding doc T1 node updated: the host decision is made; the site is
  not built

## Impact

- Capabilities: ADDED `taskmaster` (materialized by fold, not by this
  proposal)
- ADRs: ADR-006
- Living specs: unchanged in this change. `openspec/specs/` gains no
  SvelteKit — now or after fold.

## User journey & surfaces

No new UI in this change, because the surface being decided is a
boundary, not a screen. The journeys are readers'.

- **Working** — someone asks "does the SaaS live in this repo?" They
  open `ARCHITECTURE.md`, find ADR-006 accepted, and stop asking. They
  follow the pointer to `docs/taskmaster/` for the stack.
- **Working** — someone greps `openspec/` for `SvelteKit` and gets
  nothing. The framework is a sketch fact, reachable in one hop from
  the ADR.
- **Empty** — `openspec/specs/taskmaster/` does not exist yet. That is
  correct: the capability is created by `fold`, and an empty living
  spec for an unbuilt site would be the lie ADR-002 forbids.
- **Failed** — a later change adds `ready` as a stored column, or
  copies the packet fields into a Taskmaster table. ADR-006 and the
  delta both name that a defect; the reviewer has a citation.
- **Off** — Duke re-parks T1. The ADR is amended in place with the
  reason, not deleted (`CONVENTIONS.md`).

When the site itself lands, its journeys (ready set, assignment,
evidence) belong to that build's own change, not this one.

## Out of scope

- Implementing or changing `/taskmaster-web`
- Guest vite port / DNS — `bazaar-lgr.1`, `bazaar-lgr.2`
- IdentiKey login, snapshot deploy, Storybook, Playwright
- MetaDev copy — `bazaar-zmq`. Overlay stays parked (ADR-003)
- Forking the agent surface, or absorbing MetaDev / MetaCoding
