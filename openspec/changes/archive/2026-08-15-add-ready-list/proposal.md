# add-ready-list

> **ACTIVE BUILD** → folded and archived 2026-08-15.

## Why

Need one command for ready/unblocked work and everything parked. Status
already lives in banners; this is a query, not a second tracker.

## What

`scripts/ready.py`, `openspec/parked.md`, skill `ready`.

## User journey & surfaces

No new UI because the surfaces are `python3 scripts/ready.py` and `/ready`.
Working: READY empty, PARKED lists P1 / sprint-plan / F1-path-b.
Empty: no in-flight changes. Failed: a parked item missing from both
banners and parked.md. Off: do not implement from the list.

## Out of scope

- Beads `bd ready` integration
- Unparking P1
