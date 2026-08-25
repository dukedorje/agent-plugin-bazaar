# Shared vocabulary

Loaded by `intend`, `change`, `advise`, `act`, `fold`, `brief`, `debrief`, `map`, `ready`, and `run`. None of them restates
the agent surface. If this file and `docs/contracts/agent-surface.md`
disagree, the contract wins.

## Citations (read, do not paste)

| Need | File |
|---|---|
| Laws, packet, result | `docs/contracts/agent-surface.md` |
| Schema | `docs/contracts/agent-surface.schema.json` |
| Density, roles, persist, distilled | `docs/contracts/dispatch.md` |
| Identity / signing | `docs/contracts/identity.md` |
| Topologies | `docs/contracts/topologies.md` |
| Living-spec rules | `openspec/specs/living-specs/spec.md` |
| What is built | `openspec/specs/*/spec.md` |
| Learnings | `docs/LEARNINGS.md` |
| Why it is shaped this way | `ARCHITECTURE.md` |
| Harness matrix | `plugins/intention/references/harness.md` |
| Conductor ready-set / persist | `plugins/intention/scripts/conductor.py` |
| Spawn / prompt-file / stall | `plugins/intention/scripts/spawn.py` |
| Assignment ladder | `plugins/intention/references/ladder.json` |

## Verb boundaries

| Verb | Produces | Must not |
|---|---|---|
| `intend` | A DAG of nodes (change-id / brief / direct fix), rigor, groups, ready-set | Implement, write SHALLs, scaffold `docs/sprints/` |
| `change` | `openspec/changes/<id>/` with banner, journey, deltas | Implement (until ACTIVE), fold, archive |
| `advise` | Review file + verdict (`accept` / `accept-with-nits` / `send-back`) + signed read-result | Implement, fold, flip banner, sole-author accept |
| `act` | Edits + commit + signed result | Fold, flip living specs as “done”, slash-command a foreign harness |
| `fold` | Living spec updated + change archived | Implement leftover tasks, fold PENDING/PARKED |
| `map` | Intend-dag page with live status / wave / outcome | Implement, unpark, second store |
| `ready` | Ready-set + parked list | Implement, unpark |
| `brief` | Disposable one-pager | Become a story template |
| `debrief` | Expansion of a finished or failed unit; takeaways; feeds intend | Fold, implement, become a story template |
| `run` | Campaign card + waves until a stop predicate | Second packet schema; slash a foreign worker; inline other verb bodies |

## Skip a change

Direct fix, no `openspec/changes/`: restore intended behavior, typo,
formatting, comment, non-breaking pin, test for already-specced behavior.

## Rigor

| Rigor | Landing | Activation |
|---|---|---|
| `vibe` | direct fix or bead | none |
| `brief` | bead description + acceptance, or chat | none |
| `change` | `openspec/changes/<id>/` | human unless already granted write |
| `architecture` | change + ADR | human-gate |
| `instrument` | change + property-red | human-gate + independent reader |

Load class: `structure-clear` · `intention-critical` · `ambiguous`.
`ambiguous` and `sensitive` always include a human member.

## Groups (do not invent new ones)

`solo` · `weave` · `pipeline` · `fan-out` · `fork` · `review-pair` ·
`human-gate` · `conductor-workers` · `quorum`.

Default complementary form is `weave`. `fork` only when at least two of:
schema/auth/money/protocol blast; load `intention-critical` or `ambiguous`;
two designs survived Orient; cost of being wrong exceeds two short acts.

A group is an agent. Same packet, one signed result.

## Packets

At `change` · `architecture` · `instrument`, `capability` is required and
is a directory name under `openspec/specs/` (or an id the change is ADDing).
`python3 docs/contracts/validate.py` is the schema check.
