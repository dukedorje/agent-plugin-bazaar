# update-campaign-inflight-accounting

> **ACTIVE BUILD**

## Why

The conductor currently treats every globally `in_progress` bead as a live
worker. Historical and unrelated project tracking therefore exhausts a
campaign's `max_inflight` allowance even when no worker holds an act lease.

## What

- Give each conducted campaign an explicit identifier derived from its pinned
  intention/root.
- Carry that identifier through `run` into conductor `ready`, `wave`, and
  `take`, and record it on held act leases.
- Count held leases for the current campaign when applying `max_inflight`.
- Keep write-set collision protection global across all held leases, regardless
  of campaign.
- Stop using bead `in_progress` status as evidence that a worker occupies a
  campaign slot.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: will amend `ARCHITECTURE.md`

## User journey & surfaces

No new UI because the outcome changes scheduling behind the existing `run`,
`act`, `ready`, and `run-wave` command surfaces.

## Preparation

- Inputs: `bazaar-658` goal, acceptance, and user-steered design; living
  `verbs` requirements; `conductor.py` dispatch/lease code; active
  `add-run-wave-workflow` contract.
- Dependencies: none.
- Outcome: still valid. The active run-wave change composes with this policy:
  disjointness remains global while free-slot accounting becomes campaign
  scoped.
- Authority: user explicitly activated `update-campaign-inflight-accounting`
  on 2026-09-27, bounded to the scope and out-of-scope above.
- Review: `reviews/2026-09-27-advise.md` accepted the current contract. Carry
  forward its implementation cautions: preserve empty-path fail-safe behavior,
  keep inventory lease input hermetic, and prevent concurrent same-campaign
  takes from oversubscribing the final slot. Contract unchanged.

## Out of scope

- Changing bead lifecycle statuses or cleaning historical `in_progress` beads.
- Weakening cross-campaign write-set exclusion.
- Changing `max_inflight` precedence or its default value.
- Implementing the remaining post-join honesty task in
  `add-run-wave-workflow`.
