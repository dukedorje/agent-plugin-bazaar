# add-advise-verb

> **PENDING**

## Why

The loop has a hole between `change` and `act`. An architecture write
can be ACTIVE BUILD, implementation must not start, and someone still
has to **read**. Today that pass is improvised (Fable + Sol + a
markdown file). It is not `act` (no product write-set), not `brief`
(not disposable), not `fold` (behavior is not built).

## What

- Add verb **`advise`**: read-only review-pair on an in-flight change.
- Verdict: `accept` | `accept-with-nits` | `send-back`.
- Artifact: `openspec/changes/<id>/reviews/<date>-advise.md` plus a
  signed result (`permission: read`).
- `send-back` adds owed boxes on the change; does not flip the banner.
- `accept` unblocks `act` on that change's implement nodes.
- Ladder: architecture-review → Grok (default), GPT-5.6 Sol when
  `available`; plan consult → Fable. Human pick wins.
- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`.

## Impact

- Capabilities: MODIFIED `verbs`, `default-loop`, `packaging`
- ADRs: will amend `ARCHITECTURE.md` (loop table) when this folds
- `ready.py` grows a `needs-advise` face (implementation task)

## User journey & surfaces

Duke (or a conductor), from chat, on an ACTIVE BUILD architecture
change.

1. Says `advise add-buzz-local-client` (or `/advise <id>`).
2. Skill loads proposal, design, deltas, cited code.
3. Assigns reader + optional consult from the ladder.
4. Writes `reviews/<date>-advise.md` and a signed read-result.
5. **Today: off** — the pass exists only as a one-off in mjolnir
   (`reviews/2026-08-16-advise.md`).
6. After send-back, `act` stays blocked; after accept, `act` may run.

`No new UI because` the surfaces are `openspec/changes/*/proposal.md`
and `openspec/changes/*/reviews/`.

## Out of scope

- Implementing mailbox / Buzz deploy (mjolnir)
- Promoting Sol to default reader (stays `available` flag)
- Morphist `critic` as a second catalog name — `advise` is that slot
- Changing packet schema laws (reuse existing result + `permission: read`)
