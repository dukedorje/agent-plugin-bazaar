# add-skills-packaging

> **ACTIVE BUILD** → folded and archived 2026-08-14 (F1).

## Why

C1 and C2 exist. Verbs need a host that works on Grok and Claude. Two
packagings survived Orient: a new Agent Skills tree, or a MetaDev fork.

## What

Fork. Same acceptance: five verbs runnable on Grok and Claude.

**Winner: Path A** — `plugins/intention` + `.agents/skills` symlinks +
both marketplace indexes.

**Loser: Path B** — fork/extend MetaDev. Parked. Revive when we need
planctl/headless runners and Phong wants an overlay that *consumes*
these packets.

## Impact

- New capability: `packaging`
- ADR-003
- Plugin `intention` 0.1.0
- Thin dispatchers for the five verbs (S1–S4 deepen)

## User journey & surfaces

No new UI because the surfaces are skill discovery: Grok loads
`.agents/skills/` in this repo; Claude loads plugin `intention`. Working:
`/intend` (or skill match) runs the dispatcher. Empty: clone without
symlinks. Failed: verbs only exist as Claude slash commands. Off: do not
install the plugin; in-repo Grok still sees `.agents/skills/`.

## Out of scope

- Deep skill bodies (S1–S4)
- Harness-by-harness adapters (H1)
- G1 hygiene
- Implementing Path B
