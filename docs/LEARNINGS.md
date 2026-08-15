# Learnings

Append-only. One line per hard-won fact. Dated, with a file reference.

- 2026-08-14 — Validating a JSON Schema `$defs` slice: build a tiny schema `{ "$ref": "#/$defs/Name", "$defs": schema["$defs"] }`. A bare `$ref` into the parent file needs a registry. (`docs/contracts/validate.py`)
