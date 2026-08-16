# design — where a host gets its edges

Cross-cutting (kernel ↔ host) and genuinely ambiguous at Orient: four
transports survived. Recording the rejected ones so the next host does not
relitigate this.

## The constraint that eliminates most of it

`openspec/specs/taskmaster` forbids a second object model: *"Taskmaster SHALL
NOT define a second object model for actors, packets, or results."* Any
transport that ends with the host owning authoritative work state is out,
however convenient it is at runtime.

The two forges are also not the same forge. The kernel is
`github.com/dukedorje/agent-plugin-bazaar` (private); the app is
`mimir.worldtree.network/Taskmaster/taskmaster-web` (private, self-hosted).
Anything that reads the kernel *at runtime* therefore needs a GitHub
credential on a public-facing guest — which is a new secret, a new trust
boundary, and a new way for `taskmaster.dev` to go down because a token
expired.

## Options

### (a) Exported snapshot, pulled at deploy — **CHOSEN**

`bd export` already emits JSONL with labels **and dependencies** — precisely
the edge set `readySet()` needs, no bespoke serializer. A step on the machine
that has both clones writes the snapshot into the app repo; the guest gets it
by the `git pull` it already does.

- No new service, no new runtime dependency, no credential on the guest.
- The guest never learns what `bd` is. The kernel stays the source of truth.
- Failure is at build time and visible, not at request time and silent.
- Cost: staleness between exports. **Mitigated by specifying that the page
  states its age** — which is the actual fix to the original defect. The bug
  was never "the data was old", it was "the page did not say so".

### (b) Live kernel endpoint — rejected

Kernel host serves ready-set JSON; the guest fetches per request.

Rejected because it buys freshness we have no demand for and charges a new
cross-repo interface for it: an ADR, Grok as independent reader, a service to
run and monitor, a GitHub credential on the guest, and a hard runtime
dependency that makes the public site fail when the kernel is unreachable.
This was the escalation trigger in `bazaar-lgr.11`; not taking it is what
keeps this change at `change` rigor.

Reconsider when someone genuinely wants the page live on a second screen. The
JSON contract below is deliberately transport-agnostic so that is a delivery
swap, not a rewrite.

### (c) `bd` replica on the guest — rejected

Most live, most moving parts, and it puts authoritative work state on the
host. That is the parallel kernel the `taskmaster` spec exists to prevent.
Rejected on the spec, not on cost.

### (d) Guest fetches the raw file from a forge — rejected

Superficially cheap: no service, just an HTTPS GET of the exported JSON from
GitHub. But the kernel repo is private, so it needs a GitHub token in managed
secrets, and it reintroduces every runtime-coupling problem of (b) while
pretending to be (a). If we are going to depend on the network at request
time, (b) is the honest version of it.

## The contract

Settled here so `bazaar-lgr.5` builds against something fixed.

```json
{
  "generated_at": "2026-08-16T16:40:00Z",
  "source": "bazaar",
  "nodes": [
    {
      "id": "bazaar-lgr.4",
      "title": "add-taskmaster-host — kernel ADR names the host",
      "kind": "node",
      "state": "open",
      "needs": ["bazaar-lgr.3"]
    }
  ]
}
```

- `state` is `open` | `landed`. Closed beads map to `landed`; everything else
  open. Deferred/parked beads are omitted, not shown as blocked.
- `needs` carries **only** ids present in `nodes`, so the host can never
  derive against a dangling edge.
- `generated_at` is required. A snapshot that cannot say when it was taken is
  not usable — the host renders empty rather than guessing.
- The host still derives: `readySet()` is unchanged and no `ready` field
  appears anywhere in this document.

## What we are betting

That freshness matters less than honesty. A ready set that is forty minutes
old and says so is useful; a ready set that is four hours old and looks live
is the defect we are fixing. If that bet turns out wrong, (b) is waiting and
the contract already fits it.
