---
name: ready
description: >
  List ready unblocked work and everything parked. Use when asked what's
  ready, what's unblocked, what's parked, the ready-set, or "what's on deck".
user-invocable: true
argument-hint: "[--parked|--ready]"
---

# ready

The observe script is `scripts/ready.py` **in this skill directory**
(the folder that contains this SKILL.md). Do **not** run
`scripts/ready.py` from the current repo unless that file exists —
it is not required. The skill script finds `openspec/` by walking up
from cwd.

```
python3 <this-skill-dir>/scripts/ready.py
python3 <this-skill-dir>/scripts/ready.py --json
python3 <this-skill-dir>/scripts/ready.py --parked
python3 <this-skill-dir>/scripts/ready.py --ready
```

Print the command output. That is the report. Do not re-derive the
ready-set by grepping banners yourself.

- **READY** — `ACTIVE BUILD` changes with open owed checkboxes (unblocked).
- **NEEDS ACTIVATION** — `PENDING` drafts. Not ready until a human activates.
- **NEEDS ADVISE** — `ACTIVE BUILD` architecture/instrument with no
  accepting `reviews/*-advise.md` (or last verdict `send-back`).
- **PARKED** — in-flight `PARKED` banners plus `openspec/parked.md`.

If the script prints `no openspec/` it is not a guessed ready-set.

Do not implement. Do not unpark. If they want to start something, hand
off to `act` (ready) or wait for activation (pending).
