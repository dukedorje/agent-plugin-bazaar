# steer add-block-store-stage

**When.** 2026-10-29
**Depth.** standard

## Decided

- block-store-identity: Spike before act (user)
  Why: the look found no mounted store on the dev guest. The line
  stays open. `act` does not land a recipe until that line is `go`
  or `skipped`.
- Attach moment: new guests at boot (user)
  Why: Mjolnir already starts `extra_mounts` in `do_boot`. The live
  Pi VM stays up. The default allowlist is empty, so a later
  Mjolnir landing names an allowed prefix. This campaign does not
  reboot `WyLPnVKfcozTNipLqz2LX3`.

## Skipped

- None.

## Feeds change

The store is still unnamed. Do not add a packet field or a runner
for a guessed store. When a later decision names a host directory,
the share is boot-time `extra_mounts` on new guests, and the live
Pi session is not the attach target. A store step that does not
finish still must not paste.
