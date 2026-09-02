---
name: run-wave
description: >
  One act fan-out: two or more wholly disjoint write nodes in parallel
  on HEAD. Use when asked to run-wave, /run-wave, fan out disjoint
  acts, or to look at a real two-node wave (EYES). Not the campaign
  (/run). Not a single node (/act).
user-invocable: true
argument-hint: "[<id> <id> …]"
---

# run-wave

You are the **wave conductor**. One fan-out, then stop. You do not
run the campaign. You do not fold. You do not check EYES boxes.

Load `../../references/shared.md` and `../../references/act-io.md`.

The rhai envelope is `plugins/intention/workflows/run-wave.rhai`
(also `.grok/workflows/run-wave.rhai` in this clone). Packet is the
brief. Worktrees are PARKED — stay on HEAD.

## Skip

`conductor.py wave` has fewer than two nodes → print the wave JSON,
say it is not a wave, stop. Use `/act` for one node. Do not invent
ids. Do not isolate.

## Procedure

1. **Pick.** If they named node ids, those are the candidates.
   Always run `python3 plugins/intention/scripts/conductor.py wave`
   and keep only ids that appear in `wave` (wholly disjoint owned
   packets). Unnamed: use the whole `wave` list. Fewer than two →
   Skip above.
2. **Packets.** Each node needs `groups/<id>/packet.json` with
   non-empty `constraints.paths`. Write + lint missing packets
   (`act-io.md`, `conductor.py lint-packet`) **before** take.
   Empty paths overlap everything — they cannot form a wave of two.
3. **Take.** `conductor.py take --node <id> --holder <this-host>`
   for every wave node. A child that takes again fails. If a take
   fails midway: `release` every node already taken, stop (infra-red).
4. **Launch.** Do **not** isolate. Do **not** use host
   `isolation_worktree`.

   | Host | How |
   |---|---|
   | This session has `workflow` | `workflow` `run-wave` with `args.nodes=[{id, packet}, …]` (`script_path` `plugins/intention/workflows/run-wave.rhai` if `name=` is untrusted) |
   | Grok, no workflow | `spawn_subagent` `general-purpose` per node, packet path in the prompt, in parallel |
   | Claude / Codex assignees | `spawn.py` per node |

   Child prompt: read `act/SKILL.md`, packet path, node id, already
   taken, stay on HEAD, only `constraints.paths`, focused verify,
   signed result, stop, do not fold. Do not restate the rest of
   `act`.
5. **Infra-red launch.** `release` every taken node. Stop.
6. **After join.** `git status --porcelain` on HEAD ⊆ union of the
   wave's `constraints.paths`. Stray dirt → park that node, do not
   persist the stray under a sibling. Then persist each node's
   paths **sequentially** on HEAD (`conductor.py persist --paths …`).
   Read `groups/<id>/results/*.json`, `classify`, close / repair /
   park, `release` on failure.
7. **Stop.** Print `{id, success}` per node. Do not fold. Do not
   check an EYES box. Handoff: `/status` if a look remains; `/run`
   for the campaign.

## Must not

- Isolate / `persist --worktree` / host `isolation_worktree`
- Slash a foreign worker
- Launch a one-node “wave”
- Replace `/run` with this skill
- Flip PENDING or a by-eye box
