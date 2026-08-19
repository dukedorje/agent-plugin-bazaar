# update-run-ooda

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-19 (`activate bazaar-8uv.1`).

## Why

`/run` already emits `next: change` when a named landing has no
change directory. The OODA loop is observe → orient → decide → act
→ observe again. `intend` and `fold` are those outer beats and are
not legal `next` values. A goal that is not a change-id cannot
enter the campaign except by someone typing `/intend` first.

## What

- `next` may be `intend`, `change`, `advise`, `act`, or `fold`.
- Goal (not a verb-led change-id) → `next: intend`.
- Named landing, no dir → `next: change` (unchanged).
- `--until fold` and fold is legal → `next: fold`.
- `ready` stays the card observe, not a wave. `brief` stays
  disposable.
- `run.py` still launches zero workers. Conductor re-reads the
  stage skill.
- Capability: MODIFIED `verbs`. ADDED on `default-loop` if the
  stranger line needs the full stage set.

## Impact

- Capabilities: MODIFIED `verbs` · ADDED on `default-loop`
- ADRs: none

## User journey & surfaces

Duke, from chat, on a goal or a landing.

1. Says `/run we need extract-from on intend`.
2. **Working (goal)** — card `next: intend`. Conductor re-reads
   `intend/SKILL.md` for one wave.
3. **Working (no directory)** — `/run add-x` → `next: change`
   (already living).
4. **Working (`--until fold`, writes done, fold legal)** —
   `next: fold`.
5. **Empty** — no goal, no ready, no advise: stop empty.
6. **Failed** — PENDING scope: stop activation.
7. **Off** — `ready.py` missing: stop `no-ready`.

`No new UI because` the surfaces are `/run` and
`plugins/intention/skills/run/scripts/run.py`.

## Out of scope

- Named default gate table — `update-run-gates` / `bazaar-8uv.2`
- Flipping PENDING
- A second executor inside `run.py`
- Path B / `planctl` / `@skills`
