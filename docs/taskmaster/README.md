# Taskmaster notes moved

Product notes live in the sibling app (ADR-006), not this marketplace.

- Laptop: [`~/work/Taskmaster/taskmaster-web/docs/`](../../../Taskmaster/taskmaster-web/docs/README.md)
- Guest: `/taskmaster-web/docs/`
- Remote: `ssh://git@mimir.worldtree.network/Taskmaster/taskmaster-web.git`

| Moved file | New home |
|---|---|
| INTENT | `~/work/Taskmaster/taskmaster-web/docs/INTENT.md` |
| ARCHITECTURE | `~/work/Taskmaster/taskmaster-web/docs/ARCHITECTURE.md` |
| RELATED | `~/work/Taskmaster/taskmaster-web/docs/RELATED.md` |
| NOTES | `~/work/Taskmaster/taskmaster-web/docs/NOTES.md` |
| GHOST | `~/work/Taskmaster/taskmaster-web/docs/GHOST.md` |

Kernel SHALLs stay here: [ADR-006](../../ARCHITECTURE.md) and
[`openspec/specs/taskmaster/`](../../openspec/specs/taskmaster/spec.md).

Snapshot the app vendors at deploy:

```bash
python3 scripts/export-graph.py
# writes docs/taskmaster/graph.json
```

`generated_at` is required. There is no `ready` field. Copy that file
into the sibling app (`bazaar-lgr.5`).

The [ARCHITECTURE.md](ARCHITECTURE.md) file in this folder is a hop,
not the sketch.
