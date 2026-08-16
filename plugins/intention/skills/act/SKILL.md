---
name: act
description: >
  Execute a ready work node: assign, emit a task packet, run focused verify,
  commit-on-red. Foreign harnesses get a packet, never a slash command. Use
  when implementing an activated change, a brief, or a ready-set node.
user-invocable: true
argument-hint: "<node-id or packet path>"
---

# act

Load `../../references/shared.md` and `../../references/act-io.md`.
The packet is the only interface. Schema:
`docs/contracts/agent-surface.schema.json`.

## Procedure

1. **Admit.** Node is ready (inbound artifacts committed). If rigor is
   `change` / `architecture` / `instrument` and this is a write, the
   change banner is `ACTIVE BUILD` (or the human just activated it).
2. **Assign.** Shape × load class × permission. Complementary → weave.
   Foreign harness → packet file, never a slash command.
3. **Write the packet** to the path in `act-io.md`. Validate with
   `python3 docs/contracts/validate.py` if you added an example, or by
   eye against `$defs.taskPacket`. `capability` required at change+.
   Anchors, not file bodies.
4. **Do the work** only on `constraints.paths`.
5. **Commit-on-red** as in `act-io.md`. Persistence ≠ acceptance.
6. **Focused verify** once. Classify with the closed set. `baseline-red`
   completes; do not fix the baseline.
7. **Write the result.** Groups: `topology`, `members`, `member_results`.
   Hash: `python3 plugins/intention/scripts/content-hash.py <result>`.
   Distill: `python3 plugins/intention/scripts/distill-result.py <result>`
   — conductor reads that face; `raw_ref` keeps the full report.
   Persist at the isolation boundary (`docs/contracts/dispatch.md`).
8. **Stop.** Do not fold. Self-check does not promote. Handoff: `fold`
   when the change's owed work has landed; `intend` if surprise splits
   a new node.

If the packet contradicts the laws in `docs/contracts/agent-surface.md`,
quote both instructions. Do not silently keep the narrower one.
