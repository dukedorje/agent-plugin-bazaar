---
name: map
description: >
  Reprint the intend DAG with live status, last wave, and outcome.
  Pin or change the current intention for this session with --current.
  Use when asked for the lay of the land, the map, DAG status, how
  the nodes went, or to switch which DAG this tab is on.
user-invocable: true
argument-hint: "[<epic | bead | change-id>] [--current <id>|-]"
---

# map

Observe-only. The intend page, later: same shape, plus Status /
Wave / Outcome. Not `ready` (queue). Not `debrief` (one unit, deep).
Not a `/run` wave.

The script is `scripts/map.py` **in this skill directory**.

```
python3 <this-skill-dir>/scripts/map.py
python3 <this-skill-dir>/scripts/map.py bazaar-6os
python3 <this-skill-dir>/scripts/map.py --current bazaar-6os
python3 <this-skill-dir>/scripts/map.py --current -
```

Print the command output. That is the report. Do not re-derive the
DAG from memory.

## Current intention

Current is **this session's** DAG, not the repo's. Two tabs on the
same clone must not share a pin. The script writes
`~/.intention/sessions/<session>/current.json` keyed by
`GROK_SESSION_ID` (or `INTENTION_SESSION` / `--session`). Never write
`current` into the checkout, `.omc/`, or `openspec/`.

- `map --current <id>` — pin that DAG and print it.
- `map --current -` — clear the pin, then print the index.
- `map` — pinned DAG if any, else an **index** of open epics (one
  line each). Never flatten every bead.
- `map <id>` — peek that DAG without changing the pin.

After `/intend`, pin the root: `map --current <epic-or-id>`.

Residue is beads + banners + last advise + signed
`distilled.summary` / close reason. The session pin is attention,
not a fourth work store.

Do not implement. Do not unpark. Do not fold.
