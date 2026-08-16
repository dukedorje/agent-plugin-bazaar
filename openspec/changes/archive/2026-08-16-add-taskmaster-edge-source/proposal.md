# add-taskmaster-edge-source

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

`openspec/specs/taskmaster` already SHALLs that ready is derived, never
stored — and `src/lib/graph.ts` honours it: `readySet()` computes
`open ∧ all deps landed` from edges. The derivation was never the problem.
The problem is that the **edge set itself is a hand-copied fiction**, and a
correct derivation over invented edges is a confident wrong answer.

It has failed twice in one day. First `bazaar-lgr.3` sat at the top of READY
in signal colour for hours after it closed, while `bazaar-lgr.4` — genuinely
startable — was hidden under WAITING at 0.62 opacity. Then filing six beads
made the page stale again inside a minute: it says 3 startable, `bd` says 8.

So the open question is narrow and worth deciding once, because it sets
precedent for every future host: **where does a host legitimately obtain
kernel state?** This change answers that and specifies the answer. It does
not build it — `bazaar-lgr.5` does.

## What

- Choose the edge source: **an exported snapshot, pulled at deploy time**.
  Rejected options and why are recorded in [`design.md`](design.md).
- Specify the rule as a requirement on the `taskmaster` capability: a host
  sources edges from an export, does not depend on a live kernel service for
  its ready set, and **states the age of what it is showing**.
- Fix the JSON contract (shape + `generated_at`) so `bazaar-lgr.5` can build
  against something settled.

The staleness clause is the load-bearing part. It converts the failure mode
from *silently wrong* to *visibly N hours old*, which is the difference
between a product that is behind and a product that lies.

- Capabilities touched: `taskmaster`

## Impact

- Capabilities: MODIFIED `taskmaster` (one ADDED requirement)
- ADRs: **none.** The escalation trigger named in `bazaar-lgr.11` was
  option (b), a live kernel endpoint — that would have been a new cross-repo
  interface and would have required an ADR plus Grok as independent reader.
  Export needs neither: it introduces no service, no runtime coupling, and no
  new trust boundary. Rigor stays `change`.

## User journey & surfaces

Duke, arriving at `taskmaster.dev` mid-flight from a terminal, wanting to know
what to start.

- **Working** — the ready set matches `bd`, and a quiet line near the ledger
  says when the snapshot was taken.
- **Stale** — the snapshot is hours old; the same line says so plainly. The
  page is still useful and still honest, because it is not claiming currency
  it does not have.
- **Empty** — no ready nodes; the existing designed empty state already
  covers this ("that is a graph problem, not a work problem").
- **Failed** — the export file is missing or unparseable at build time. The
  guest must not render an invented graph: it renders the ledger empty with
  the reason, rather than falling back to a seed.
- **Off** — no JS: the page is server-rendered, so the ready set is present
  regardless.

The "as of" line is a new surface element. It is specified here and built in
`bazaar-lgr.5`.

## Out of scope

- Building the export or wiring the page to it — `bazaar-lgr.5`
  (`nod-live-graph`), which is blocked on this change and unblocks when it
  lands.
- Removing the footer's "this project's own work" claim in the interim —
  `bazaar-lgr.12` (`nod-stale-claim`), which ships today and is superseded
  once the `generated_at` line exists.
- Live push / websockets / sub-minute freshness. The upgrade path to a live
  transport is deliberately preserved: same JSON shape, different delivery.
  Revisit when someone actually wants the page open on a second screen.
- Per-user or authenticated graphs. Needs IdentiKey (A0), still a hop.
- Node / assignment / evidence tables in the host. `bazaar-lgr` epic.
