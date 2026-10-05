---
name: consult
description: >
  Second opinion from architecture / plan / thinking readers. No intend
  node, no act unblock. Use when asked for a second opinion, another
  pair of eyes, consult the architecture buddy, run this by Opus /
  Astra / Grok, call several, or convoke a panel.
user-invocable: true
argument-hint: "[--who opus,astra,grok | --panel] [--shape architecture-review] [<question>]"
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
   (`opus` resolves the current registry version in every shape).
   Sol is a thinking reader; Sol and Terra are refused for architecture review.

   Chat routing (not a classifier):

   | Utterance | Flag |
   |---|---|
   | named models (“Astra”, “Opus and Grok”) | `--who astra` / `--who opus,grok` |
   | “compare Sol and Opus” | `--shape thinking --who sol,opus` (named wins) |
   | bare “panel” / “convoke” / “everyone” | `--panel` |
   | nobody named | first executable different-vendor reader (Opus → Astra → Grok) |

   `--who`, `--panel`, and `--id` are mutually exclusive. `--who`
   several is ladder priority order, not token order. Unknown or
   ambiguous nickname → error, do not guess. Named unspawnable
   → hard fail. `--panel` skips unspawnable.

   Supply `--author-family <harness/family/vendor>` for automatic architecture
   review. The author's vendor is skipped deterministically, even when that
   leaves no executable reader; report that condition. Human names override
   the boundary. Health warnings accompany explicit degraded picks. Automatic
   infra-red fallback preserves priority and takes at most two hops.
3. **Spawn.** The script is `scripts/consult.py` **in this skill
   directory** (the folder that contains this SKILL.md — Grok lists
   that path). It locates plugin `spawn.py`. Do **not** run
   `plugins/intention/scripts/spawn.py` from the current repo; that
   file only exists in the bazaar clone.

   ```bash
   python3 <this-skill-dir>/scripts/consult.py \
     --shape architecture-review \
     [--who opus,astra,grok | --panel | --id <route>] \
     [--author-family <author>] \
     [--paths <p> ...] \
     --goal "<question>"
   ```

   Or pipe the brief: `… consult.py --panel --paths ARCHITECTURE.md < brief.md`.
   Prompt is stdin; result is stdout JSON (`opinions[]` with
   `verdict` agree/caution/dissent and `body`).
4. **Present.** Quote verdicts and the one real tradeoff from each
   body. If `--panel` or several `--who`, compare qualitatively; do
   not majority-vote a fake accept. Do not implement the notes
   unless they then ask.
5. **Stop.** Do not `act`. Do not `fold`. Do not write an advise
   review file.

Grok is `grok --prompt-file` when `grok` is on PATH (`GROK_BIN`).
`--who grok` and `--panel` include it. Astra is `codex exec`
(or read-only OpenAI HTTP if no CLI). Thinking may use Sol through the same
adapter. Concrete model versions are resolved only from the family registry.
