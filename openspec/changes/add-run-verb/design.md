# Design — run

## Slot

```
                /run  (campaign + policy)
                   │
   intend → change → advise → act → fold
   ready · brief sit beside the spine
```

`act` is one dispatchable node. `run` is zero or more stages until a
stop predicate. `run` does not replace `act`.

## Attention

Yin et al. (arXiv:2608.12610): resident descriptions decay across a
long session. `/run` therefore:

- keeps its own SKILL.md **thin** (policy + stop table)
- **Reads** `plugins/intention/skills/<stage>/SKILL.md` when it
  enters that stage
- does not paste intend/act/fold into `run/SKILL.md`
- earns one resident frontmatter slot; the other seven stay as they are

`@skills` / `.atskills` / hub are **not** this change.

## Policy

| Token | Means |
|---|---|
| `--until empty` | stop when nothing is dispatchable |
| `--until advise` | stop when the next owed step is a read |
| `--until activation` | stop on PENDING |
| `--until ask` | stop at the first ASK |
| `--until fold` | include remember |
| `--autonomous` | asleep: `--until empty`, consult-before-ask, punch-list; never deploy / never flip by-eye |
| `--pause-before <id>` | hard stop before that node |
| `--max-inflight N` | existing conductor cap |

Halting ≠ asking. Autonomous parks a veto subject and continues the
tree.

## Why not act --until

`act` already means one node + packet + verify. Overloading it hides
the campaign. Duke picked `/run`.

## Why not forty verbs

Headless adapters stay under `act` (`add-act-headless`). Guard stays
hooks. Unpark stays register + `intend`.
