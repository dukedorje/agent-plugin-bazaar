# Routing and passive health

`ladder.json` owns stable route ids, family versions, verification dates,
priority, and one-release migration aliases. `scripts/routing.py` resolves
models for both ladder and launcher. An older explicit model needs `pin_reason`.

Assignment accepts `--permission read|write|sensitive`; writes (including
advise review files) require a CLI harness. `OPENAI_API_KEY` alone makes only
read-only OpenAI HTTP executable. `--author-family <harness/family/vendor>`
is the recorded author identity for automatic architecture review. Claude
authors skip Opus and try Astra then Grok; Codex authors try Opus first.
Gating advise does not stop at that first route. `ladder.py vary-reader`
(`references/reviewers.md`) prefers Astra for high blast and otherwise
rotates through the eligible list. `assign` remains first-by-priority.
`--not-harness` remains an input alias for that vendor boundary. Explicit
`--who`/`--id` overrides health and the boundary and returns warnings.

Configured is pure policy; executable is recomputed locally for the requested
permission; health is `verified`, `unknown`, or `degraded`. Automatic selection
preserves priority, admits unknown, and skips degraded. Consult/oneshot retry
infra-red at most two hops. Manual handoffs pass `--after <route-id>` and
`--fallback-hops <completed hops>`; carry the returned hop count. Panels and
human picks run only the explicit selection.

No paid recurring probes. Only passive infrastructure evidence updates health:
success 60 minutes, quota 30 minutes, auth 24 hours or credential epoch change,
model-not-found until the family mapping changes, and two stalls within 15
minutes degrade for 15 minutes. Task-red and baseline-red are ignored.
Expired health is unknown and remains usable. Explicit `HealthStore.reset`
clears a record; the store accepts a clock and in-memory records for tests.

Default scratch is `$XDG_CACHE_HOME/intention/routing-health.json` (otherwise
the user's `.cache/intention/`); `INTENTION_HEALTH_FILE` overrides the path.
It is runtime cache, never project memory. Health keys contain adapter,
concrete model and a hash of a NON-SECRET credential identity, never an API key
or a hash of a key. Set `INTENTION_CREDENTIAL_ID_OPENAI` to an account/login
epoch (and bump on key rotation); CLI logins use corresponding `_CODEX`,
`_CLAUDE`, or `_GROK` values. Default identity uses a public org id or a default
login label. A credential change that does not change this public identity
requires explicit reset; auth also expires after 24 hours.
