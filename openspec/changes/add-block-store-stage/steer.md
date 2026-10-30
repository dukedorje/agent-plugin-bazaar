# steer add-block-store-stage

**When.** 2026-10-30
**Depth.** standard

## Decided

- block-store-identity: host directory via virtiofs (user)
  Why: the 2026-10-29 look found no mount the harness can already
  read. That claim is no-go. The store is a host directory attached
  with virtiofs. Protocol is virtiofs plus a path copy.
- Attach moment: new guests at boot (user, 2026-10-29)
  Why: `extra_mounts` already start in `do_boot`. The live Pi VM
  stays up. The allowlist is empty, so a later Mjolnir landing
  names an allowed prefix. This campaign does not reboot
  `WyLPnVKfcozTNipLqz2LX3`.
- Copy machine: the session machine (user)
  Why: the runner copies from the guest mount to the session tree.
  The conductor does not need the bytes on the Mac. A missing mount
  fails the step and does not paste.

## Skipped

- None.

## Feeds change

The old spike claim is closed no-go. The stage source is the guest
mount of a host directory, declared as a path on the session
machine. The session machine copies that path onto the session
tree before the paste. Do not invent the host prefix or the tag;
the Mjolnir allowlist landing names those. Do not hot-add, and do
not reboot the live Pi VM. A missing mount or a failed copy does
not write a prompt and does not submit. Fresh advise after this
contract is amended. `mjolnir-uull` stays deferred.
