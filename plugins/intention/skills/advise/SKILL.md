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
3. **Assign.** Author family is the harness that wrote the change
   (this session if you wrote it; else the packet / review identity).
   Resolve a reader that is **not** that family:

   `python3 plugins/intention/scripts/ladder.py assign --shape architecture-review --not-harness <author>`

   Default without `--not-harness` is Fable 5.1 (Claude). Optional
   consult: `--shape plan` (Fable, no write). Human pick always wins.
   Same-family as the change author cannot be the sole `accept`
   reader (ADR-005). This session inlines advise only when it **is**
   the assigned other-family route.

   Second family is any `architecture-review` harness other than the
   author’s — not “Grok or Sol.” Grok author → Claude (Fable, or
   Opus 4.8). Claude author → Grok, or **Sol** when the Codex CLI is
   on PATH (`codex`) or `OPENAI_API_KEY` is set (`ladder.py show` —
   `sol-arch-review` `available: true`). Sol off does **not** mean
   no second family while Claude or Grok remains available.

   Spawn: `spawn.py stage` + `spawn.py run --adapter <harness>`
   (`claude` → live `claude -p`; `codex` → live `codex exec`; no
   CLI with `OPENAI_API_KEY` → `--adapter openai`). Override the
   Codex binary with `CODEX_BIN`. Never a Codex slash command. Do
   not paste keys into the packet. `run` waits this wave for that
   spawn; it does not park the id as ASK.

   **Panel (fan-out):** `ladder.py panel --shape architecture-review`
   then spawn Fable 5.1, Sol, and Opus 4.8 (or every available
   route). Compare verdicts. Still no sole-accept as the author
   (ADR-005).

   **Handoff:** if this reader cannot promote,
   `ladder.py assign --shape architecture-review --after <current-id>`
   and spawn the next. Do not fake a send-back to retrigger change.
4. **Packet.** Readers receive `permission: read`. Foreign harnesses
   get a packet file, never a slash command. Sol is packet-only
   (CLI or API), not a skill-host slash.
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
