# add-working-split

> **PENDING**

Depends on: `extract-working-method`.

## Why

Split rules keep the graph honest: one acceptance surface, real
edges, ready from artifacts, named landing change-ids. They live in
founding § Splitting intention and are only partly implied by
`conductor.py`.

## What

ADD the split rules onto `working-method`.

## Impact

- Capabilities: MODIFIED `working-method`
- ADRs: none

## User journey & surfaces

No new UI because the surfaces are `intend` and `conductor.py ready`.
Working: a node is ready when inbound artifacts exist. Empty: a
markdown second graph. Failed: a checkbox that can never close.
Off: leave PENDING.

## Out of scope

- Implementing conductor (already folded)
- Epic-as-dispatchable filter (separate if we want it)
