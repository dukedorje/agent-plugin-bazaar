# Architecture readers

Opus (`opus-design`) writes the ordinary initial architecture. Fable 5.2
(`fable-design`, model `claude-fable-5-2`) drafts that architecture when
the blast is high, or when a human names Fable. The session driver, often
Grok, may edit the draft before advise. Pass the driver's family as
`--author-family`.

Fallback order is `astra-arch-review`, then `grok-arch-review`, then
`fable-arch-review`, then `opus-arch-review`. That list is the infra-red
handoff. It is not a rotation. `assign` still returns the first eligible
route. Gating advise uses `vary-reader`. Fable 5.1 is not a route and is
not an alias of Opus.

```bash
python3 <plugin>/scripts/ladder.py vary-reader \
  --permission write \
  --author-family <author> \
  --openspec openspec \
  --change-dir openspec/changes/<id> \
  [--blast high|schema|deletion|protocol|durability]
```

The author's vendor is skipped. Human `--who` / `--id` still wins.

- **Ordinary review** is Astra. A previous accept does not move the next
  review on. If Astra is the author vendor, take the first remaining
  reader that is not Fable (Grok, then Opus) and say why.
- **High blast** (schema, deletion, protocol, durability, or the DAG calls
  the blast high) is Fable 5.2. If Fable is not eligible, take the first
  remaining reader and say why.
- **Send-back** on this change returns to that review's `READER` when the
  route is still eligible. Do not switch away from the reader who sent it
  back.
- **Initial architecture** is Opus. Fable drafts it when the blast is high
  (`vary-reader --shape design --blast high`) or a human names Fable.
  Ordinary plan consult is Astra, then Opus. Fable takes a plan the same
  way (`vary-reader --shape plan --blast high`).

A fresh session after send-back is the same reader, not the next one.
Consult does not use this rotation and does not unblock `act`.
