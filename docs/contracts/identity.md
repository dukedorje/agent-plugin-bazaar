# Identity

Face 3 of C1. How an agent is named and how a result is attested.

This is not a user account system. It is the minimum a packet and a result
need so they can be addressed, nested, and later signed with a real key
without a schema break.

## An identity

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable kebab-case id. Unique within the project. Never recycled. |
| `kind` | yes | `human` · `model` · `group` · `vm` |
| `display_name` | no | For humans. Not used in hashes. |
| `harness` | yes | `grok` · `claude` · `codex` · `hermes` · `prime` · `human` · `none` · `other` |
| `interface` | no | Forward label for a host not in `harness` (`cursor-cloud`, `devin`, `mjolnir-vm`, …) |
| `signing` | yes | See below |

`kind: group` means this identity *is* an agent whose interior is a topology.
There is no separate “group id” type.

`kind: vm` is reserved for Mjolnir. Do not emit it until a VM is the signer.
`harness: none` is for groups (the group has no harness; members do) and for
purely on-disk stand-ins. `harness: other` plus `interface` is how a
cloud or future host appears without a schema bump. Do not add a `kind`
per vendor.

### Id prefixes (convention, not enforced)

| Prefix | Used for |
|---|---|
| `agt-` | a solo human or model |
| `grp-` | a group |
| `pkt-` | a task packet |
| `res-` | a signed result |
| `nod-` | a work-graph node (C1, S3, …) |

## Signing

Two modes. Same fields. The mode tells you which fields must be populated.

### `stand-in` (now)

| Field | Required | Meaning |
|---|---|---|
| `mode` | yes | `stand-in` |
| `stand_in_id` | yes | Usually equal to `identity.id` |
| `content_hash` | on results | `sha256:` + hex of the canonical payload (see Hash) |
| `signed_at` | on results | ISO-8601 UTC |
| `public_key` | no | omit |
| `algorithm` | no | omit |
| `bytes` | no | omit |

A stand-in signature **is** the content hash plus who claims it. It attests
attribution, not non-repudiation. That is enough for a repo. It is not enough
for a hosted agency. Do not pretend otherwise in the summary.

### `key` (later, same schema)

| Field | Required | Meaning |
|---|---|---|
| `mode` | yes | `key` |
| `public_key` | yes | Hex or multibase, matching `algorithm` |
| `algorithm` | yes | `ed25519` (v1; add algorithms by amendment, not by silent field) |
| `content_hash` | on results | same as stand-in |
| `signed_at` | on results | ISO-8601 UTC |
| `bytes` | on results | signature over `content_hash` |
| `stand_in_id` | no | omit, or keep as a readable alias |

Filling `bytes` does not add fields. Hosts that cannot verify a key treat
`content_hash` as the stand-in and record `key-unverified` in evidence, they
do not drop the result.

## Hash

`content_hash` covers the result object with `signature.bytes` removed (and
`signature.content_hash` itself removed — the hash cannot include itself).

Canonical form: UTF-8 JSON, RFC 8785 (JCS) if available; otherwise
`json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)`.
v1 examples in this repo use the `json.dumps` form. A host that implements
JCS must say so in the result evidence so hashes are not compared across
canonicalizers.

Hash input is the result, not the packet. The packet is identified by
`packet_id`. Tampering with the packet is a different node.

## On disk

```
groups/<id>/
  surface.json    # the agent record (identity + topology + members)
  packet.json     # what was asked
  results/        # one signed result per member, filename = member id
  reduced.json    # the group's signed result
```

Solo agents MAY write the same layout with one member, or write a single
`results/<id>.json` next to the packet. Groups MUST use the directory form
so interior results are not lost when the reduce signs.

Markdown siblings (`surface.md`, …) are projections for reading. JSON is
the object. If they disagree, JSON wins.

## What identity is not

- Not authentication to a harness. Harness auth stays in the harness.
- Not a permission grant. Permission is on the packet.
- Not a substitute for `LEARNINGS.md` or a living spec.
- Not recyclable. If a group dissolves, park the id. Mint a new one.
