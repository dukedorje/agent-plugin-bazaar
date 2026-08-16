# Tasks

Work **this** change owes. Building the export and wiring the page is
`bazaar-lgr.5` and is not owed here.

- [x] Decide the edge source; record the rejected options and why (`design.md`)
- [x] Fix the JSON contract so `bazaar-lgr.5` builds against something settled
- [x] Add the requirement to the `taskmaster` capability delta
- [x] Record the decision on `bazaar-lgr.11` and close it
- [x] Unblock `bazaar-lgr.5` and note the contract location in its design
- [x] Confirm `bazaar-lgr.12` is still worth shipping ahead of the export
      (it is — superseded only when the `as of` line exists, not duplicated)

Findings and handoffs:

- The escalation trigger in `bazaar-lgr.11` was option (b), a live endpoint.
  It was not taken, so no ADR and no Grok reader; rigor stayed `change`.
- `bd export` already emits labels and dependencies as JSONL, so the export
  step needs no bespoke serializer — only a projection to the contract shape.
- The two repos are on different forges (kernel on GitHub, app on Forgejo).
  Any runtime read of the kernel would need a GitHub credential on a
  public-facing guest. This is what killed option (d).
- `readySet()` in `src/lib/graph.ts` is unchanged by this decision. The seam
  held; only its input changes.
- Fold replaces the living `taskmaster` spec block wholesale — the ADDED
  requirement here is additive to that capability, not a rewrite of
  "Ready is derived, never stored".
