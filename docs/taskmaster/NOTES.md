# Taskmaster — speculative notes

Dated 2026-08-15. Not decisions. Promote a line into
[ARCHITECTURE.md](ARCHITECTURE.md) when Orient settles it. Delete or
date-stamp when it dies.

- **virtiofs** — doubt it is the right persistence path for the DB.
  Mjolnir’s LUKS-backed volumes feel closer to “a drive the instance
  owns.” Need a spike before we bet the write log on virtiofs.
- **Write pool** — “thread pool of open connections that linearize” is
  the instinct, not a library choice. libsql may already serialize;
  measure before wrapping.
- **IdentiKey hop** — login interface incomplete. Relevant soon. Do not
  build a second auth just to keep moving; park the auth node and walk
  over.
- **Dogfood the methodology** — splitting Taskmaster’s own work should
  look like using Taskmaster. First useful slice is a hosted ready-set
  (nodes + assignments + evidence), not a generic ticket tracker.
- **Playground** — first site attempt is on Mjolnir box
  `0a0fa094-252f-47b7-b348-6e4624eac9ef` (512 MiB). Node is not
  installed. May need `--memory 2048` before SvelteKit will install.
- **Information ingestion** — bead `bazaar-ja7`. Sit down on how this
  project ingests knowledge: G Brain, MetaCoding, and/or Dreamballs.
  Do not invent a fourth store first.
