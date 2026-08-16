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
  **Re-checked 2026-08-16 (`bazaar-lgr.2` closed):**
  `mj domain ls` → `10.204.71.168:5173` cert=yes http-01=yes.
  Public http/https and guest `:5173` are the same 56695-byte page
  (ETag `m4wxyu`). Origin CA not needed.
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
  - **Superseded 2026-08-16 (same day):** the key is no longer on the
    rootfs at all — see *Managed secrets* below. Deploy key id 2 was
    revoked; id 3 (`SHA256:DvXykS8VTJ5RxtraVy4q0FKjnZmZMBe4EHVzPuAWK2c`)
    is the live one and exists only inside managed secrets.
  - Adding a deploy key needs an admin API token; mint with
    `forgejo admin user generate-access-token -u duke --raw`, POST to
    `/api/v1/repos/{owner}/{repo}/keys`, then delete the row from
    `access_token` in `/var/lib/forgejo/data/forgejo.db` (sqlite3).
    Do not leave the token behind.
- **`$lib` is gone** in this SvelteKit (next). It errors at import
  analysis: use `#lib` (the `imports` map in `package.json`).
- **Managed secrets, live 2026-08-16.** Taskmaster now runs on VM
  `00473745-46d6-46fa-86c7-8b6fb688c46b` (`10.204.71.168`), spawned with
  `secrets_mode: :managed`. Six secrets (the five old `.env` vars plus
  the deploy key) live in a LUKS volume; `/run/mjolnir/secrets.env`
  (tmpfs, 0600) is rendered at boot and auto-sourced into every `exec`.
  **No plaintext secret is on the rootfs, so no snapshot can capture
  one.** Verified across two reboots. The predecessor VM `8a878070` is
  orphaned but still running — it still has the old `.env` on its
  rootfs, so destroy it rather than snapshot it.
  - `mj spawn` has **no** secrets flags. Use `POST /api/vms` with
    `{"secrets_mode":"managed","secrets":{...}}`; the Elixir-rpc dance
    in Mjolnir's Zine runbook is unnecessary.
  - Cutover is `Mjolnir.Deploy.Registry.put/2` over `mjolnir rpc` —
    there is no HTTP route that repoints an app at a different VM.
    `sudo` strips the sourced release env, so source `/etc/mjolnir/env`
    *inside* the privileged shell or rpc fails `:noconnection`.

- **`graph.ts` went stale within hours and the site lied.** On 2026-08-16
  it still showed `bazaar-lgr.3` as open after it was closed, so the page
  put finished work at the top of READY in signal colour and hid
  `bazaar-lgr.4` — genuinely startable — under WAITING. Corrected by
  hand, which is exactly the problem. **The one job is "what can I
  start"; a hand-synced graph cannot do that job.** Wire it to `bd` or
  drop the footer claim that it is this project's real work.
- **Dev-mode CSS goes stale under HMR.** A pushed `.css`/`<style>` change
  can be live in the SSR HTML and in the source while the browser still
  computes the old values — reloading, cache-busting and `cache:'reload'`
  all fail to fix it. `systemctl restart taskmaster-dev` does. Verify
  visual changes after a restart, not just a reload, or you will chase a
  cascade bug that does not exist.
- **Cutting an app over to a new VM takes TWO steps.**
  `Mjolnir.Deploy.Registry.put/2` updates the record and `mj domain ls`
  will happily show the new backend, but the gateway keeps serving the
  old one until `Mjolnir.Gateway.RouteReconciler.trigger()` runs. Worse,
  browsers that already hold an HTTP/2 connection stay pinned to the old
  upstream even after that — `cache: 'reload'` does not help, only a new
  connection does. Verify a cutover from a **fresh** connection, and
  ideally with content that differs between the two VMs; identical pages
  will show green while the route is still wrong.

### Three Mjolnir bugs found doing this (worth filing upstream)

1. **Managed secrets cannot work from `base_image: ubuntu-24.04`.**
   That image carries a **2026-06-23** agent with no `inject_secrets`
   handler, so the host's request fails to deserialize, the guest
   answers nothing, and the unlock dies as a bare 60s `:timeout`. The
   comment at `vm.ex:2075` already describes this happening to VM
   `2da0e442` — whose orphaned escrow entry is still on the host. Root
   cause: `MJOLNIR_GUEST_AGENT_BIN` is **commented out** in
   `/etc/mjolnir/env` *and* the path it names
   (`/opt/mjolnir/native/target/x86_64-unknown-linux-musl/release/mjolnir-agent`)
   does not exist, so `inject_guest_agent/1` silently no-ops on every
   spawn. **Workaround used:** spawn from snapshot
   `taskmaster-web-predev`, which carries a good Aug-16 agent
   (md5 `070e5c6af7743dbb51c04754dafd565e`). **Real fix:** put a current
   agent at that path and uncomment the var, or all future VMs stay
   stuck on a June agent.
2. **Secrets silently truncate at the first newline.** The store is
   line-based (`format!("{}={}", k, v)` joined by `\n`), so a PEM
   arrives as just `-----BEGIN OPENSSH PRIVATE KEY-----` (35 chars) with
   no error anywhere. Store multi-line values base64-encoded. This will
   bite anyone putting a TLS key or PEM in managed secrets.
3. **`mjolnir-secrets.target` activates ~3s before `secrets.env`
   exists.** The target tracks the LUKS *mount*, not the env render, so
   `After=`/`Requires=` on it is not enough — observed 07:23:52 target
   active, 07:23:53 unit ran and failed, 07:23:55.99 file appeared.
   Gate on the file with a systemd `.path` unit instead.
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
