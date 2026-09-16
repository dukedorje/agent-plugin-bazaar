---
name: demo
description: >
  Present the journey so the human can try a landed act. Internal
  ring only. After act, before fold. Use when asked to demo, try it,
  or /demo. Named change-id or the session current pin.
user-invocable: true
argument-hint: "[<change-id>]"
---

# demo

Observe-only halt. The human tries the feature. Not `status` (board).
Not EYES (mailbox checkbox). Not `fold`. Not staging or production.

The script is `scripts/demo.py` **in this skill directory**.

```
python3 <this-skill-dir>/scripts/demo.py
python3 <this-skill-dir>/scripts/demo.py add-run-wave-workflow
```

Print the command output. That is the halt. Do not re-derive the
journey from memory. Do not continue into fold or act.

## Source

Journey text is the change's proposal `User journey & surfaces`
and/or the `Next:` command on its owed boxes. Resolve
`openspec/changes/<id>/` first, then
`openspec/changes/archive/*-<id>/`. Bare `demo` uses this session's
map pin if it is a verb-led change-id.

Empty (no inflight dir, no archive): the script prints `/status` and
stops. That is legal. Bare `/run` may have folded first. Slice one
is not a fold gate.

## Residue

At most a bead comment or a signed result with `permission: read`.
Do **not** write `demo.md`. Do **not** mint an owed box. Do **not**
add a `demo` token to EYES / by-eye / human-verify. Do **not** check
an EYES box.

Halt is loud, like YOUR EYES. Stop.

Do not implement leftover tasks. Do not deploy. Do not fold.
