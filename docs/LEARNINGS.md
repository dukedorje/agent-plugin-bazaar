# Learnings

Append-only. One line per hard-won fact. Dated, with a file reference.

- 2026-08-14 — Validating a JSON Schema `$defs` slice: build a tiny schema `{ "$ref": "#/$defs/Name", "$defs": schema["$defs"] }`. A bare `$ref` into the parent file needs a registry. (`docs/contracts/validate.py`)
- 2026-08-14 — MetaDev’s Grok path is a headless *worker*, not a skill host. A “fork MetaDev so Grok can run our verbs” plan still needs an Agent Skills tree — Path A inside Path B. (`ARCHITECTURE.md` ADR-003)
- 2026-08-15 — Vercel `skills` 1.4.8 has no `--agent grok` or `hermes-agent`. Codex and `universal` both install to `.agents/skills/`, which Grok already scans. Do not `skills add` inside this repo or it copies into `.claude/skills/` and forks the tree. (`plugins/intention/references/harness.md`)
- 2026-08-15 — Fold-debt that only fires when every `- [x]` is checked misses lie-by-omission (no tasks.md). ACTIVE BUILD with no open owed box is fold-debt. A bland `- [ ] verify` still greens; do not pretend the stick kills every stall. (`scripts/check-hygiene.py`)
- 2026-08-15 — Parking a skill is an in-file banner plus `disable-model-invocation`, not a delete. Revive stays one explicit ask. (`plugins/morphist-tools/skills/sprint-plan/SKILL.md`)
