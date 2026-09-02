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
# isolate is PARKED (add-act-worktree-land). Wave children stay on HEAD.
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
# isolated (PARKED — add-act-worktree-land):
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

## Native host (Grok)

When the conductor tab has `spawn_subagent` / `workflow`, disjoint
`act` nodes go through `conductor.py wave` then `.grok/workflows/run-wave.rhai`.
Single Grok assignee: `spawn_subagent`. Claude/Codex: `spawn.py` below.

## Spawn

```bash
python3 plugins/intention/scripts/spawn.py stage --packet <packet.json>
python3 plugins/intention/scripts/spawn.py run --spec <spec.json>
python3 plugins/intention/scripts/spawn.py consult --shape architecture-review [--panel]
python3 plugins/intention/scripts/spawn.py oneshot --who terra
```

`stage` writes a unique `.spawns/<node>-<id>/` with `packet.json`,
`prompt.md`, and `spec.json`. Two stages never share a path. Missing
or empty prompt hard-fails before any adapter starts.

`surface` comes from the packet (`skill-host` / `packet-only`). Cloud
hosts keep `packet-only` and set `assignee.interface`. The exec
adapter is for tests and local commands. Live Codex/Grok/Claude CLIs
are not vendored — the spec is the handoff.

Live CLI adapters send the prompt on **stdin** and capture
**stdout**. The brief is never an argv token (ARG_MAX). Scratch
files (`.spawns/`) stay for staging, not as the message channel.

`run --adapter claude` is live `claude -p` with no prompt arg
(stdin). Model comes from the spec interface. Shared effort
(`low` / `medium` / `high`) maps to `--effort`. Packet-only adds
`--disable-slash-commands`. Override the binary with `CLAUDE_BIN`.

`run --adapter codex` is live `codex exec -` (stdin). Same effort
word maps to `-c model_reasoning_effort="…"`. Sandbox is
`read-only` for consult / empty write-set; `workspace-write`
when `permission: write` or `constraints.paths` includes a
`reviews/` dir — the reader writes their own review file.
Override the binary with `CODEX_BIN`. Stage picks this when the
assignee harness is `codex` and `codex` is on PATH.

`run --adapter grok` is live `grok --prompt-file` (headless). Grok
does **not** read piped stdin; the staged `prompt.md` is the brief
(no ARG_MAX). Model from the spec interface (`grok-4.6`). Shared
effort maps to `--effort`. `--output-format json`. Override the
binary with `GROK_BIN`.

`run --adapter openai` is the OpenAI HTTP API fallback for Sol
when there is no Codex CLI but `OPENAI_API_KEY` is set. The prompt
is the chat body, not argv. Packet-only. Never a slash.

`run` with no adapter prints `infra-red` / `adapter-none` and does
not pretend a worker ran. Timeout kills the process group and
classifies `stall` as `infra-red`.

`consult` is a second opinion with no intend node and no act
unblock. Default shape `architecture-review`. `--who fable,sol`
(nicknames or ids, several, ladder order). `--panel` is every
spawnable reader. `--id` is exact-id only. `--who` / `--panel` /
`--id` are mutually exclusive. Named unspawnable hard-fails;
`--panel` skips harnesses with no CLI. Prompt on stdin / `--goal`;
JSON opinions on stdout (`agree` / `caution` / `dissent`). Does
not write `openspec/changes/*/reviews/`. Use `advise` when a
change needs a gated accept.

`oneshot` is the worker twin: no intend node. Default shape
`known` (Terra, then Sonnet). `--who terra` / `--who sol`.
Stdin or `--goal`; JSON `results[]` on stdout.

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
python3 plugins/intention/scripts/ladder.py assign --shape architecture-review --not-harness grok
python3 plugins/intention/scripts/ladder.py assign --shape known --after terra-known
python3 plugins/intention/scripts/ladder.py panel --shape architecture-review
python3 plugins/intention/scripts/ladder.py assign --shape fold
```

Source: `plugins/intention/references/ladder.json`. Priority
(first available; `--after` handoff; `panel` fan-out): known →
Codex Terra then Sonnet 5. Implementation/thinking → Sol then Opus
5. Plan → Fable 5.1 then Sol. Architecture → Fable 5.1, Sol, Opus
4.8, Grok. Fold → Opus 5. Human pick always wins. Same-family
author uses `--not-harness <author>` and **spawns** — does not park.

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
