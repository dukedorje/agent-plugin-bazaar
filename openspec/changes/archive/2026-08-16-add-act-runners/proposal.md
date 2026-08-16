# add-act-runners

> **ACTIVE BUILD** → folded and archived 2026-08-16.

## Why

The conductor can pick a disjoint node and persist. It still has no
honest way to *launch* a worker: shared scratchpads collide, empty
prompts silently skip, hangs look like code, and slash commands leak
onto packet-only hosts.

## What

- `plugins/intention/scripts/spawn.py` — unique prompt-file, hard-fail
  on empty, stall → `infra-red`, surface `skill-host` / `packet-only` /
  cloud `interface`
- Exec adapter only (forward-compat). No vendored MetaDev runners
- Focused tests: uniqueness, empty fail, slash-free packet-only, stall

## Impact

- Capabilities: MODIFIED `verbs`
- ADRs: none

## User journey & surfaces

No new UI because the surfaces are `act` and
`python3 plugins/intention/scripts/spawn.py`. Working: `stage` writes a
new `.spawns/<node>-<id>/prompt.md` with the packet inlined; `run`
with a hanging adapter and a short timeout returns `infra-red`. Empty:
missing or zero-byte prompt exits non-zero before any worker starts.
Failed: two stages never share a path. Off: do not invoke `act`;
packets still exist without a spawn.

## Out of scope

- Vendoring `codex-headless-exec` / `grok-headless-exec` / `planctl`
- Auto-wiring live Codex/Grok/Claude CLIs
- Ready-set scheduling (already `conductor.py`)
