# Tasks

- [x] Independent architecture advise accepts the family registry, health semantics, and review-family boundary.
- [x] Replace the ladder with stable route ids, the approved route order, migration aliases, and centralized concrete family versions.
- [x] Add shared configured/executable/health resolution with permission-aware adapter checks and bounded fallback.
- [x] Record and consume infra-only health evidence with the approved TTLs and injectable clock/store tests.
- [x] Update spawn adapters to use resolved concrete models and remove silent stale-model fallbacks.
- [ ] Remove Fable, Opus 4.8, Sol architecture-review, and stale routing claims from live skills, references, specs, ADRs, and tests.
- [x] Verify Grok 4.7 model selection without requiring a paid recurring probe.
- [x] Preserve unrelated dirty work and commit only this change's files.

## Worker evidence — 2026-10-05

The packet acceptance command ran exactly once:
`python3 plugins/intention/scripts/test-ladder.py && python3 plugins/intention/scripts/test-spawn.py`
Exit 0: routing/health contract checks passed, and all 25 offline spawn tests passed.
No paid API probe ran. Live skills, references, README, ADR-005 and learning
claims were swept; historical learning entries are explicitly superseded.
The complete sweep box remains open because the conductor reserved living-spec
editing for fold. The persist box remains open because this worker does not commit.
