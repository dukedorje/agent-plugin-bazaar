# Learnings

Append-only. One line per hard-won fact. Dated, with a file reference.

- 2026-08-14 — Validating a JSON Schema `$defs` slice: build a tiny schema `{ "$ref": "#/$defs/Name", "$defs": schema["$defs"] }`. A bare `$ref` into the parent file needs a registry. (`docs/contracts/validate.py`)
- 2026-08-14 — MetaDev’s Grok path is a headless *worker*, not a skill host. A “fork MetaDev so Grok can run our verbs” plan still needs an Agent Skills tree — Path A inside Path B. (`ARCHITECTURE.md` ADR-003)
- 2026-08-15 — Vercel `skills` 1.4.8 had no `--agent grok` / `hermes-agent`. **1.5.22 added both** (`grok` → `.grok/skills/`, `hermes-agent` → `.hermes/skills/`). Prime is still only `--agent pi`. Do not `skills add` inside this repo. (`plugins/intention/references/harness.md`)
- 2026-08-15 — Fold-debt that only fires when every `- [x]` is checked misses lie-by-omission (no tasks.md). ACTIVE BUILD with no open owed box is fold-debt. A bland `- [ ] verify` still greens; do not pretend the stick kills every stall. (`scripts/check-hygiene.py`)
- 2026-08-15 — Parking a skill is an in-file banner plus `disable-model-invocation`, not a delete. Revive stays one explicit ask. (`plugins/morphist-tools/skills/sprint-plan/SKILL.md`)
- 2026-08-15 — A skills table that lists deleted names is a lie with the same voice as a live spec. Catalogs follow the directories; dropped names stay in CONVENTIONS only. (`CLAUDE.md`)
- 2026-08-15 — Ready-set is a query over banners + `openspec/parked.md`, not a second tracker. Beads `bd ready` is not used here. (`scripts/ready.py`)
- 2026-08-15 — Unparking a P1 host is a register edit plus intend, not a verb. Remaining hosts stay parked. (`openspec/parked.md`)
- 2026-08-15 — Speculative product talk files as intent / architecture-sketch / notes, not LEARNINGS and not living SHALLs. (`docs/taskmaster/`)
- 2026-08-16 — `.omc/` is disabled here (Claude and Grok). March–July contents were parked sprint-plan and OMC session junk. Tracker is beads. (`AGENTS.md`)
- 2026-08-15 — Conductor reads distilled; density is inverse of capability; persist at the worktree top. Never put “don’t commit” in a packet. (`docs/contracts/dispatch.md`)
