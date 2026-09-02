# Dispatch

Vocabulary for a conductor tree. Fields live on the packet and result
(`docs/contracts/agent-surface.md`). This file is how to set them.

A tree is `conductor-workers` (or a nest of groups). Six roles. Same
agent surface. Cloud / VM / future hosts are identities with an
`interface` label, not a new type.

---

## Roles

| Role | Job | Persist? |
|---|---|---|
| **Conductor** | Ready-set, assign, persist, graph write door. Reads **distilled** only. | Yes — top of this isolation boundary |
| **Worker** | Inlined packet. Edits `constraints.paths`. Returns raw + evidence. | No, if a conductor can |
| **Consultant** | Stronger model, nested, `explain` / `replan` only. No write handoff. | No |
| **Reader** | Review-pair. Writes nothing in the builder's paths. | No |
| **Human** | Activation, `ambiguous`, `sensitive`. A member, not an exception. | When they are the top of the tree |
| **Group** | Any topology that is itself an agent. One signed result. | The group's conductor / reduce |

Solo is a degenerate group: one worker, no interior conductor. That
worker *is* the isolation boundary and persists.

---

## Density

How much the packet *says*. Inverse of assignee capability.

| | `lean` | **`standard`** (default if absent) | `explicit` |
|---|---|---|---|
| Granularity | node-level | split only where layers fork | one write-set / file cluster |
| Sketches | contract / symbol only | sketch where ambiguous | verified sketch |
| Anchors | symbols + invariant | + callers / guards | full inventory |
| Verify | acceptance; worker may pick the command | one focused command | command + expected shape |

**Capability order is `lean` > `standard` > `explicit` — the inverse of
depth.** A lean packet expects the strongest worker and says the least.
Prescription a capable model does not need is context that competes
with the work.

| Density | Expected assignee (this project) |
|---|---|
| `lean` | Fable 5.1 (plan consult + arch buddy) · Grok 4.6 (cross-family review) · Sol if `OPENAI_API_KEY` |
| `standard` | Opus 5 (implementation / design, effort low–medium) |
| `explicit` | Sonnet 5 (known / mechanical coding) |

Assignment is **not** restated here. Resolve:

```bash
python3 plugins/intention/scripts/ladder.py assign --shape known
```

Source: `plugins/intention/references/ladder.json`. Claude Code is the
coding pool (high limits). Grok is the default architecture reader.
GPT-5.6 Sol is named but `available: false` until subscribed.

Blast **raises** density and never lowers it: schema/migration, auth,
crypto, money, cross-service contract → at least `standard`.

**Mismatch warns, never blocks.** `lean` on Flash: one line, then
proceed. Stronger worker + more explicit packet is always safe.

`intend` writes this field. `act` may warn. Neither invents a second
planner.

---

## Surface

How the assignee is addressed. Not the same as `identity.harness`.

| `surface` | Meaning |
|---|---|
| `skill-host` | Same Agent Skills / slash tree (Claude Code on DeepSeek, in-Grok `intend`) |
| `packet-only` | Foreign agent. Packet JSON only. Never a host command |

Grok as *this* session's skill host is `skill-host`. Grok spawned from
Claude via a headless runner is `packet-only`. Same binary, two roles.

Absent `surface` is unspecified. New packets from `act` set it.

---

## Interface

Optional `identity.interface`: a forward label (`cursor-cloud`,
`devin`, `mjolnir-vm`, …). Closed `harness` enum stays; unknown hosts
use `harness: other` plus `interface`. The surface does not grow a
kind for every vendor.

---

## Consult

A weaker assignee may call a **stronger** model without becoming that
model.

| Field | Meaning |
|---|---|
| `allowed` | default **true** when omitted |
| `purposes` | default `["explain", "replan"]` |
| `ceiling` | densest packet the consultant may receive (default `lean`) |

The write, the paths, and the signed result stay with the original
assignee. Consult is a nested read packet. It is not a reassignment
and not a fork.

A consultant packet is `permission: read` unless the conductor
explicitly reassigns.

---

## Persist at the boundary

Edits must be committed before the isolation boundary returns.
**Who** runs `git commit` is the top-level agent of that boundary.

- Worktrees are allowed isolation. Inside a worktree, the conductor
  commits if it can. Workers edit declared paths and stop.
- A cloud / VM agent that *is* the top of its tree persists itself.
- The signed result is written **after** persist. `artifacts` +
  `commit: null` is still invalid on a signed result.
- Never write “do not commit” into a packet. That line will be pasted
  onto a backend it was not meant for. Fix the executor or route.

Workers do not push. The conductor owns the remote if anyone does.

---

## Distilled face

The conductor's default read. Full report stays at `raw_ref`.

```
disposition · summary · verify_command · verify_exit ·
commit_sha · changed_files · blockers · raw_ref
```

Project with:

```bash
python3 plugins/intention/scripts/distill-result.py <result.json>
```

Open `raw_ref` only to investigate. Classification uses the face.
Promotion still needs a fresh reader, a live oracle, or a human.

---

## What this file is not

Not the scheduler. Ready-set, disjoint write-sets, isolate, persist,
and classify are `plugins/intention/scripts/conductor.py`. Unique
prompt-file, stall → infra-red, and surface-aware launch are
`plugins/intention/scripts/spawn.py`.
