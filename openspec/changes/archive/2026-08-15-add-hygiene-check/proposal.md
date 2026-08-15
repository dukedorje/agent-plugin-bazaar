# add-hygiene-check

> **ACTIVE BUILD** → folded and archived 2026-08-15 (G1).

## Why

C2 named the rules. Without a check they are decoration (Tatastu’s
archive-debt lesson). G1 is the instrument: property-reds with
discriminating fixtures.

## What

`scripts/check-hygiene.py` + fixtures + `test-hygiene.sh`. Wired into
`validate.sh`. Living spec `hygiene`. Review pair: independent reader
asks how to fake “folded.”

## User journey & surfaces

No new UI because the surface is `python3 scripts/check-hygiene.py` and
`./validate.sh`. Working: zero in-flight changes, or honest PENDING.
Empty: no openspec/. Failed: fold-debt or missing banner. Off: do not
commit a fully-checked change still in `changes/`.

## Out of scope

- Journey *quality* scoring
- Tatastu disposition encyclopedia / icebox / orphan routers
- D1 sprint-plan park
