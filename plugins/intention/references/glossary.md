# Glossary of commands

Index of every Intention verb. Boundaries and laws live in
[`shared.md`](shared.md). If this page and
`docs/contracts/agent-surface.md` disagree, the contract wins.

Skill files: `plugins/intention/skills/<verb>/SKILL.md`.

## Loop

`intend` → `steer` → `change` → `advise` → `act` → `demo` → `fold`

`steer` is the default next after `intend`.

| Verb | Produces |
|---|---|
| [`intend`](../skills/intend/SKILL.md) | A DAG of nodes (change-id, brief, or direct fix), rigor, groups, ready-set, and a decision briefing. `--ask` presents the DAG and stops. “Activate this set” records campaign authority and pauses after contracts. “And run” records that grant and enters `run`. |
| [`steer`](../skills/steer/SKILL.md) | Decision briefing, then menus. Recommended option first, and skip is always a choice. Residue is bead design notes, plus `steer.md` when a change directory exists. |
| [`change`](../skills/change/SKILL.md) | `openspec/changes/<id>/` with banner, journey, and deltas. Reads steer residue. Scaffold only, until the change is ACTIVE. |
| [`advise`](../skills/advise/SKILL.md) | A review file written by a fresh other-family reader: `accept` or `send-back`, with `READER:`. Notes stay in the body. |
| [`act`](../skills/act/SKILL.md) | Edits, a commit, and a signed result for one ready node. |
| [`demo`](../skills/demo/SKILL.md) | The journey for a landed act, on the internal ring, then a halt. Residue is at most a bead comment or a read result. |
| [`fold`](../skills/fold/SKILL.md) | Living specs updated and the change archived. The designated folder is latest Opus (`--shape fold`). It may run in the background. |

## Around the loop

| Verb | Produces |
|---|---|
| [`brief`](../skills/brief/SKILL.md) | A disposable one-pager: goal, acceptance, contracts, gotchas, and out-of-scope. |
| [`debrief`](../skills/debrief/SKILL.md) | An expansion of a finished or failed unit. Takeaways feed the next `intend`. |
| [`map`](../skills/map/SKILL.md) | This tab’s intend DAG with live status. `map --current <id>` pins the session. `map <id>` peeks and leaves the pin. The pin is not in the repo. |
| [`status`](../skills/status/SKILL.md) | The board: READY, PENDING, ASK, EYES, PUNT, beads, parked. `--queue` is the open pile (unblocked leaves, then blocked). |
| [`ready`](../skills/ready/SKILL.md) | Alias of `status`. Same board, same script. Prefer `status`. |
| [`run`](../skills/run/SKILL.md) | A campaign: observe, then one sibling verb per wave, until a stop predicate. Two or more disjoint writes use the `run-wave` fan-out. `--autonomous` skips the steer pause. `--wait` is desk mode. `--tidy` folds. |
| [`run-wave`](../skills/run-wave/SKILL.md) | One disjoint `act` fan-out on HEAD. `run` already does this when a wave exists. |
| [`consult`](../skills/consult/SKILL.md) | Second opinions from architecture, plan, and thinking readers. Stdin in, JSON opinions out. No intend node, and no review file under the change. |
| [`setup`](../skills/setup/SKILL.md) | A repo ready for Intention: `bd`, the `node` issue type, the `openspec/` skeleton, scratch dirs gitignored, and an agent pointer. `--check` reports only. Once per repo. |

## Dispatch, no skill file

| Command | Produces |
|---|---|
| `oneshot` | One ladder worker and a JSON `results[]`, with no intend node. Default shape is `known`. `oneshot --who terra` names the route. Implemented as `python3 plugins/intention/scripts/spawn.py oneshot`. The worker twin of `consult`. |

## Say this

Phrase-to-command map: [plugin README](../README.md#say-this).

Between turns, the next command is a Jev choice over the legal transitions:
[jev-next.md](jev-next.md).
