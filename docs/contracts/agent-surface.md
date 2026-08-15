# Agent surface

> **C1 · ACTIVE BUILD → folded 2026-08-14.**
> Weave of packet/result schema · topologies · identity.
> Reduce: **a group is an agent.**

Normative contract for every actor in this system. Skills, hosts, and later
VMs implement this. They do not grow a parallel RPC.

Companion faces (same change, different jobs):

- [`identity.md`](identity.md) — who signs
- [`topologies.md`](topologies.md) — how members are wired
- schemas in this directory — machine shape

If prose and schema disagree, **schema wins** for structure, **this file wins**
for laws the schema cannot say (commit-on-red, no slash commands, promotion).

---

## The type

```
agent := identity + (task packet → signed result)
group := agent whose interior is a topology of agents
```

A human is an agent. A model in a harness is an agent. A group is an agent.
Later, a Mjolnir VM is an agent. The surface does not change. That is what
makes the graph composable.

If a proposed thing cannot accept a packet and sign a result, it is not an
agent and it is not a group. It is a document, a meeting, or a bigger prompt.

---

## Laws

These are not style. A skill that violates them is wrong, even if the JSON
validates.

1. **Packet in, result out.** The only interface. Foreign harnesses receive a
   packet. Never a slash command, never “run `/meta-execute`.”
2. **A group is an agent.** Same schemas. Interior topology is an
   implementation detail of that agent.
3. **Anchors, not bodies.** Packets name symbols and invariants. Workers
   re-anchor on live HEAD. Pasted file bodies go stale mid-flight.
4. **Commit-on-red.** An agent that edits and returns without committing the
   exact paths it touched has created unowned state. Verification gates
   *done*, not persistence. No backend exemption in the packet; fix the
   executor or route elsewhere.
5. **Focused verify is the acceptance surface.** The packet names one
   command, one journey, or one contrast. Suites are not task gates.
6. **Failure classes are closed.** `pass` · `task-red` · `baseline-red` ·
   `infra-red` · `blocked` · `parked`. Classify before acting. `baseline-red`
   completes the node. `task-red` repairs the implicated branch. Do not stop
   the graph for someone else's baseline.
7. **Self-verify does not promote.** A builder may check their work. Promotion
   needs a fresh reader, a live oracle, a discriminating contrast, or a human.
8. **Permission is on the packet, not the identity.** `read` / `write` /
   `sensitive`. A plan is not permission. Architecture and instrument nodes
   sit behind a `human-gate` until activated.
9. **Status lives in the file.** Packet, result, and agent records carry
   their own disposition and identity. Paths are not status.
10. **Schema is forward-compatible with a real key.** `stand-in` today, `key`
    later, same fields. Do not add `unsigned_result`.

---

## Task packet

The only thing an assignee is given.

| Field | Required | Why |
|---|---|---|
| `schema_version` | yes | `1.0` |
| `id` | yes | `pkt-…` |
| `node_id` | yes | Work-graph node this packet is for (`C1`, a bead id, …) |
| `capability` | **yes** at `change` · `architecture` · `instrument` | Living-spec id (`openspec/specs/<id>/`). Must name an existing spec or a change that ADDs it. Optional at `vibe` / `brief`. |
| `change_id` | no | In-flight change this node belongs to |
| `requester` | yes | Identity. Who asked, so the result can be addressed |
| `assignee` | yes | Identity. May be a group |
| `goal` | yes | What is true after that is not true now |
| `non_goals` | no | Commander’s non-goals for this node |
| `anchors` | yes (may be `[]` at vibe rigor) | `{symbol, invariant}` — not file bodies |
| `acceptance` | yes | See below |
| `out_of_scope` | yes (may be `[]`) | `{item, tracked_as}` |
| `constraints` | yes | `permission`, `paths`, `do_not` |
| `load_class` | yes | `structure-clear` · `intention-critical` · `ambiguous` |
| `rigor` | yes | `vibe` · `brief` · `change` · `architecture` · `instrument` |
| `inherited` | no | Facts from LEARNINGS.md that touch this node |
| `input_result_id` | no | Prior member result (pipeline, review-pair reader, some weaves) |
| `role` | no | Member role inside a group (`builder`, `reader`, `conductor`, …) |

### Acceptance

Exactly one `kind`:

| `kind` | Fields | Discriminates when |
|---|---|---|
| `command` | `command` — the exact focused command | Exit and output would differ if the claim were false |
| `journey` | `journey` — who, from which surface, working / empty / failed / off | A human (or a browser) can tell |
| `contrast` | `if_true`, `if_false` | The two observations cannot be identical |
| `none` | — | **Only** `vibe` rigor, restore-only, or `read` permission drafts |

`criteria` is an optional list of checkable outcomes. It does not replace
`kind`. If you cannot say how you would test it, it is not acceptance.

### Constraints

| Field | Values |
|---|---|
| `permission` | `read` · `write` · `sensitive` |
| `paths` | POSIX paths the assignee may write. Empty means read-only |
| `do_not` | Closed verbs the assignee must not do (`deploy`, `push`, `fold`, …) |

`sensitive` always implies a human member somewhere in the ancestor groups.

---

## Signed result

| Field | Required | Why |
|---|---|---|
| `schema_version` | yes | `1.0` |
| `id` | yes | `res-…` |
| `packet_id` | yes | The packet this answers |
| `signer` | yes | Identity of the agent that produced this |
| `topology` | if signer is a group | Which wiring produced it |
| `members` | if signer is a group | Identities that actually ran |
| `member_results` | if signer is a group | Interior `res-…` ids |
| `artifacts` | yes (may be `[]`) | `{path, role}` written or claimed |
| `evidence` | yes | Focused result, or why it could not run |
| `disposition` | yes | Closed set above |
| `promoted` | yes | `true` only if promotion rules pass |
| `activation` | no | Human-gate: `true` if this result activates a draft |
| `commit` | yes | `{sha, paths}` or `null` |
| `summary` | yes | One short paragraph. The deliverable, not “done” |
| `signature` | yes | See identity.md |

`commit` is `null` **only** when `artifacts` is empty (pure read, or blocked
before edit). Any non-empty write-set requires a sha and the exact paths.
A result with artifacts and `commit: null` is invalid.

### Evidence

| `kind` | Fields |
|---|---|
| `command` | `command`, `exit_code`, `output_tail` |
| `journey` | `journey`, `note` |
| `contrast` | `if_true`, `if_false`, `observed` |
| `none` | `note` — why there was no focused check |

A `pass` with `evidence.kind: none` is valid only when the packet's
`acceptance.kind` was `none`. Otherwise the result is invalid.

---

## Agent record

On disk, `groups/<id>/surface.json` (and solo agents that opt into the
directory form):

| Field | Required |
|---|---|
| `schema_version` | yes (`1.0`) |
| `identity` | yes |
| `topology` | yes (`solo` for a non-group) |
| `members` | yes (`[identity]` for solo) |
| `reduce` | yes | One sentence: how interior results become one result |
| `parameters` | no | Topology-specific (`k` for quorum, order for pipeline) |

There is no `type: group` flag. `identity.kind == "group"` or
`topology != "solo"` is the group. Solo is the degenerate group so assignment
is one operation.

---

## Assignment (who gets the packet)

A function of `shape × load class × permission`, not who is logged in.
The work ladder (cheap model / Grok / Codex / native / human / group) lives
with `act`. This contract only requires:

- `ambiguous` → a human is in the assignee group
- `sensitive` → a human is in the assignee group
- `architecture` or `instrument` write → `human-gate` until activated
- complementary pieces → `weave` (default), not a bigger prompt
- contested expensive pieces → `fork` only under the fork rules
- foreign harness → packet, never a host command

---

## Versioning

`schema_version: "1.0"` is this file. Additive optional fields may appear
without a bump if old readers can ignore them. Removing or reinterpreting a
required field is an architecture amendment (new ADR, this file updated, old
text kept as trail).

C2 requires `capability` at `change` · `architecture` · `instrument`. Additive. The id is the directory name under `openspec/specs/`.

---

## Out of scope (C1)

- Living-spec directory layout (C2)
- Packaging: new skill tree vs MetaDev (F1)
- The five skills themselves (S1–S4)
- Harness adapters (H1)
- Hygiene enforcement (G1)
- Real keys, VMs, hosting (P1)

Those cite this surface. They do not redefine it.
