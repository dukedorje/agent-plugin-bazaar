# Tasks

- [ ] After steer names the store, implement that one transport
      under the existing session lock. A step that does not finish
      does not write the prompt and does not paste.
- [ ] Tests use a fake store or a local temp dir. They do not
      contact the dev VM.

- Spike: `block-store-identity` a mounted path the harness can already read — no-go (look 2026-10-29). Decision: host directory via virtiofs; the session machine copies from the guest mount.

## Owed from advise (2026-10-30, astra-arch-review)

- [ ] Resolve the recorded store-identity spike/steer gate before act;
      record the selected store, protocol, execution machine, path semantics,
      readiness evidence, and provisioning boundary without guessing a store.
- [ ] Reconcile the selected declaration and dispatch with the living
      remote-stage requirements and affected schema/validation/propagation;
      preserve legacy rsync semantics and specify focused fake/local checks
      for success, missing store, failure/timeout, malformed and absent stages.
- [x] Correct the delta and Failed journey to require no new prompt write
      or submit on stage failure; cover an unchanged pre-existing prompt file.
- [ ] Obtain fresh advise on the resolved store contract and amended change
      before implementation; this send-back does not close the identity gate.
