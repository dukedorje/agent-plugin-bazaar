---
name: consult
description: >
  Second opinion from architecture / plan / thinking readers. No intend
  node, no act unblock. Use when asked for a second opinion, another
  pair of eyes, consult the architecture buddy, or run this by Fable /
  Sol / Opus 4.8 / the panel.
user-invocable: true
argument-hint: "[--panel] [--id <route>] [<question>]"
---

# consult

Load `../../references/shared.md` and `../../references/act-io.md`.

This is **not** `advise`. Advise gates an in-flight change (`accept` /
`send-back` unblocks `act`). Consult is a side channel, like a
oneshot: pipe a question, get opinions, stop. It does not flip a
banner, write `openspec/changes/*/reviews/`, or unblock `act`.

## Skip

If there is an ACTIVE BUILD architecture/instrument change that needs
a gated reader, use `advise` instead.

## Procedure

1. **Brief.** The user's question plus any cited paths. Do not invent
   a change-id. Pass the question on stdin (or `--goal`). `--paths`
   for files they named.
2. **Who.** Default shape is `architecture-review` (Fable 5.1, then
   Sol, Opus 4.8; Grok if they asked). Plan/replan → `--shape plan`.
   Thinking → `--shape thinking` (still `permission: read`). Human
   pick always wins (`--id fable-5.1-arch-review` / `sol-arch-review`
   / `opus-4.8-arch-review` / `grok-arch-review`). `--panel` fans out
   every spawnable reader. This session's harness is not the sole
   reader: if you are Grok, pass `--not-harness grok` unless they
   asked for Grok.
3. **Spawn.**

   ```bash
   python3 plugins/intention/scripts/spawn.py consult \
     --shape architecture-review \
     [--panel | --id <route>] \
     [--not-harness <harness>] \
     [--paths <p> ...] \
     --goal "<question>"
   ```

   Or pipe the brief: `… consult --panel --paths ARCHITECTURE.md < brief.md`.
   Prompt is stdin; result is stdout JSON (`opinions[]` with
   `verdict` agree/caution/dissent and `body`).
4. **Present.** Quote verdicts and the one real tradeoff from each
   body. If `--panel`, compare qualitatively; do not majority-vote a
   fake accept. Do not implement the notes unless they then ask.
5. **Stop.** Do not `act`. Do not `fold`. Do not write an advise
   review file.

Grok has no CLI adapter here — skip it unless they want a packet to
hand over. Sol is `codex exec` (or OpenAI HTTP if no CLI).
