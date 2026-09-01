---
name: advise
description: >
  Read-only review-pair on an in-flight change. Verdict accept,
  accept-with-nits, or send-back. Use after change, before act, on
  architecture or instrument work, or when asked to advise / review the
  plan / architecture pass.
user-invocable: true
argument-hint: "<change-id>"
---

# advise

Load `../../references/shared.md`. You are a **reader**. You do not
implement. You do not fold. You do not flip the change banner.

This is the hole between `change` and `act`:

```
intend → steer → change → advise → act → fold
              ↖ amend ↙
```

## Skip

PARKED → stop. PENDING may be read, but an `accept` does **not**
unblock `act` until the banner is `ACTIVE BUILD`.

## Procedure

1. **Target.** Change-id from the user, or `change_id` on a packet.
   Open `openspec/changes/<id>/` (not `archive/`).
2. **Load.** `proposal.md`, `design.md` if present, `tasks.md`,
   `specs/**/spec.md`, cited code. `docs/LEARNINGS.md` if it names
   this id.
3. **Assign.** `python3 plugins/intention/scripts/ladder.py assign --shape architecture-review`
   (reader; default Opus 4.8). Optional consult: `--shape plan`
   (Fable, no write). Human pick always wins. Same-family as the
   change author cannot be the sole `accept` reader (ADR-005).

   Second family: Grok, or **Sol via OpenAI API** when `OPENAI_API`
   or `OPENAI_API_KEY` is set (`ladder.py show` — `sol-arch-review`
   `available: true`). Pick Sol with
   `ladder.py assign --shape architecture-review --id sol-arch-review`.
   Then `spawn.py stage` + `spawn.py run --adapter openai` (model
   `gpt-5.6-sol`, packet-only). Never a Codex slash. The ambient
   key is enough; do not paste it into the packet.
4. **Packet.** Readers receive `permission: read`. Foreign harnesses
   get a packet file, never a slash command. Sol is API, not a
   skill-host.
5. **Write** `openspec/changes/<id>/reviews/<YYYY-MM-DD>-advise.md`.
   First banner line after the title MUST be exactly one of:

   ```
   > **ADVISE:** accept
   > **ADVISE:** accept-with-nits
   > **ADVISE:** send-back
   ```

   Body: verdict, steelman against, one real tradeoff, findings,
   what is solid, implementer gaps. Cite file:line for code claims.
6. **Send-back** adds owed boxes on `tasks.md`. Does not flip the
   banner. **Accept** / **accept-with-nits** unblocks `act` on that
   change's write nodes (`ready.py` / `conductor.py ready`).
7. **Signed result** (`permission: read`):
   - accept / accept-with-nits → `disposition: pass` (nits listed)
   - send-back → `disposition: task-red` (not infra)
8. **Stop.** Do not implement nits (`change` amends). Do not fold.
   Do not `act`.

`ready.py` reports `needs_advise` when an ACTIVE BUILD architecture
or instrument change has no accepting advise (or last is send-back).
`act` must not dispatch those write nodes until an accept lands.
