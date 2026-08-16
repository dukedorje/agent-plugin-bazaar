# Make taskmaster.dev in /taskmaster-web on the Mjolnir VM

Tracked as epic **bazaar-lgr**. This file is disposable; beads are the graph.

**Non-goals.** Storybook, Playwright/Chromium, snapshot deploy, IdentiKey login, kernel SHALLs, multi-instance SQLite, absorbing MetaDev or MetaCoding.

## Orient
- Load class: intention-critical
- Blast: host app on one guest, not the kernel
- Lifecycle: brief (highest *ready* node). Architecture exists as `add-taskmaster-host` and does not block the site
- Why: first public address for the work graph we already run

## DAG

### nod-dev-listen (`bazaar-lgr.1`)
- Goal: `vite dev` answers HTTP 200 on the guest
- Landing: brief `.omc/briefs/taskmaster-dev-listen.md`
- Rigor: brief
- Depends on: none
- Group: solo
- Activation: none
- Acceptance: guest curl `/` is 200; tmux `taskmaster`; `DATABASE_URL=file:local.db`

### nod-route (`bazaar-lgr.2`)
- Goal: `taskmaster.dev` (or a subdomain) hits that process
- Landing: brief
- Rigor: brief
- Depends on: nod-dev-listen
- Group: human-gate (DNS / gateway)
- Activation: needs human
- Acceptance: public hostname serves the same app as guest curl

### nod-first-page (`bazaar-lgr.3`)
- Goal: `/` is Taskmaster, not the Kit demo
- Landing: brief (edits live on the guest)
- Rigor: brief
- Depends on: nod-dev-listen
- Group: weave with nod-route (complementary)
- Activation: none after listen lands
- Acceptance: title + ready-set empty state or live query

### add-taskmaster-host (`bazaar-lgr.4`)
- Goal: kernel ADR names objects; app consumes the surface
- Landing: `add-taskmaster-host`
- Capability: taskmaster
- Rigor: architecture
- Depends on: none (does not block the site)
- Group: human-gate
- Activation: needs human
- Acceptance: ADR accepted; no SvelteKit SHALLs in this marketplace

## Ready-set
- `bazaar-lgr.1` nod-dev-listen
- `bazaar-lgr.4` add-taskmaster-host (architecture — do not write until activated)

## Needs activation
- `bazaar-lgr.4` architecture write
- `bazaar-lgr.2` DNS / gateway (after listen)

## Next
- `act` / implement `bazaar-lgr.1` from the existing brief
- `change add-taskmaster-host` only after you activate it
- Weave peers (not children): `bazaar-ja7`, `bazaar-zmq`
