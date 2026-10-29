# Independent take — astra-arch-review

1. Pin staging to the gap after run_turn's idle check and before write_prompt, inside run_pi's existing lock.
2. Pin packet-to-spawn propagation so a declared stage cannot disappear before execution.
3. Extend taskPacket's closed schema with an optional typed array; preserve validation of old packets and document fields in docs/contracts/.
4. Require explicit src and dest, boolean delete, and reject malformed declarations before any copy or paste.
5. Run entries in declaration order and stop on the first failure; never write the prompt or submit after that failure.
6. Treat a missing runner as pi-stage-failed, with enough detail to identify the failed entry and cause.
7. Preserve absent and empty stage behavior, dirty-composer refusal, opt-in routing, and the existing named session.
8. Refuse implicit destination selection, environment-controlled pruning, a second harness process, or Ctrl-C recovery.
9. Tradeoff: holding the session lock across copying delays other turns, but keeps staging and prompt submission one serialized operation; bound runner failure and timeout behavior.
10. Verify event order, lock scope, partial failure, schema compatibility, and failure-to-face mapping with focused fakes; leave transport implementation to the dependent change.
