## MODIFIED Requirements

### Requirement: intend and act resolve the ladder file

`intend`, `act`, `advise`, `consult`, `fold`, and `run` SHALL assign agents
from `plugins/intention/references/ladder.json` via the shared ladder resolver.
They SHALL NOT invent a second assignment or model-version table. An explicit
human pick SHALL always win, including when recent health is degraded, but the
system SHALL report that warning.

The ladder SHALL use stable version-free route ids and one family registry that
maps each family to the concrete model id sent to its adapter. Family mappings
SHALL record when they were verified. A route that selects an older concrete
model SHALL provide a `pin_reason`. Historical route ids MAY remain migration
aliases for one release.

The default order SHALL be Sonnet then Terra for known/mechanical work; Sol
then Opus for implementation/thinking; Opus for design; Opus then Astra for
planning; Opus then optional Grok for fold; and Opus at high effort, then
Astra, then Grok for architecture review. Fable SHALL NOT be configured. Sol
and Terra SHALL NOT be architecture-review routes. Grok routes SHALL resolve to
Grok 4.7.

#### Scenario: Known coding task

- GIVEN shape `known`
- WHEN `ladder.py assign --shape known` runs
- THEN the assignee is the latest configured Sonnet (`skill-host`, density `explicit`)
- AND Terra is the next route

#### Scenario: Planning order

- GIVEN shape `plan`
- WHEN assignment runs
- THEN latest Opus is first and latest Astra is second
- AND no Fable or Sol planning route exists

#### Scenario: Architecture review order

- GIVEN shape `architecture-review`
- WHEN assignment runs for a non-Claude author
- THEN latest Opus at high effort is first, Astra is second, and Grok 4.7 is third
- AND no Fable, Sol, Terra, or pinned Opus 4.8 review route exists

#### Scenario: Cross-family review by default

- GIVEN the first architecture-review route shares the author's vendor family
- WHEN automatic assignment runs
- THEN it skips that route and selects the first executable different-family reader
- AND a human may explicitly override the skip

## ADDED Requirements

### Requirement: model routes separate configuration, executability, and health

The shared resolver SHALL distinguish configured routes, executable routes for
the requested permission, and recent adapter/model/credential health.
Configured SHALL be pure ladder truth. Executable SHALL be recomputed from the
available adapter, CLI, credentials, and permission; an OpenAI API key without
a write-capable harness SHALL NOT make a write route executable.

Health SHALL be `verified`, `unknown`, or `degraded`. Verified and unknown
routes SHALL remain eligible in configured priority order. Automatic selection
SHALL skip degraded routes without reordering the remaining priorities and
SHALL take at most two fallback hops. Explicit human selection SHALL not be
blocked by health.

Only infrastructure evidence SHALL affect health. A successful execution SHALL
remain verified for 60 minutes then become unknown. Quota failure SHALL remain
degraded until an explicit reset or 30 minutes. Authentication failure SHALL
remain degraded until credential identity changes or 24 hours. Model-not-found
SHALL remain degraded until the family mapping changes. Two stalls within 15
minutes SHALL degrade the route for 15 minutes. Task-red and baseline-red SHALL
NOT degrade model health.

#### Scenario: API key is read-only executability

- GIVEN Codex CLI is absent and only an OpenAI API key is present
- WHEN a read-only Astra consult is resolved
- THEN the route may be executable
- WHEN a Sol implementation write is resolved
- THEN that route is not executable

#### Scenario: Unknown health remains usable

- GIVEN the highest-priority executable route has no recent evidence
- WHEN automatic assignment runs
- THEN it remains eligible as `unknown`

#### Scenario: Quota fallback preserves priority

- GIVEN the first route has a recent quota failure and the next two routes are executable
- WHEN automatic assignment runs
- THEN it skips the degraded first route and selects the second route
- AND it does not reorder the remaining routes

#### Scenario: Human pick overrides degraded health

- GIVEN a human explicitly selects a degraded route
- WHEN assignment runs
- THEN it returns that route with a health warning
- AND it does not silently substitute another model

## MODIFIED Requirements

### Requirement: claude adapter is live print mode

`spawn.py run --adapter claude` SHALL invoke `claude -p` with the concrete
model id resolved from the packet's model family and with the route's explicit
effort. The prompt SHALL be written to stdin, not argv. Packet-only runs SHALL
pass `--disable-slash-commands`. Tests MAY stub the binary.

#### Scenario: Stub records resolved model

- GIVEN a fake `claude` on PATH and a route whose family is `sonnet`
- WHEN `run --adapter claude` executes
- THEN the fake argv includes `-p` and the family registry's concrete Sonnet id
- AND the prompt body is on stdin, not argv

### Requirement: second-family advise is spawned, not parked

When `next` is `advise`, `run` SHALL assign an executable
`architecture-review` route whose vendor family differs from the change author
unless the human explicitly selected a reader. It SHALL spawn that reader,
wait for the wave, and re-observe. It SHALL NOT halt or punt while a different-
family reader is executable. An infra-red spawn SHALL update model health and
retry according to bounded fallback; it SHALL NOT manufacture a verdict.

#### Scenario: Claude author uses another family

- GIVEN Claude authored an architecture change
- WHEN automatic advise assignment runs
- THEN it skips Opus and selects executable Astra, otherwise Grok 4.7

#### Scenario: Codex author uses Opus

- GIVEN Codex authored an architecture change
- WHEN automatic advise assignment runs
- THEN it selects latest Opus at high effort when executable
