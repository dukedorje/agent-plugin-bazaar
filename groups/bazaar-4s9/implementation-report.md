# Worker report — bazaar-4s9

Implemented stable family routing, the approved route order and concrete registry,
one-release route/interface migration aliases, permission-aware adapter resolution,
passive infra health with injectable clock/store and TTLs, human override warnings,
deterministic author-vendor input, and automatic consult/oneshot fallback capped
at two hops. Launcher model argv resolves through the shared registry; API-only
HTTP refuses writes before launch. Removed the paid live acceptance probe.

## Focused acceptance

Ran exactly once:
`python3 plugins/intention/scripts/test-ladder.py && python3 plugins/intention/scripts/test-spawn.py`

Exit 0. Routing/health contract checks passed; all 25 spawn tests passed.
All adapter checks were offline or stubbed. Grok argv resolves `grok-4.7`.

## Changed files owned by this worker

- `ARCHITECTURE.md`
- `docs/LEARNINGS.md`
- `plugins/intention/README.md`
- `plugins/intention/references/act-io.md`
- `plugins/intention/references/fold-steps.md`
- `plugins/intention/references/intend-dag.md`
- `plugins/intention/references/ladder.json`
- `plugins/intention/references/shared.md`
- `plugins/intention/references/routing.md` (new)
- `plugins/intention/scripts/ladder.py`
- `plugins/intention/scripts/routing.py` (new)
- `plugins/intention/scripts/spawn.py`
- `plugins/intention/scripts/test-conductor.py` (reader fixture names only)
- `plugins/intention/scripts/test-ladder.py`
- `plugins/intention/scripts/test-spawn.py`
- `plugins/intention/skills/act/SKILL.md`
- `plugins/intention/skills/advise/SKILL.md`
- `plugins/intention/skills/consult/SKILL.md`
- `plugins/intention/skills/fold/SKILL.md`
- `plugins/intention/skills/intend/SKILL.md`
- `plugins/intention/skills/run/SKILL.md`
- `openspec/changes/update-model-routing-health/tasks.md`
- `groups/bazaar-4s9/implementation-report.md`

## Preserved overlaps and conductor obligations

Existing dirty branch-policy/frontier-preparation edits in act/fold/run skills
and shared references were retained. This worker did not edit change skill,
run observer/tests, advise-status script, living specs, root README, agent
contracts, beads, archived changes, or unrelated scratch trees. Retired names
remain only in explicit migration aliases, migration/rejection tests, accepted
historical review, and superseded dated learning records.

The task box for the full sweep including living specs remains unchecked;
`openspec/specs/verbs/spec.md` is reserved for fold. The preserve-and-commit box
remains unchecked because the conductor persists. No commit, push, fold or archive
was performed. This report is an unsigned worker handoff, not a signed result
claiming persisted artifacts.

Credential epochs are operator-provided non-secret ids; update
`INTENTION_CREDENTIAL_ID_<ADAPTER>` when credentials change, or explicitly reset
runtime health. Default labels do not automatically detect a secret-key rotation.
