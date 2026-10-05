# update-model-routing-health

> **ACTIVE BUILD**

## Why

Model assignment is scattered across versioned route ids, launcher mappings,
tests, and skill prose. A static `available` flag conflates configuration,
local executability, and recent quota/auth health, so routing repeatedly selects
known-broken adapters and stale model generations.

## What

- Remove Fable, pinned Opus 4.8, and Sol architecture-review routes.
- Introduce stable family-based route ids and one concrete version registry.
- Route known work Sonnet → Terra; implementation/thinking Sol → Opus;
  planning Opus → Astra; architecture review Opus-high → Astra → Grok 4.7.
- Separate configured, executable, and recently verified/degraded health.
- Make executability permission-aware: an OpenAI key alone cannot take writes.
- Preserve old route ids as migration aliases for one release.
- Enforce cross-family review by default and bound automatic fallback to two hops.

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: amend ADR-005 in `ARCHITECTURE.md`

## User journey & surfaces

No new UI because the behavior is visible through existing ladder assignment,
consult, advise, act, run, and spawn command surfaces.

## Preparation

- Inputs: user-approved routing decisions; Claude Opus CAUTION consultation;
  current ladder, spawn adapters, skills, tests, living verbs spec, ADR-005.
- Dependencies: none.
- Outcome: still valid. Current HEAD retains the old model table and no active
  change overlaps this routing surface.
- Authority: user granted the whole campaign on 2026-10-05.
- Review: `reviews/2026-10-05-advise.md` accepts the current contract. Carry
  forward deterministic author-family input, non-secret credential identity,
  one-release launcher compatibility for retired interfaces, and the complete
  stale-doc sweep. Contract unchanged.

## Out of scope

- Paid synthetic probes on every assignment.
- Health changing explicit human selection or route priority.
- Treating task/test failures as model-health failures.
- A global quota broker across unrelated repositories.
