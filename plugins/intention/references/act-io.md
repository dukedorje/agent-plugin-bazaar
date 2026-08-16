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

## Commit-on-red

If you edited, before every return (green, red, blocked):

```bash
git add -- <only the paths in constraints.paths that you touched>
git commit --only -m "<conventional message>" -- <those same paths>
```

Never `git add -A`, `.`, or a directory. Never `commit -a`.
`commit` in the result is `{sha, paths}` or `null` (null only if
`artifacts` is empty).

Do not push unless you are the conductor and the user expects it.

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

## Foreign harness

Give them the packet path or inline JSON. Never `/act`, `/intend`, or
`/meta-execute`.

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

## Persist

Isolation MAY be a worktree. Inside it, **this conductor commits**.
Workers edit `constraints.paths` and stop. Do not put “do not commit”
in the packet. A cloud/VM worker that is the top of its own tree
persists itself. Signed result is written after persist.

## Claim is advisory

`bd assign` / `bd update --status in_progress` records who has the node.
A claim **never** blocks dispatch. Two writers collide on
`constraints.paths`, not on a second tracker.

Do not copy `planctl` (markdown plans + `~/.cache` SQLite). Beads are
the graph. `.omc/` is off.

## Verify before close

Focused `acceptance.command` must run **before** `bd close` or flipping
an owed checkbox. Self-check does not promote.
