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

## Revised contracts

An unchecked `Fresh advise after preparation` task invalidates historical
acceptance. Review the current reconciled contract in a new reader session.
Only that fresh accepting reader checks this task, recording the contract
reference in its review; send-back or infra-red leaves it open. Never clear
unrelated ASK/EYES work.

## Procedure

1. **Target.** Change-id from the user, or `change_id` on a packet.
   Open `openspec/changes/<id>/` (not `archive/`).
2. **Assign.** Supply the recorded author harness/family/vendor explicitly
   (this session if you wrote it; else the packet / review identity).
   Resolve a reader that is **not** that family:

   `python3 <this-skill-dir>/../../scripts/ladder.py vary-reader --permission write --author-family <author> --openspec openspec --change-dir openspec/changes/<id> [--blast high]`

   Load `../../references/reviewers.md`. High blast (schema, deletion,
   protocol, durability) passes `--blast high` and prefers Astra.
   Ordinary reads rotate. A send-back on this change returns to that
   `READER`. `assign` without `vary-reader` is the fallback list only.

   Run `ladder.py show` / `assign`: configured, executable, and health
   are separate. API-only OpenAI chat cannot write a review file.
   Unknown health remains usable; degraded routes are automatically skipped.
   On infra-red, pass `--after <route-id> --fallback-hops <completed hops>`
   and carry the returned `fallback_hops` into the next attempt. Stop after
   two automatic hops. The launcher records passive infrastructure evidence.

   Human pick (`--who` / `--id`) selects the spawned reader. It
   does not waive isolation.

   Eligible order stays Opus, then Astra, then Grok. Varying walks that
   list; it does not always start at Opus. Claude authors skip Opus;
   Codex authors skip Astra.
   Human picks may override the vendor boundary and degraded health with
   a warning. Optional extra: `--shape plan` consult (Opus then Astra). Plan consult is
   **not** the sole accept.

   If `assign --author-family <author>` finds no executable route:
   park as ASK (`PUNT: second-family advise` on `tasks.md`).
   Never inline. Never fake a send-back. Grok is spawnable when
   `grok` is on PATH (`GROK_BIN`).
3. **Packet a new session.** Reader gets: change id, Why
   (`proposal.md` without the design), living spec paths, cited
   file:line, LEARNINGS lines that name this id. Not this chat.
   Not “we just activated these.” Not `design.md` / `tasks.md`
   in the first brief.

   Packet sets `role: reader` (spawn.py keys the reader brief on
   it; `change_id` alone is an act packet). `constraints.paths` is
   the review dir (and `tasks.md`
   if send-back may add owed boxes or fresh accept must close the
   preparation marker). `permission: write` on
   that write-set only. Codex sandbox is `workspace-write` so
   the reader can persist the file. Consult stays read-only.

   `python3 <this-skill-dir>/../../scripts/spawn.py stage` +
   `spawn.py run --adapter <harness>`.
   Do not use cwd `plugins/intention/scripts/`.
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

**Panel:** `python3 <consult-skill-dir>/scripts/consult.py --panel`
is a second opinion; it
does not unblock `act`. Gating advise is one spawned
other-family reader (or several `--who`, still spawned). Compare
qualitatively; no sole-author accept (ADR-005).

`ready.py` reports `needs_advise` when an ACTIVE BUILD
architecture or instrument change has no accepting advise with
`READER:` (or last is send-back). `act` must not dispatch those
write nodes until that accept lands.
