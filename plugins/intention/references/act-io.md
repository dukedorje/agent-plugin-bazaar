# act I/O

## Where files go

Solo: put the packet and result on the bead (`bd note`) or in chat.
Do not write `.omc/`.

Group:

```
groups/<id>/surface.json
groups/<id>/packet.json
groups/<id>/results/<member-id>.json
groups/<id>/reduced.json
```

JSON must validate against `docs/contracts/agent-surface.schema.json`.
Examples live in `docs/contracts/examples/`.

## Conductor

```bash
python3 plugins/intention/scripts/conductor.py ready
python3 plugins/intention/scripts/conductor.py lint-packet <packet.json>
python3 plugins/intention/scripts/conductor.py isolate --node <id>
python3 plugins/intention/scripts/conductor.py persist --paths <p> [<p> ...] -m "<msg>"
python3 plugins/intention/scripts/conductor.py classify <result.json>
python3 plugins/intention/scripts/conductor.py implicated --node <id>
```

`ready` is beads (or `--inventory`) minus closed/parked, minus nodes
whose paths overlap an `in_progress` write-set. Overlap → `deferred`.
Independent ready nodes stay `dispatchable`.

## Persist

The conductor of the isolation boundary commits. Workers edit
`constraints.paths` and stop.

```bash
python3 plugins/intention/scripts/conductor.py persist --paths <only touched declared paths> -m "<conventional message>"
# isolated:
python3 plugins/intention/scripts/conductor.py persist --worktree .worktrees/<id> --paths … -m "…"
```

Never `git add -A`, `.`, or a directory. Never `commit -a`.
`commit` in the result is `{sha, paths}` or `null` (null only if
`artifacts` is empty). Signed result is written after persist.

Do not push unless you are the conductor and the user expects it.
Do not put “do not commit” in the packet. `do_not: ["push"]` is fine.

## Focused verify

Run **only** `acceptance.command` (or record the journey / contrast).
Once. Classify:

| Class | Meaning | Then |
|---|---|---|
| `pass` | focused check green | complete the node |
| `task-red` | failure caused by this node's paths | repair the branch |
| `baseline-red` | unchanged or outside declared paths | complete; do not "fix" |
| `infra-red` | runner/tool/env | retry once, then report |
| `blocked` | missing input, human, or decision | park the branch |
| `parked` | loser of a fork, or human reject | leave a revive condition |

Suites, project-wide typecheck, and builds are not task gates.

## Stand-in hash

```bash
python3 plugins/intention/scripts/content-hash.py <result.json>
```

Writes `signature.content_hash` (`sha256:` + hex) over the result with
`signature.content_hash` and `signature.bytes` removed.

## Spawn

```bash
python3 plugins/intention/scripts/spawn.py stage --packet <packet.json>
python3 plugins/intention/scripts/spawn.py run --spec <spec.json>
```

`stage` writes a unique `.spawns/<node>-<id>/` with `packet.json`,
`prompt.md`, and `spec.json`. Two stages never share a path. Missing
or empty prompt hard-fails before any adapter starts.

`surface` comes from the packet (`skill-host` / `packet-only`). Cloud
hosts keep `packet-only` and set `assignee.interface`. The exec
adapter is for tests and local commands. Live Codex/Grok/Claude CLIs
are not vendored — the spec is the handoff.

`run` with no adapter prints `infra-red` / `adapter-none` and does
not pretend a worker ran. Timeout kills the process group and
classifies `stall` as `infra-red`.

## Foreign harness

Give them the staged prompt file or packet path. Never `/act`,
`/intend`, or `/meta-execute`.

## Work ladder (assign)

Route by **task shape**, not by habit. Explicit human pick always wins.
Density, surface, consult, and persist: `docs/contracts/dispatch.md`.

| Shape | Default worker | Default density |
|---|---|---|
| Bounded mechanical edits | cheapest pooled backend | `explicit` |
| Multi-step implementation | Grok when the conductor is Claude; else the host’s strong worker | `standard` |
| Architecture / instrument / sensitive | human-gate + this harness | `standard` or deeper |
| Needs vision, slash, or tight back-and-forth | stay native | `lean` if the native model is strong |

A weaker worker may consult a stronger one for `explain` / `replan`.
That is not a write handoff.

Foreign harnesses get a **packet**, never a slash command. Do not vendor
MetaDev’s 40-command surface or `planctl/`.

## Distilled face

The conductor reads the distilled face, not the transcript.

```bash
python3 plugins/intention/scripts/distill-result.py <result.json>
```

Full report stays at `raw_ref`. Open it only to investigate.

## Claim is advisory

`bd assign` / `bd update --status in_progress` records who has the node.
A claim **never** blocks dispatch. Two writers collide on
`constraints.paths`, not on a second tracker.

Do not copy `planctl` (markdown plans + `~/.cache` SQLite). Beads are
the graph. `.omc/` is off.

## Verify before close

Focused `acceptance.command` must run **before** `bd close` or flipping
an owed checkbox. Self-check does not promote.
