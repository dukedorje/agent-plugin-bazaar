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
- **Playground** — first site is Mjolnir box
  `0a0fa094-252f-47b7-b348-6e4624eac9ef` (512 MiB), **dev server**,
  one SQLite file. Snapshot deploy later. May need `--memory 2048`
  before `bun install` / Playwright.
- **Information ingestion** — bead `bazaar-ja7`. Sit down on how this
  project ingests knowledge: G Brain, MetaCoding, and/or Dreamballs.
  Do not invent a fourth store first.
- **Storybook vs browser** — `sv create` died on Storybook:
  `Unable to find a usable package manager within NPM, PNPM, Yarn and Yarn 2`
  (`create-storybook` does not see bun). Scaffold at `/taskmaster-web` is
  partial: Kit + Tailwind + adapter-node + Vitest/Playwright landed;
  drizzle, libsql, better-auth, Storybook did not. Skip Storybook for
  now. Vitest already pulled Playwright — that is the agent-facing
  surface. Storybook is a human component workshop; add later from a
  machine that has npm, or not at all. 512 MiB will not hold Chromium.
- **Fong Meta Env** — our copy’s path is not on this machine under a
  name I could find. Bead `bazaar-zmq`. Paste the path into RELATED.md.
