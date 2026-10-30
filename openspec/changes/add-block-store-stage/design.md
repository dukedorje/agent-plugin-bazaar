# add-block-store-stage

## Look (2026-10-29)

Read-only on the dev guest `10.237.227.19` (VM `WyLPnVKfcozTNipLqz2LX3`)
and on its state file. Pi was not restarted. Nothing was written.

- Guest mounts: `/` is virtiofs tag `myfs`. `/secrets` is ext4 on
  `/dev/mapper/mjolnir-secrets` (16M of a 32M loop). No second
  virtiofs, no 9p, no NFS.
- `nullb0` is a 250G disk with no mountpoint (524288000 sectors).
  It is not a store the harness can read.
- State `spawn_config` has no `extra_mounts`.
- Mjolnir starts extra virtiofs shares only in `do_boot`, from
  `extra_mounts` on the VM config. The spawn API accepts
  `{tag, path}` and checks `allowed_mount_prefixes`. The default
  in `config/config.exs` is `[]`, which disables the API.
- There is no hot-add of a share onto a running guest in that boot
  path.
- `Mjolnir.LanFiles.install` copies a guest binary at boot for one
  selected VM. That is the Recrypt share's publisher, not a
  directory mounted for the harness.

## Closed hypothesis

- `block-store-identity`: a mounted path the harness can already
  read. No-go. The 2026-10-29 look found no such mount.

## Forks

- Store identity: decided. A host directory attached with virtiofs.
  See `steer.md`.
- Attach moment: decided. New guests at boot, via `extra_mounts`.
  The live Pi VM is not rebooted. The host prefix and tag belong
  to the later Mjolnir allowlist landing.
- Copy machine: decided. The session machine copies from the guest
  mount to the session tree. Readiness is that extra virtiofs mount,
  its root or a descendant, checked on the session machine before
  any copy or prune. An existing directory on the guest root is not
  that mount. `/` being virtiofs is not enough. A missing or unready
  mount fails the step and does not prune.
