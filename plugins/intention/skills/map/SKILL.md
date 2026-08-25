---
name: map
description: >
  Reprint the intend DAG with live status, last wave, and outcome.
  Use when asked for the lay of the land, the map, DAG status, or
  how the nodes went. Observe only.
user-invocable: true
argument-hint: "[<epic | bead | change-id>]"
---

# map

Observe-only. The intend page, later: same shape, plus Status /
Wave / Outcome. Not `ready` (queue). Not `debrief` (one unit, deep).
Not a `/run` wave.

The script is `scripts/map.py` **in this skill directory**.

```
python3 <this-skill-dir>/scripts/map.py
python3 <this-skill-dir>/scripts/map.py bazaar-6os
```

Print the command output. That is the report. Do not re-derive the
DAG from memory.

No scope lists open epics and their children. A named epic, bead, or
change-id focuses that graph. Residue is beads + banners + last
advise + signed `distilled.summary` / close reason. No fourth store.

Do not implement. Do not unpark. Do not fold.
