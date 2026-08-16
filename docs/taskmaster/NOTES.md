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
- **Playground** — live site VM is `8a878070-2da0-4f8a-8dc0-776f3e1cf7db`
  (2048 MiB, snapshot `taskmaster-web-predev`). `vite dev` on `:5173`,
  tmux `taskmaster`. HTTP `http://taskmaster.dev` is routed (gateway
  apex + Deploy.Registry app `taskmaster`). HTTPS needs a Cloudflare
  Origin CA PEM — Mjolnir ACME is worldtree-only. Same pattern as
  `startupcentral.build`. Corrections 2026-08-16: `vite dev` is
  systemd unit `taskmaster-dev.service` (logs via `journalctl -u`),
  **not** tmux — no tmux server is running. `bun` is not on PATH for
  `mj exec`; it lives at
  `/root/.local/share/mise/installs/bun/1.3.14/bin/bun`. HTTPS on
  `taskmaster.dev` is in fact answering, so the Origin CA note above
  may be stale — re-check before spending on it.
- **`/taskmaster-web` had no version control** until 2026-08-16.
  `git init` + first commit `8a8ee6f`, now pushed. **Resolved same
  day** — the app is no longer single-copy on a dev VM.
- **Forgejo remote (2026-08-16)** — `mimir.worldtree.network` is a
  Forgejo 15.0.0 co-located on the Mjolnir host (same box: public IP
  `45.76.77.97`, `forgejo web` on `:3000` behind the gateway).
  Remote is
  `ssh://git@mimir.worldtree.network/Taskmaster/taskmaster-web.git`,
  default branch `main`, repo **private**.
  - Forgejo has `START_SSH_SERVER = false`, so git-over-SSH rides the
    **host's own sshd on :22** as user `git`. Nothing special to open;
    the guest already had DNS + TCP 22 out.
  - The guest authenticates with a **repo-scoped deploy key** (write),
    not a key on Duke's account: `/root/.ssh/id_ed25519`, fingerprint
    `SHA256:xIpz3h4zqoabOnqzvL5/zv3xuChcg+1DmFAn1Nlw7DA`. Revoke by
    deleting deploy key id 2 on the repo; that severs this one guest
    and nothing else.
  - `known_hosts` is **pinned** to the host key read off the server
    (`SHA256:jrKhuXPC+bdbvV7Pico35yzPBN8ViNF50+UKwVyQ7HA`), so pushes
    run with `StrictHostKeyChecking=yes` rather than TOFU.
  - Adding a deploy key needs an admin API token; mint with
    `forgejo admin user generate-access-token -u duke --raw`, POST to
    `/api/v1/repos/{owner}/{repo}/keys`, then delete the row from
    `access_token` in `/var/lib/forgejo/data/forgejo.db` (sqlite3).
    Do not leave the token behind.
- **`$lib` is gone** in this SvelteKit (next). It errors at import
  analysis: use `#lib` (the `imports` map in `package.json`).
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
- **Phong / MetaDev** — voice was “Phong,” not Fong. Copy is
  `~/work/Projects/AI/meta-dev`. Bead `bazaar-zmq`. F1-path-b stays
  parked until Phong wants an overlay that consumes our packets.
