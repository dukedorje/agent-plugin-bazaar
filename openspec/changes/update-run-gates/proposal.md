# update-run-gates

> **PENDING**

**Rigor:** change

Depends on: `update-run-ooda` / `bazaar-8uv.1` (the stage set
exists). Not activated.

## Why

Once `next` can be any loop stage, the product is which gates fire
by default. Without a named table, `--until empty` will grow into
intend-and-fold-everything, or someone will flip PENDING to keep
the walk moving.

## What

- Name the default gates. No new verbs.
- `--until empty` (default): change → advise → act. Stop at
  PENDING, ASK, and fold. Do not intend unless the scope is a
  goal. Do not fold.
- `--until fold`: after writes, `next: fold` when legal.
- `--until advise` / `--until activation` / `--until ask`:
  unchanged.
- `--autonomous`: same walk as empty; consult-before-ask; never
  flip PENDING or by-eye; never deploy.
- Capability: ADDED on `verbs` (gate table). Does not replace the
  campaign `next` set.

## Impact

- Capabilities: ADDED on `verbs`
- ADRs: none

## User journey & surfaces

Duke, from chat, after ooda next values exist.

1. Says `/run` or `/run add-x --until empty`.
2. **Working** — change / advise / act only. Stops before fold.
3. **Goal scope** — intend is allowed (ooda); empty does not
   invent a goal.
4. **`--until fold`** — after writes, `next: fold` when legal.
5. **PENDING** — stop activation; banner unchanged.
6. **`--autonomous`** — same walk; EYES for by-eye; no deploy.
7. **Off** — no table; empty may fold or intend a change-id.

`No new UI because` the surfaces are `/run` flags and
`plugins/intention/skills/run/SKILL.md` policy table.

## Out of scope

- Expanding the `next` set — `update-run-ooda` / `bazaar-8uv.1`
- Flipping PENDING
- `--until intend` as a new token (empty + a goal is enough)
- Path B / `planctl`
