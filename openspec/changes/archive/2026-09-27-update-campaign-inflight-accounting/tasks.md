# Tasks

- [x] Independent architecture advise accepts the campaign/lease boundary.
- [x] Thread explicit campaign identity through `run`, `act`, `run-wave`, and
      conductor `ready`, `wave`, and `take` calls.
- [x] Persist campaign identity in held leases and derive campaign slot usage
      from those leases rather than global bead status.
- [x] Preserve global lease-based write-set collision detection across
      campaigns, including legacy leases without campaign identity.
- [x] Add regression coverage for unrelated `in_progress` beads, same-campaign
      leases, status-without-lease, release, cross-campaign overlap, and
      agreement among `ready`, `wave`, and `take`.
- [x] Amend `ARCHITECTURE.md` with the campaign-capacity versus global-collision
      boundary.
- [x] Reconcile the active `add-run-wave-workflow` change before fold.
