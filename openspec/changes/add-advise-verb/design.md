# Design — advise

## Slot

```
intend → change → advise → act → fold
              ↖ amend ↙
```

`brief` and `ready` sit beside this, not on the write spine.

## Why not act

| | `act` | `advise` |
|---|---|---|
| Permission | write | read |
| Output | commit of product paths + signed build result | verdict + review file + signed advice result |
| `constraints.paths` | product write-set | `openspec/changes/<id>/reviews/` only |
| Gate | focused verify command | accept / accept-with-nits / send-back |
| Topology | conductor-workers | review-pair (reader + optional consult) |
| Banner | stays ACTIVE BUILD | stays ACTIVE BUILD |

Same-family review still cannot promote (ADR-005). Author of the
change must not be the sole `accept` reader.

## Procedure (skill)

1. Load `shared.md`. Target is a change-id (or packet with
   `capability` + `change_id`).
2. Refuse PENDING? No — a draft can be advised; verdict cannot
   unblock `act` until the banner is ACTIVE BUILD.
3. Refuse PARKED.
4. Assign: `ladder.py assign --shape architecture-review` (and
   `--shape plan` for Fable consult). Human pick wins.
5. Readers get a **packet**, `permission: read`. Foreign harnesses:
   packet-only, no slash.
6. Write `openspec/changes/<id>/reviews/<YYYY-MM-DD>-advise.md`.
7. Signed result: `disposition` maps accept → green,
   accept-with-nits → green with blockers listed as nits,
   send-back → task-red (owed boxes added, not infra).
8. Stop. Do not implement nits (`change` amends). Do not fold.

## ready.py

`needs-advise`: ACTIVE BUILD + rigor architecture/instrument + no
accepting advise result yet (or last advise is send-back).

`act` `conductor.py ready` SHALL NOT list implement nodes of that
change as `dispatchable` while `needs-advise` holds.

## First use

The 2026-08-16 mjolnir pass is the worked example, not the
implementation.
