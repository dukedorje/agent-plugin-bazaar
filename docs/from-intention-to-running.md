# From intention to a running system

Amended 2026-08-16 (`update-founding-doc-pointer`). This file is
**reasoning**. It is not living truth.

The method of working lives in
[`openspec/specs/working-method/spec.md`](../openspec/specs/working-method/spec.md).

| Want | Open |
|---|---|
| Loop, rigor dial, load class | `working-method` |
| Objects and the brief | `working-method` |
| Split rules, owed checkboxes | `working-method` |
| Packet in, result out | [`openspec/specs/agent-surface`](../openspec/specs/agent-surface/spec.md) · [`docs/contracts/`](contracts/) |
| Two-layer specs / changes | [`openspec/specs/living-specs`](../openspec/specs/living-specs/spec.md) |
| Default verbs | [`openspec/specs/default-loop`](../openspec/specs/default-loop/spec.md) |
| Why it is shaped this way | [`ARCHITECTURE.md`](../ARCHITECTURE.md) |
| Hard-won facts | [`LEARNINGS.md`](LEARNINGS.md) |
| Work graph | `bd ready` · `python3 scripts/ready.py` · `conductor.py ready` |

A `SHALL` only in this file is not a requirement. Name a change-id and
fold it.

The first use of the method on itself is the DAG below. Keep the trail.
Do not delete it.

---

## First DAG (trail)

Built 2026-08-14 through 2026-08-16. Status is history, not a second
ready-set.

```
I0  this document (commander’s intent)
 │
 ├── C1  agent surface + group contract          [folded 2026-08-14]
 ├── C2  living-spec layout                      [folded 2026-08-14]
 ├── F1  packaging Fork — Path A won             [folded 2026-08-14]
 │     Path B PARKED — ADR-003
 ├── S1–S4  intend / change / act / fold         [folded 2026-08-15]
 ├── H1  harness touch-ins                       [folded 2026-08-15]
 ├── G1  hygiene                                 [folded 2026-08-15]
 ├── D1  park-sprint-plan                        [folded 2026-08-15]
 ├── D2–D6  density, conductor, spawn, ladder    [folded 2026-08-15/16]
 ├── extract-working-method + loop/objects/split [folded 2026-08-16]
 ├── T1  taskmaster.dev                          [host ADR-006 · site live]
 │     next: live graph (T1b / bazaar-lgr.5)
 └── P1  Tatastu / intentional.agency / Mjolnir-the-product
       [parked — Duke unparks]
```

Lineage (Morphist, Tatastu/OpenSpec, MetaCoding, MetaDev, OODA) was
Observe for that DAG. It is not restated here.

---

## Later hosts

Named so the surface stays stable. Not a promise to build them here.

| Host | In this vocabulary |
|---|---|
| **taskmaster.dev** | Ready-set as a product. Sibling host (ADR-006). |
| **Tatastu** | Loop with humans in the room. |
| **intentional.agency** | Intentions with a public address. |
| **Mjolnir VMs** | Agents with real keys. Same surface. |

If a host needs a different object model, amend
`docs/contracts/agent-surface.md`. Do not grow a parallel kernel.
