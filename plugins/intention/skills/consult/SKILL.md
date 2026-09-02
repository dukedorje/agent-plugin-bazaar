---
name: consult
description: >
  Second opinion from architecture / plan / thinking readers. No intend
  node, no act unblock. Use when asked for a second opinion, another
  pair of eyes, consult the architecture buddy, run this by Fable /
  Sol / Opus 4.8, call several, or convoke a panel.
user-invocable: true
argument-hint: "[--who fable,sol | --panel] [--shape architecture-review] [<question>]"
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
2. **Shape first, then who.** Default shape is `architecture-review`.
   Plan/replan → `--shape plan`. Thinking → `--shape thinking`
   (still `permission: read`). Nicknames bind *inside* that shape
   (`opus` is 4.8 on architecture-review, Opus 5 on thinking).
   `4.8` is never Opus 5. `terra` is not a thinking reader.

   Chat routing (not a classifier):

   | Utterance | Flag |
   |---|---|
   | named models (“Sol”, “Fable and 4.8”) | `--who sol` / `--who fable,4.8` |
   | “compare Sol and Fable” | `--who sol,fable` (named wins; not the full panel) |
   | bare “panel” / “convoke” / “everyone” | `--panel` |
   | nobody named | first spawnable (Fable on architecture) |

   `--who`, `--panel`, and `--id` are mutually exclusive. `--who`
   several is ladder priority order, not token order. Unknown or
   ambiguous nickname → error, do not guess. Named unspawnable
   (Grok, no CLI) → hard fail. `--panel` skips unspawnable.

   This session’s harness is skipped (`--not-harness`) **only if**
   another spawnable reader exists, and **not** when they named
   this harness. Do not skip Claude by default — that can leave
   nobody to ask.
3. **Spawn.**

   ```bash
   python3 plugins/intention/scripts/spawn.py consult \
     --shape architecture-review \
     [--who fable,sol | --panel | --id <route>] \
     [--not-harness <harness>] \
     [--paths <p> ...] \
     --goal "<question>"
   ```

   Or pipe the brief: `… consult --panel --paths ARCHITECTURE.md < brief.md`.
   Prompt is stdin; result is stdout JSON (`opinions[]` with
   `verdict` agree/caution/dissent and `body`).
4. **Present.** Quote verdicts and the one real tradeoff from each
   body. If `--panel` or several `--who`, compare qualitatively; do
   not majority-vote a fake accept. Do not implement the notes
   unless they then ask.
5. **Stop.** Do not `act`. Do not `fold`. Do not write an advise
   review file.

Grok has no CLI adapter here — skip it on `--panel`; `--who grok`
errors unless they want a packet to hand over. Sol is `codex exec`
(or OpenAI HTTP if no CLI).
