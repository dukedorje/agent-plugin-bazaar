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

## Unverified hypotheses

- `block-store-identity`: the block store connected to the Pi VM is
  a mounted path the harness can read. Look says this guest has no
  such mount. Confidence low. Verification: not empirically tested
  as a store. Synthesis path: none.

## Forks

- Store identity: still open. Steer chose spike before act. See
  `steer.md`.
- Attach moment: decided. New guests at boot, via `extra_mounts`.
  The live Pi VM is not rebooted for this. The allowlist landing
  waits until the store has a name.
