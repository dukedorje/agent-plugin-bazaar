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
