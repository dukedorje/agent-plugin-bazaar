# add-living-spec-layout

> **ACTIVE BUILD** → folded and archived 2026-08-14 (C2).

## Why

C1 defined the agent surface. Packets at change rigor and above need a
capability id to cite. There was no tree that distinguished what **is**
built from what **should** change. Sprint folders are not that tree.

## What

OpenSpec-lite under `openspec/`: living specs, in-flight changes with
in-file disposition, fold+archive as done. Steal Tatastu’s two-layer truth.
Do not steal the disposition encyclopedia.

## Impact

- New capability: `living-specs`
- Pointer spec: `agent-surface` → `docs/contracts/`
- Additive C1 rule: `capability` required at change / architecture / instrument
- ADR-002 in `ARCHITECTURE.md`

## User journey & surfaces

No new UI because the surfaces are files agents and humans already open:
`openspec/specs/` (what is built) and `openspec/changes/*/proposal.md`
(disposition banner). Working: a stranger can tell current from in-flight.
Empty: `specs/` missing a capability they expected. Failed: a SHALL in
`changes/` cited as if it were built. Off: restore-only work never enters
this tree.

## Out of scope

- G1 hygiene automation (depends on this spec)
- Skill verbs S1–S4
- F1 packaging
- Icebox / DISPOSITIONS.md / `openspec` CLI as a required tool
