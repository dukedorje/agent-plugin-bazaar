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
**named journey** the human can run. Source of that journey: the
change's proposal `User journey & surfaces` and/or the Next command
on its owed boxes (inflight `openspec/changes/<id>/`, else
`openspec/changes/archive/*-<id>/`). Example: after `act` lands
`run-wave`, `/demo` points at `/run-wave` and waits for the human
to experience it. Residue is at most a bead comment or a signed
result with `permission: read`. No `demo.md`, no minted box, no
`demo` token in `EYES_RE`. The agent does not check the box.

## Fold gate

Slice-one demo is **not** a fold gate. The fold predicate stays the
single rule from `update-run-ooda`. Bare `/run` may fold first;
`/demo <id>` therefore resolves the archive. Not every act owes a
demo — `/demo` is opt-in; CLI-only nits may skip.

## Fold union

`add-run-wave-workflow` also MODIFIES packaging “One skill tree”
(adds `run-wave`). Fold of this change MUST union that list, not
last-writer-wins (`docs/LEARNINGS.md` 2026-09-02 batch fold). That
instruction lives here and in `tasks.md`, not in the packaging
SHALL.

## Not decided here

How staging/production attach to a host. Packet schema for `ring`.
