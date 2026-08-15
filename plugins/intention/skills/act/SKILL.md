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

Read `docs/contracts/agent-surface.md` and `docs/contracts/topologies.md`.
The packet is the only interface.

## Procedure

1. Confirm the node is ready (inbound deps have committed artifacts) and,
   if rigor is `change` / `architecture` / `instrument` for a write, that
   it is activated.
2. Assign by shape × load class × permission. Complementary → weave.
   Foreign harness → packet, never `/intend` or `/meta-execute`.
3. Write a task packet (JSON matching
   `docs/contracts/agent-surface.schema.json` `$defs.taskPacket`). At
   `change`+ rigor, `capability` is required. Anchors, not file bodies.
4. Do the work on declared `constraints.paths` only.
5. **Commit-on-red.** If you edited, stage those exact paths and commit
   before returning, including on red. Never `git add -A`. Verification
   gates done, not persistence. Do not push unless you are the conductor
   and the user expects it.
6. Run **only** the packet's focused acceptance. Classify:
   `pass` · `task-red` · `baseline-red` · `infra-red` · `blocked` · `parked`.
7. Write a signed result (stand-in: `content_hash` + who). Groups include
   `topology`, `members`, `member_results`. `commit` is null only if
   `artifacts` is empty.
8. Self-check is not promotion. Do not mark a change folded. That is `fold`.

If the packet contradicts these laws, report both instructions. Do not
silently keep the narrower one.
