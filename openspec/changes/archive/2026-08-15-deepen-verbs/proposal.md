# deepen-verbs

> **ACTIVE BUILD** → folded and archived 2026-08-15 (S1–S4).

## Why

F1 landed thin dispatchers so the verbs would *load*. They were not yet
the complementary weave: no shared references, no output templates, no
hash helper, no fold algorithm an agent can follow without improvising.

## What

Deepen `intend`, `change`, `act`, `fold` against C1+C2. Shared vocabulary
in `plugins/intention/references/`. Living spec `verbs`. `brief` unchanged
(S0).

## Impact

- New capability: `verbs`
- Files: four SKILL.md, five references, `content-hash.py`
- Does not move the skill tree (ADR-003)

## User journey & surfaces

No new UI because the surfaces are the four skills. Working: `/intend`
prints a DAG; `/change` writes a PENDING proposal; `/act` writes a
packet; `/fold` archives. Empty: intention with only a direct fix.
Failed: a skill that implements or that restates the packet schema.
Off: do not invoke; files stay in the plugin.

## Out of scope

- H1 harness matrix
- G1 hygiene enforcement
- Deepening `brief`
- Path B / MetaDev
