---
name: ready
description: >
  List ready unblocked work and everything parked. Use when asked what's
  ready, what's unblocked, what's parked, the ready-set, or "what's on deck".
user-invocable: true
argument-hint: "[--parked|--ready]"
---

# ready

Run from the repo root (pass `--parked` or `--ready` if the user asked
for only one list):

```bash
python3 scripts/ready.py
```

Print the command output. That is the report.

- **READY** — `ACTIVE BUILD` changes with open owed checkboxes (unblocked).
- **NEEDS ACTIVATION** — `PENDING` drafts. Not ready until a human activates.
- **NEEDS ADVISE** — `ACTIVE BUILD` architecture/instrument with no
  accepting `reviews/*-advise.md` (or last verdict `send-back`).
- **PARKED** — in-flight `PARKED` banners plus `openspec/parked.md`.

Do not implement. Do not unpark. If they want to start something, hand
off to `act` (ready) or wait for activation (pending).
