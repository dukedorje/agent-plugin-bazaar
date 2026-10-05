# Design — family routing and health

## Stable families, concrete executions

Routes have stable, version-free ids and declare a model family. A single
family registry resolves each family to the concrete model id sent to a CLI and
records when that mapping was verified. Human aliases resolve to routes inside
the requested shape. A route may pin an older concrete model only with a
`pin_reason`.

For one compatibility release, historical route ids remain aliases to the new
stable ids so `--after`, stored packets, and operator muscle memory do not fail
mid-campaign.

## Approved ladder

| Shape | Order |
|---|---|
| known / mechanical / bounded edit | Sonnet latest (currently 5.5) → Terra latest |
| implementation / thinking | Sol latest → Opus latest |
| design | Opus latest |
| plan / replan / intend consult | Opus latest → Astra latest |
| fold | Opus latest → Grok 4.7 optional |
| architecture review | Opus latest, high effort → Astra latest → Grok 4.7 |

Fable is absent. Sol and Terra are refused for architecture review.

## Three routing states

1. **Configured** is pure ladder truth: enabled, shape-compatible, resolves to
   a concrete model, and passes policy validation.
2. **Executable** is recomputed per call from adapter/CLI/credentials and
   requested permission. API-only OpenAI is read-only; write routes require a
   write-capable harness.
3. **Health** is recent evidence for the adapter + concrete model + credential
   identity: `verified`, `unknown`, or `degraded`.

Selection preserves configured priority. Unknown and verified routes are
usable; degraded routes are skipped for automatic selection. Explicit human
selection still wins and reports the health warning. Automatic fallback takes
at most two hops.

## Health evidence

Only infrastructure failures update health. Success is verified for 60
minutes, then decays to unknown. Quota failures degrade until an explicit reset
or 30 minutes. Authentication failures degrade until credential identity
changes or 24 hours. Model-not-found degrades until the family registry
changes. Two stalls within 15 minutes degrade for 15 minutes. Task-red and
baseline-red do not affect health.

The health store is runtime scratch, not project memory. Ladder and spawn share
one resolver module so configured/executable semantics cannot drift.

## Review-family boundary

Architecture review defaults to a vendor/family different from the author.
When Opus authored the contract, automatic selection skips Opus and tries Astra
then Grok. When Codex authored it, Opus remains first. Human selection may
override this boundary explicitly.
