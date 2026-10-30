# Tasks

- [ ] After steer names the store, implement that one transport
      under the existing session lock. A step that does not finish
      does not write the prompt and does not paste.
- [ ] Tests use a fake store or a local temp dir. They do not
      contact the dev VM.

- Spike: `block-store-identity` the block store connected to the Pi VM is a mounted path the harness can read — unverified (low, no synthesis). The 2026-10-29 look found no such mount.
