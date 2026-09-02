# Design — demo

## Where it sits

```
intend → steer → change → advise → act → demo → fold
```

`demo` is a stage, not observe (`status` / `map`) and not a mailbox
face (EYES). EYES stays for look-owed checkboxes that are not this
verb. `/run` walking `next: demo` is `update-run-demo`, not this
slice.

## Three rings, one verb

| Ring | Audience | Slice one |
|---|---|---|
| internal | the human in this tab | **yes** — try the feature |
| mesoteric | staging | named only (`bazaar-spi.2`) |
| exoteric | production / the world | named only (`bazaar-spi.2`) |

A ring field on the packet or the skill (`--ring internal`) is
enough later. Do not grow three skills.

## What “try” means here

This kernel is verbs in a TUI, not a web app. Internal demo is a
**named journey** the human can run: a slash, a CLI, or the Next
command already used on EYES. Example: after `act` lands
`run-wave`, `/demo` points at `/run-wave` and waits for the human
to experience it. The agent does not check the box.

## Fold union

`add-run-wave-workflow` also MODIFIES packaging “One skill tree”
(adds `run-wave`). Fold of this change MUST union that list, not
last-writer-wins (`docs/LEARNINGS.md` 2026-09-02 batch fold).

## Not decided here

How staging/production attach to a host. Packet schema for `ring`.
Whether every act owes a demo (probably not — CLI-only nits may
skip).
