1. Pin the named store, its access protocol, and its location relative to the session machine before choosing a runner.
2. Pin an explicit distinction between conductor-local sources and session-machine store sources; existing src semantics must remain intact.
3. Pin who provisions and mounts the store; staging must not silently create infrastructure or select another host.
4. Pin the store-relative source and destination resolution rules, including what an unavailable store means.
5. Preserve whole-list validation, declaration order, first-failure stopping, and explicit per-entry delete authority.
6. Preserve the idle check and existing session lock around all staging and prompt submission, with no second harness or Ctrl-C.
7. Bound store access by timeout_sec and map missing sources, launch failures, transport failures, and timeouts to pi-stage-failed without paste.
8. Refuse a success result based only on an existing mount directory when the intended backing store may be absent.
9. Refuse hidden environment-selected sources, implicit destinations, or a new packet shape without matching validation and propagation contracts.
10. Tradeoff: a pre-mounted store keeps the staging runner small, but requires an explicit mount identity and readiness contract outside that runner.
