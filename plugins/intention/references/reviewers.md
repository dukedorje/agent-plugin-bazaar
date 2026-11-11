# Architecture readers

Fable 5.2 (`fable-design`, model `claude-fable-5-2`) writes the initial
architecture. Opus is the design fallback when Fable is not executable.
The session driver, often Grok, may edit that draft before advise. Pass
the driver's family as `--author-family`, so a Grok edit keeps Fable
eligible as a reader.

Fallback order is `fable-arch-review`, then `astra-arch-review`, then
`opus-arch-review`, then `grok-arch-review`. `assign` still returns the
first eligible route. Gating advise uses `vary-reader`, which rotates
Fable and Astra when either is eligible and uses Opus or Grok only when
that pair is not. Fable 5.1 is not a route and is not an alias of Opus.

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
- **Otherwise rotate** Fable 5.2 and Astra. The next of that pair after
  the latest accepting `READER` is the pick. No prior accept starts at
  Fable when the author is not Anthropic, otherwise the first remaining
  reader. Opus and Grok enter only when neither Fable nor Astra is
  eligible. Astra on a high-blast accept counts as Astra's turn, so the
  next ordinary review moves on.

A fresh session after send-back is the same reader, not the next one.
Consult does not use this rotation and does not unblock `act`.
