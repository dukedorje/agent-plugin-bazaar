# steer update-campaign-inflight-accounting

**When.** 2026-09-27
**Depth.** standard

## Decided

- Campaign scope source: explicit campaign id (user)
  Why: `run` can carry the pinned intention/root across harness boundaries;
  lease accounting need not depend on a local pin store or tracker ancestry.
- Collision boundary: global across held leases (auto)
  Why: campaign-local capacity must not permit overlapping writes between
  campaigns.

## Skipped

- None.

## Feeds change

Separate campaign membership, active act leases, and bead status. Scope worker
capacity to leases tagged with the explicit current campaign id, while retaining
global write-set exclusion across all held leases.
