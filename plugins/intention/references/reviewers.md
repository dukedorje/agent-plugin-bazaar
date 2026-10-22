# Architecture readers

Ladder priority is unchanged: `opus-arch-review`, then `astra-arch-review`,
then `grok-arch-review`. That list is the fallback order and the infra-red
handoff. It is not a rotation. `assign` still returns the first eligible
route. Gating advise uses `vary-reader`.

```bash
python3 <plugin>/scripts/ladder.py vary-reader \
  --permission write \
  --author-family <author> \
  --openspec openspec \
  --change-dir openspec/changes/<id> \
  [--blast high|schema|deletion|protocol|durability]
```

The author's vendor is skipped. Human `--who` / `--id` still wins.

- **High blast** (schema, deletion, protocol, durability, or the DAG calls
  the blast high) prefers Astra. If Astra is the author vendor, take the
  first remaining reader and say why.
- **Send-back** on this change returns to that review's `READER` when the
  route is still eligible. Do not rotate away from the reader who sent it
  back.
- **Otherwise rotate.** The next eligible reader after the latest accepting
  `READER` in `openspec/changes/` (archive included, this change excluded)
  is the pick. No prior accept starts at the first eligible reader.
  Astra on a high-blast accept counts as Astra's turn, so the next ordinary
  review moves on.

A fresh session after send-back is the same reader, not the next one.
Consult does not use this rotation and does not unblock `act`.
