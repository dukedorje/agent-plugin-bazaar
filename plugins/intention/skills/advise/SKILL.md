---
name: advise
description: >
  Fresh-context read-only review of an in-flight change. Verdict accept
  or send-back. Notes in the body. Never accept in the author tab.
  Use after change, before act, on architecture or instrument work, or
  when asked to advise / review the plan / architecture pass.
user-invocable: true
argument-hint: "<change-id>"
---

# advise

Load `../../references/shared.md`. You are the **conductor** of a
reader, not the reader. You do not implement. You do not fold. You
do not flip the change banner. You do **not** write
`reviews/*-advise.md` with `accept` in this conversation.

No change on the board? Use `consult` (second opinion). This skill
gates an in-flight change.

```
intend → steer → change → advise → act → fold
              ↖ amend ↙
```

## Skip

PARKED → stop. PENDING may be read, but an `accept` does **not**
unblock `act` until the banner is `ACTIVE BUILD`.

## Same-tab is not advise

This session, if it authored the change, may write
`openspec/changes/<id>/notes/self-critique.md` (disclosure). That
file MUST NOT contain `**ADVISE:**`. Human pick chooses **which
reader to spawn**, not “this conversation may accept.” Grok-on-Grok
or Claude-on-Claude in one thread is asking yourself.

## Procedure

1. **Target.** Change-id from the user, or `change_id` on a packet.
   Open `openspec/changes/<id>/` (not `archive/`).
2. **Assign.** Author family is the harness that wrote the change
   (this session if you wrote it; else the packet / review identity).
   Resolve a reader that is **not** that family:

   `python3 plugins/intention/scripts/ladder.py assign --shape architecture-review --not-harness <author>`

   Run `ladder.py show` / `assign` — never treat the static
   `available: false` in `ladder.json` as physics. Env-presence
   (`codex` on PATH, `OPENAI_API_KEY`) is a preflight, not a
   successful spawn. If spawn infra-reds, `--after` the current id
   and spawn the next. Do not skip Sol because the JSON file said
   false.

   Human pick (`--who` / `--id`) selects the spawned reader. It
   does not waive isolation.

   Fable 5.1 on architecture-review is a valid *other-family*
   reader only when the author is not Claude. Optional extra:
   `--shape plan` consult (Fable). Plan consult is **not** the
   sole accept.

   If `assign --not-harness <author>` finds no spawnable route
   (Claude author, no Codex, Grok has no CLI adapter): park as
   ASK (`PUNT: second-family advise` on `tasks.md`). Never
   inline. Never fake a send-back.
3. **Packet a new session.** Reader gets: change id, Why
   (`proposal.md` without the design), living spec paths, cited
   file:line, LEARNINGS lines that name this id. Not this chat.
   Not “we just activated these.” Not `design.md` / `tasks.md`
   in the first brief.

   Packet `constraints.paths` is the review dir (and `tasks.md`
   if send-back may add owed boxes). `permission: write` on
   that write-set only. Codex sandbox is `workspace-write` so
   the reader can persist the file. Consult stays read-only.

   `spawn.py stage` + `spawn.py run --adapter <harness>`.
   Claude → `claude -p` (stdin). Codex → `codex exec -`.
   No CLI + `OPENAI_API_KEY` → `--adapter openai` (HTTP cannot
   write files — last-resort harvest only). Never a Codex
   slash. `run` waits this wave.
4. **Blind pass (in the reader packet).** Order the reader must
   follow: Why + living spec + cited code → 10-line independent
   take (what they would pin, refuse, one tradeoff) → **then**
   open `design.md` / `tasks.md` → compare. Steelman against
   that take. The take is **concerns the author must have
   answered**, not a competing design.
5. **The reader writes the review.** Not this tab. After spawn,
   check `openspec/changes/<id>/reviews/<YYYY-MM-DD>-advise.md`
   exists with:

   ```
   > **ADVISE:** accept
   > **READER:** <route-id>
   > **SPAWN:** <spawn-dir>
   ```

   or `send-back`. Notes in the body. Do not write
   `accept-with-nits`. Do not transcribe or edit the verdict.
   Missing file after a green spawn is infra — retry once, then
   ASK. HTTP OpenAI fallback may harvest only if there is no
   CLI.

   `ready.py` / `advise_status.py` **ignore** an `accept` that
   has no `READER:` line. Same-tab accept does not unblock `act`.
6. **Send-back** adds owed boxes on `tasks.md` (reader writes
   those too). Does not flip the banner. **Accept** (with
   `READER:`) unblocks `act`.
7. **Signed result:**
   - accept → `disposition: pass`
   - send-back → `disposition: task-red` (not infra)
8. **Stop.** Do not implement the notes (`change` amends). Do
   not fold. Do not `act`.

**Panel:** `spawn.py consult --panel` is a second opinion; it
does not unblock `act`. Gating advise is one spawned
other-family reader (or several `--who`, still spawned). Compare
qualitatively; no sole-author accept (ADR-005).

`ready.py` reports `needs_advise` when an ACTIVE BUILD
architecture or instrument change has no accepting advise with
`READER:` (or last is send-back). `act` must not dispatch those
write nodes until that accept lands.
