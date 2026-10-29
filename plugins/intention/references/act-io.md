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
python3 plugins/intention/scripts/conductor.py ready --campaign <root-id>
python3 plugins/intention/scripts/conductor.py take --campaign <root-id> --node <id> --holder sonnet-known
python3 plugins/intention/scripts/conductor.py release --node <id>
python3 plugins/intention/scripts/conductor.py lint-packet <packet.json>
# isolate is PARKED (add-act-worktree-land). Wave children stay on HEAD.
python3 plugins/intention/scripts/conductor.py isolate --node <id>
python3 plugins/intention/scripts/conductor.py persist --paths <p> [<p> ...] -m "<msg>"
python3 plugins/intention/scripts/conductor.py classify <result.json>
python3 plugins/intention/scripts/conductor.py implicated --node <id>
```

`ready` is beads (or `--inventory`) minus closed/parked, minus nodes
whose paths overlap any globally held lease. Overlap → `deferred`.
Independent ready nodes stay `dispatchable`. Capacity counts only held
leases carrying the explicit current campaign id; bead `in_progress` and
other campaigns do not consume its slots. Inventory mode also requires an
explicit `--leases-dir` so tests cannot read the live registry.

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
`act` nodes go through `conductor.py wave --campaign <root-id>` then
`.grok/workflows/run-wave.rhai`.
Single Grok assignee: `spawn_subagent`. Claude/Codex: `spawn.py` below.

## Spawn

`spawn.py` lives in the **intention plugin** (`scripts/spawn.py` next
to `skills/`), not in the current repo. From a skill file:

```bash
python3 <this-skill-dir>/../../scripts/spawn.py stage --packet <packet.json>
python3 <this-skill-dir>/../../scripts/spawn.py run --spec <spec.json>
python3 <this-skill-dir>/scripts/consult.py \
  --shape architecture-review [--panel]
python3 <this-skill-dir>/../../scripts/spawn.py oneshot --who terra
```

Consult: use `skills/consult/scripts/consult.py` (finds `spawn.py`).
Do not `python3 plugins/intention/scripts/spawn.py` from cwd unless
this clone *is* the bazaar.

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
The child env drops `ANTHROPIC_API_KEY`, `CLAUDE_API_KEY`,
`ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, and `ANTHROPIC_MODEL*`
so Opus / Sonnet use the Claude Code subscription login
instead of billing the API (Grok injects those keys; a set key
wins over claude.ai login).

`run --adapter codex` is live `codex exec -` (stdin). Same effort
word maps to `-c model_reasoning_effort="…"`. Sandbox is
`read-only` for consult / empty write-set; `workspace-write`
when `permission: write` or `constraints.paths` includes a
`reviews/` dir — the reader writes their own review file.
An act write (permission write, not a review path) also sets
`sandbox_workspace_write.network_access=true`, so local Postgres
and other dev services answer. Advise and consult stay offline.
Override the binary with `CODEX_BIN`. Stage picks this when the
assignee harness is `codex` and `codex` is on PATH.

`run --adapter pi` is the shared Pi tmux session, not another farmed-out
process. `pi -p` and `pi --mode rpc` are still fresh processes. They can
stream, and they do not type into the session that is already on screen.

What a CLI harness actually has to provide here: a prompt on stdin (or a
file, for Grok), a process that exits, and a final text (stdout, JSON
`result`, or `last.md`). `run` does not read that stdout until the process
exits, so a streaming CLI is buffered into one blob. The exit code becomes
`pass` or `infra-red`. Timeout kills that process group.

The Pi pane has none of those. It is already running, Duke may be attached,
and Ctrl-C stops Pi. A facade that pretended to be `codex exec` would keep
the buffered-until-exit shape and throw away the live screen. The adapter
keeps the same ending contract (`face.json`, `last.md`) and, while it
waits, appends new pane text to `stream.log`. Callers that only parse the
final face stay as they are. Tail `stream.log` for the partials. The pane
itself is the other live view.

The prompt file is copied to the host (`PI_TMUX_PROMPT_PATH`, default
`/tmp/intention-pi-prompt.md`). tmux pastes one line that names that file,
then Enter. A packet is not typed as keys, because newlines in the composer
can submit early. One spawn holds `~/.intention/pi-tmux.lock`. A second
spawn, or a composer that is not empty, returns `infra-red` and sends
nothing. Timeout records `stall` and does not send Ctrl-C.

```bash
# This dev VM. Opt-in: without the last line, codex stays local codex exec.
PI_TMUX_SSH='ssh -o BatchMode=yes -o ConnectTimeout=15 -J root@45.76.77.97 root@10.237.227.19'
PI_TMUX_SESSION=pi
INTENTION_CODEX_VIA_PI=1
```

`PI_TMUX_LOCAL=1` is the same adapter against tmux on this machine.
Harness `pi` uses the adapter whenever `PI_TMUX_SSH` or `PI_TMUX_LOCAL=1`
is set. `INTENTION_CODEX_VIA_PI=1` sends ladder `codex` work to that same
pane. One pane, one turn.

Optional packet `stage` entries (`src`, `dest`, optional boolean `delete`)
are validated together and copied onto the spawn spec; an invalid declaration
is retained as `stage_error`. After the idle check, while the session lock
is held, `pi_tmux.STAGE_RUNNER(step, transport, session, timeout_sec)` runs
each entry in order before `write_prompt` and the one-line paste. `transport`
is the pane's SSH argv (empty for local tmux), `delete` defaults to false,
and the runner owns each invocation's spawn timeout (600 seconds if omitted).
The post-submit clock starts later. The first non-zero result, timeout,
launch/transport exception, malformed declaration, or non-empty stage with
no runner returns `pi-stage-failed` without writing the prompt or pasting;
the lock is released. Absent or empty stage preserves the existing turn.
The copy runner is supplied by `add-rsync-before-keys`.

`run --adapter grok` is live `grok --prompt-file` (headless). Grok
does **not** read piped stdin; the staged `prompt.md` is the brief
(no ARG_MAX). Model from the spec interface (`grok-4.7`). Shared
effort maps to `--effort`. `--output-format json`. Override the
binary with `GROK_BIN`.

`run --adapter openai` is the OpenAI HTTP API read-only fallback for OpenAI families
when there is no Codex CLI but `OPENAI_API_KEY` is set. It refuses write
packets, including advise review-file writes, before making an HTTP request. The prompt
is the chat body, not argv. Packet-only. Never a slash.

`run` with no adapter prints `infra-red` / `adapter-none` and does
not pretend a worker ran. Timeout kills the process group and
classifies `stall` as `infra-red`.

`consult` is a second opinion with no intend node and no act
unblock. Default shape `architecture-review`. `--who opus,astra,grok`
(nicknames or ids, several, ladder order). `--panel` is every
spawnable reader. `--id` is exact-id only. `--who` / `--panel` /
`--id` are mutually exclusive. Named unspawnable hard-fails;
`--panel` skips harnesses with no CLI. Prompt on stdin / `--goal`;
JSON opinions on stdout (`agree` / `caution` / `dissent`). Does
not write `openspec/changes/*/reviews/`. Use `advise` when a
change needs a gated accept.

`oneshot` is the worker twin: no intend node. Default shape
`known` (Sonnet, then Terra). `--who terra` / `--who sol`.
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
python3 plugins/intention/scripts/ladder.py assign --shape known --after sonnet-known
python3 plugins/intention/scripts/ladder.py panel --shape architecture-review
python3 plugins/intention/scripts/ladder.py assign --shape fold
```

Source: `plugins/intention/references/ladder.json`. Configured priority (`--after` handoff; `panel` fan-out): known → Sonnet
then Terra; implementation/thinking → Sol then Opus; plan → Opus then Astra;
architecture gating → `vary-reader` (Astra on high blast, else rotate; fallback list stays Opus then Astra then Grok); fold → Opus, optional Grok.
Concrete models and verification dates live only in the family registry.
Same-family author passes `--author-family <author>` (harness/family/vendor)
and **spawns** an executable different-vendor reader. Advise needs write
permission; API-only chat cannot write its review. Human pick always wins
with a warning for degraded health. See `routing.md` for runtime health,
credential epochs, and the two-hop fallback bound.

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
   any held lease, a free campaign slot).
2. Status becomes `in_progress`. Holder is recorded.
3. A lease with the explicit campaign id is written to
   `.spawns/leases/<node>.json`.
4. Live beads: `bd update --claim`.
5. A second take of the same node fails.
6. Overlapping paths on other nodes become `deferred`.
7. `release` returns the node to `open` and frees the slot.

How many background workers in one campaign: `ladder.json`
`max_inflight` (default 2). Override with `ACT_MAX_INFLIGHT=4` or
`conductor.py ready --campaign <root-id> --max-inflight 4`. Held leases for
that campaign consume the cap; all held leases retain global collision
ownership. When full, extra ready nodes are `capped`.

Do not copy `planctl`. Beads are the graph. `.omc/` is off.

## Verify before close

Focused `acceptance.command` must run **before** `bd close` or flipping
an owed checkbox. Self-check does not promote. On success,
`bd close --reason` is one line and the file list goes on `bd note`.
On a blocker, leave the bead open, label it blocked, and note the
type and detail. Do not close it by working around the blocker.
Detail: `plugins/intention/references/from-sprint-exec.md`.
