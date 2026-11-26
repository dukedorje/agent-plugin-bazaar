# Architecture readers

Opus (`opus-design`, effort low) writes the ordinary initial architecture.
Fable 5.2 (`fable-design`, model `claude-fable-5-2`, effort medium) drafts
that architecture on schema, deletion, protocol, or durability, or when a
human names Fable. Effort high is only `--blast hardest`. The session
driver, often Grok, may edit the draft before advise. Pass the driver's
family as `--author-family`.

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
  [--blast schema|deletion|protocol|durability|hardest]
```

The author's vendor is skipped. Human `--who` / `--id` still wins.
Do not pass `--blast high` or `--blast challenging`. Those tokens stay
on Astra.

- **Ordinary review** is Astra at medium effort. A previous accept does
  not move the next review on. If Astra is the author vendor, take the
  first remaining reader that is not Fable (Grok, then Opus) and say why.
- **Category blast** (schema, deletion, protocol, durability) is Fable
  5.2 at medium effort: a different perspective and the solutioning pass.
  If Fable is not eligible, take the first remaining reader at medium
  effort and say why.
- **Hardest** (`--blast hardest`) is the only Fable effort high. Use it
  when the problem is stuck after a real attempt, or a human names it
  the hardest case. Do not use it because the change is architecture.
- **Send-back** on this change returns to that review's `READER` when the
  route is still eligible. Do not switch away from the reader who sent it
  back.
- **Initial architecture** is Opus. Fable drafts it on a category blast
  (`vary-reader --shape design --blast schema`) or when a human names
  Fable. Ordinary plan consult is Astra, then Opus, both medium. Fable
  takes a plan on the same four blasts (`vary-reader --shape plan --blast
  protocol`). `--blast hardest` raises that Fable route to effort high.

A fresh session after send-back is the same reader, not the next one.
Consult does not use this rotation and does not unblock `act`.
