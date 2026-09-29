# update-run-eyes-face

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-09-02 (Duke: if it stops on EYES, make it obvious
something needs his eyes, with a command in Next steps).

## Why

`/run` parked EYES into `stop: empty` and a quiet `ask` list. Duke
could not tell a look was owed. `--wait` lumped EYES into `stop: ask`.

## What

- `stop: eyes` is its own halt. Card prints **YOUR EYES** and **Next:**
  the command from `Next: …` on the box (else `/status`).
- `--wait` / `--until ask`: PENDING/ASK → `stop: ask`; EYES → `stop: eyes`.
- `--until roll` still moves unrelated READY. It halts on EYES when
  the pick is an EYES id, leftover beads would skip past a look, or
  the board is otherwise empty with EYES still open.
- `/status` EYES section is **YOUR EYES** plus Next.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

Duke, from a Grok tab.

1. `/run` — EYES box open, nothing else to pick.
2. **Working** — card `stop: eyes`, YOUR EYES, Next: `/run-wave`.
3. **Empty** — no EYES, no READY: `stop: empty` as today.
4. **Off** — `--wait` with only PENDING still `stop: ask`.

`No new UI because` `/run` card and `/status`.

## Out of scope

- Checking the EYES box
- Fileset organizer (`bazaar-7kb.1`)
- Worktree land (PARKED)
