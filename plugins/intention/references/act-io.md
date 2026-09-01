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
python3 plugins/intention/scripts/conductor.py take --node <id> --holder sonnet-5
python3 plugins/intention/scripts/conductor.py release --node <id>
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

`run --adapter claude` is live `claude -p`. Model/effort come from
the spec interface (`sonnet-5` → `claude-sonnet-5` / low,
`opus-5` / medium, `fable-5` / high). Packet-only adds
`--disable-slash-commands`. Override the binary with `CLAUDE_BIN`.

`run` with no adapter prints `infra-red` / `adapter-none` and does
not pretend a worker ran. Timeout kills the process group and
classifies `stall` as `infra-red`.

## Foreign harness

Give them the staged prompt file or packet path. Never `/act`,
`/intend`, `/meta-execute`, or `/run`.

## Work ladder (assign)

Route by **task shape**. Explicit human pick always wins. Do not
restate the table — resolve it:

```bash
python3 plugins/intention/scripts/ladder.py assign --shape known
python3 plugins/intention/scripts/ladder.py assign --shape thinking
python3 plugins/intention/scripts/ladder.py assign --shape design
python3 plugins/intention/scripts/ladder.py assign --shape plan
python3 plugins/intention/scripts/ladder.py assign --shape architecture-review
python3 plugins/intention/scripts/ladder.py assign --shape fold
```

Source: `plugins/intention/references/ladder.json`. Known → Sonnet 5.
Thinking implementation → Opus 5. Design → Opus 5 low/medium +
designer skills. Plan consult → Fable 5. Real architecture →
review-pair whose reader is Grok (Sol only if `available`).
Fold → designated folder Opus 5 (`opus-5-fold`; Grok only if picked
or `grok-fold` is flipped available).

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

## Mutex (take)

`take` is how a worker gets the node. It is a **write-set mutex**,
not a second tracker:

1. Node must be `dispatchable` (deps closed, paths not overlapping
   in-flight, a free slot).
2. Status becomes `in_progress`. Holder is recorded.
3. A lease is written to `.spawns/leases/<node>.json`.
4. Live beads: `bd update --claim`.
5. A second take of the same node fails.
6. Overlapping paths on other nodes become `deferred`.
7. `release` returns the node to `open` and frees the slot.

How many background workers: `ladder.json` `max_inflight` (default
2). Override with `ACT_MAX_INFLIGHT=4` or
`conductor.py ready --max-inflight 4`. When full, extra ready nodes
are `capped`.

Do not copy `planctl`. Beads are the graph. `.omc/` is off.

## Verify before close

Focused `acceptance.command` must run **before** `bd close` or flipping
an owed checkbox. Self-check does not promote.
