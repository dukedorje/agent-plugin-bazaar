# Tasks

- [ ] Implement the exclusive `src` / `store` declaration and the
      session-side store copy under the existing session lock.
      Surfaces: the closed `stage` item in
      `docs/contracts/agent-surface.schema.json`, the `stage` row in
      `docs/contracts/agent-surface.md`, `validate_stage`,
      `spawn.py` `cmd_stage`, `run_turn` normalization, and the
      `run_pi` runner registration. A step that does not finish
      does not write the prompt and does not paste.
- [ ] Tests use a fake mount report or a local temp dir. They do
      not contact the dev VM. Cover store-only and mixed lists,
      both and neither selectors, a malformed later entry before
      any copy, absent and empty stage, legacy `src`, a ready extra
      mount, and an existing unattached directory with `delete`
      true that preserves dest and the prompt.

- Spike: block-store-identity a mounted path the harness can already read is no-go after the look. Decision: host directory via virtiofs; the session machine copies from the guest mount — skipped

## Owed from advise (2026-10-30, astra-arch-review)

- [x] Resolve the recorded store-identity spike/steer gate before act;
      record the selected store, protocol, execution machine, path semantics,
      readiness evidence, and provisioning boundary without guessing a store.
- [x] Reconcile the selected declaration and dispatch with the living
      remote-stage requirements and affected schema/validation/propagation;
      preserve legacy rsync semantics and specify focused fake/local checks
      for success, missing store, failure/timeout, malformed and absent stages.
- [x] Correct the delta and Failed journey to require no new prompt write
      or submit on stage failure; cover an unchanged pre-existing prompt file.
- [x] Obtain fresh advise on the resolved store contract and amended change
      before implementation; this send-back does not close the identity gate.
- [x] Fresh advise after preparation

## Owed from re-advise (2026-10-30, astra-arch-review)

- [x] Reconcile complete Stage declaration and Runner boundary MODIFIED
      blocks with exclusive src/store entries; preserve existing invariants
      and explicitly scope schema, agent-surface, validation, propagation,
      normalization, and runner registration updates plus focused mixed-list
      and malformed-declaration checks (re-advise finding 1).
- [x] Define session-side store-mount readiness and mount-root/descendant
      semantics before copy or prune; distinguish an unattached existing
      directory from the extra virtiofs store mount, including when the guest
      root is virtiofs. Specify fake checks for mounted success and unattached
      directory with delete true, preserving destination and prompt with no
      copy or paste on failure (re-advise finding 2).
