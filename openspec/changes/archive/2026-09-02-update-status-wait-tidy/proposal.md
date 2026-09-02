# update-status-wait-tidy

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-09-02 (chat: ready→status, --interrupt→--wait, --only fold→--tidy).

## Why

The observe verb is the board, not a subset of it. `--interrupt` fights
the `--ask` gate. `--only fold` is a tidy pass wearing a walk flag.

## What

- Verb `ready` becomes `status`. `/ready` remains an alias.
- `/run --wait` is desk mode (was `--interrupt`).
- `/run --tidy` is fold-only (was `--only fold`).
- Old flag names stay aliases for one release.
- JSON `ready` (the implement list) is unchanged.

## Impact

- Capabilities: MODIFIED `verbs`, `packaging`, `default-loop`, `living-specs`
- ADRs: none

## User journey & surfaces

Duke, from chat.

1. `/status` — the board, including ASK / EYES / PUNT.
2. `/run --wait` — halt at first elicitation.
3. `/run --tidy` — fold-legal only.
4. **Off** — still saying `/ready` and `--interrupt`.

`No new UI because` the skill names and `/run` flags.

## Out of scope

- Renaming JSON `ready` or `bd ready`
- Renaming `conductor.py ready`
