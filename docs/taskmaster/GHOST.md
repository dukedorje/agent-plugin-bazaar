# Ghost DAG — high-level intention across repos

Filed 2026-08-16. Not living specs. Not all of these are beads.
A **ghost** node is named so it cannot fall off the table. Promote
to a bead / change when it is time to act.

Sources: `INTENT.md`, `ARCHITECTURE.md`, `RELATED.md`, `NOTES.md`,
`docs/contracts/dispatch.md`, founding DAG (T1 / P1), beads
`bazaar-lgr` / `ja7` / `zmq` / `aw7`, parked register.

## ASCII

```
                    I0  intention kernel          [landed]
                    packets · verbs · openspec
                           │
           ┌───────────────┼───────────────────┐
           │               │                   │
           ▼               ▼                   ▼
      D0 dispatch     T1 taskmaster.dev    H0 Mjolnir fabric
      conductor ✅     SaaS / ready-set     we USE, P1 product parked
      runners   ○      bazaar-lgr
           │               │                   │
           │         ┌─────┴──────┐            │
           │         ▼            ▼            │
           │    T1a site ✅   T1b live graph ○ │
           │    / + systemd   node/edge schema │
           │         │            │            │
           │         ▼            ▼            │
           │    T1c groups ○  T1d VM-act ○─────┘
           │    assign/split  Playwright on guest
           │         │
           ▼         ▼
      A0 IdentiKey login ○ ──────── hop, do not fake an IdP
           │
           ├──────── M0 MetaCoding (CT on ASTs) ──── ja7
           ├──────── P0 Phong MetaDev copy ──────── zmq  (Path B parked)
           └──────── J0 ingest: G Brain / Dreamballs / M0
                      sit before a fourth store

      parked, not on this path:
      P1 Tatastu · intentional.agency · Mjolnir-the-product
      F1-path-b  MetaDev overlay
      sprint-plan factory
```

## Nodes (words)

| Ghost | State | Where it lives | Tracker |
|---|---|---|---|
| **I0** kernel | landed | this repo | living `openspec/specs/` |
| **D0** dispatch | conductor landed; spawn/stall **next** | `docs/contracts/dispatch.md` | `bazaar-aw7` |
| **T1** Taskmaster | site live; epic open | guest `/taskmaster-web` + Forgejo | `bazaar-lgr` |
| **T1a** public `/` | landed | `taskmaster.dev` systemd `:5173` | `lgr.1` `lgr.3` |
| **T1b** live graph | ghost | `graph.ts` seam: `readySet()` | no bead yet |
| **T1c** groups assign/split | ghost | INTENT objects | no bead yet |
| **T1d** VM actions / Playwright | later | ARCHITECTURE | no bead yet |
| **H0** Mjolnir fabric | in use | `~/work/IdentiKey/mjolnir` | P1 = product parked |
| **A0** IdentiKey login | hop | IdentiKey team | ARCHITECTURE open |
| **M0** MetaCoding / CT-AST | peer | `~/work/WorldTree/MetaCoding` | via `ja7` |
| **P0** MetaDev copy | bazaar steal landed 2026-08-16; overlay parked; further work is the meta-dev repo | `~/work/Projects/AI/meta-dev` | `bazaar-zmq` closed |
| **J0** ingestion | Orient only | G Brain · Dreamballs · M0 | `bazaar-ja7` |

Edges that matter: **T1 consumes I0** (do not fork the surface). **D0 is how I0 runs long agents** (not how T1 renders). **J0 feeds T1 and I0** after a sit-down, not a fourth store. **A0 blocks logged-in SaaS**, not the public ready-set. **T1d needs H0** (the box is the action surface). **P0 must not be absorbed** into T1.

## Filed vs only-said

**Written:** commander’s intent, stack (SvelteKit, one SQLite, one VM, libsql), actions=guest, ready derived, Terminal Graphite, weave table, Path B parked, P1 parked, ingestion reminder, MetaDev steal (ladder/claim, no planctl), conductor, Forgejo remote, HTTP-01 certs, `mj domain` / registry.

**Ghost only (said, no bead):** live graph schema (T1b), groups as product (T1c), Playwright-in-VM (T1d).

**Stale ink:** `bazaar-lgr.2` still “in progress / need Origin CA” — HTTPS is Let’s Encrypt and the route is live. Close it when you next look.
