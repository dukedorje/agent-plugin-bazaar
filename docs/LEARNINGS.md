# Learnings

Append-only. One line per hard-won fact. Dated, with a file reference.

- 2026-08-14 — Validating a JSON Schema `$defs` slice: build a tiny schema `{ "$ref": "#/$defs/Name", "$defs": schema["$defs"] }`. A bare `$ref` into the parent file needs a registry. (`docs/contracts/validate.py`)
- 2026-08-14 — MetaDev’s Grok path is a headless *worker*, not a skill host. A “fork MetaDev so Grok can run our verbs” plan still needs an Agent Skills tree — Path A inside Path B. (`ARCHITECTURE.md` ADR-003)
