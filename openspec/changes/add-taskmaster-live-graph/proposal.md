# add-taskmaster-live-graph

> **PENDING**

## Why

`taskmaster` already SHALLs that a host derives ready from a **dated
export**, never from a live kernel, never from a seed. That contract
is folded. Nothing in this repo yet *emits* the snapshot
`bazaar-lgr.5` is supposed to vendor.

Until the kernel writes that file, the page either stays on a
hand-copied graph or ships empty. This change is the producer.

## What

- ADD: this marketplace SHALL emit the snapshot in the settled shape
  (`generated_at` required, no `ready` field, no dangling `needs`)
- A deterministic script + fixture so `bazaar-lgr.5` has a file to
  pull at deploy
- Cite the contract already decided in
  `openspec/changes/archive/2026-08-16-add-taskmaster-edge-source/design.md`

## Impact

- Capabilities: MODIFIED `taskmaster` (one ADDED requirement)
- ADRs: none (transport already decided; rigor stays `change`)

## User journey & surfaces

No new UI because the surface people see is `taskmaster.dev`, built
in `bazaar-lgr.5`. This change's surface is the export file.

- **Working** — a script in this repo writes a JSON snapshot whose
  `generated_at` is set and whose edges match `bd`.
- **Empty** — no open beads; `nodes` is `[]`, `generated_at` still set.
- **Failed** — a node depends on an omitted id; that edge is dropped,
  not exported dangling.
- **Off** — the guest is not involved; this never runs on the VM.

## Out of scope

- Wiring the SvelteKit page, `as of` line, empty-on-missing — `bazaar-lgr.5`
- Footer humility copy — `bazaar-lgr.12`
- Live endpoint / websockets — rejected in edge-source design
- A `ready` field in the JSON — forbidden by the living spec
- IdentiKey / per-user graphs
