# Design — campaign-scoped inflight accounting

## Separate the three states

The scheduler currently collapses three independent facts into bead status:

1. The pinned intention/root selects campaign membership and focus.
2. A held act lease says a worker is currently editing files.
3. Bead status tracks broader project progress.

Only the second fact consumes worker capacity. The first scopes that capacity;
the third does neither.

## Explicit campaign identity

`run` resolves the pinned intention/root and passes its stable identifier to
every conductor operation in the campaign. `take` copies that identifier into
the lease beside the node, holder, paths, and timestamp. `ready` and `wave`
use it to count held leases belonging to this campaign.

This avoids coupling scheduling to a harness-local session-pin file and avoids
walking tracker ancestry on every conductor call. It also works when a foreign
harness receives a packet because campaign identity is explicit at the command
boundary.

## Capacity is scoped; collision safety is global

For a campaign with identifier C, free capacity is the configured cap minus
the number of held leases tagged C. An unrelated held lease does not consume
C's capacity.

Collision detection still compares candidate paths against every held lease.
Two campaigns can use their own worker allowances concurrently, but they
cannot receive overlapping write ownership.

## Compatibility

Bead status remains useful for graph readiness and duplicate-take rejection,
but it is not the lease registry. Legacy lease records without a campaign
identifier remain visible to global collision safety; they do not silently
consume a named campaign's slots. Commands that schedule new work must carry a
campaign identifier rather than falling back to global bead counts.

The active `add-run-wave-workflow` change still chooses a disjoint subset
before applying available capacity. This change only corrects how that
available capacity and the in-flight path set are derived.
