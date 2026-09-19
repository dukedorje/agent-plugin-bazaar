# intention

Default loop from intention to a running system:

`intend` → `steer` → `change` → `advise` → `act` → `demo` → `fold`

Plus `brief` / `debrief` (disposable), `status` / `map` (observe), `run`
(campaign), `run-wave` (one disjoint act fan-out), `consult` (second
opinion, no intend node), `demo` (try a landed act). `steer` is the
human-gated guidance pass (not a `/run` wave; not `/ask`). Canonical
skill files live here. In this repo, `.agents/skills/<name>` is a
symlink at each skill so Grok, Hermes, and Prime load the same files
without a plugin install.

## Say this

| You want | Say / run |
|---|---|
| Work out a plan, then show me | “work out a plan then run it by me” or `intend --ask …` |
| Give architecture / direction on the current DAG | `steer` (menus: recommended, skip, decide-for-me) |
| Plan + architecture review, then me | `intend --advise --ask …` |
| Switch which DAG this tab is on | `map --current <epic-or-id>` |
| Lay of *this* DAG (inflight / done / pending) | `map` (uses current) or `map <id>` (peek) |
| What’s on deck (OpenSpec **and** beads) | `status` |
| Honest open pile (unblocked leaves, no empty faces) | `status --queue` |
| Keep going while unblocked | `run` |
| Fan two disjoint writes on HEAD | `run-wave` |
| Try a landed act (internal ring) | `demo` / `demo <change-id>` |
| At the desk; halt at first ASK/EYES/PENDING | `run --wait` |
| Morning pile (ASK / EYES / PUNT) | `status` |
| Scaffold + advise, never implement | `run --advise` |
| Cautious: no fold, no leftover beads | `run --no-fold --no-beads` |
| Tidy only | `run --tidy` |
| Fold a landed change (background, Opus 5) | `fold <id>` |
| Second opinion (no change, no act unblock) | `consult` / `consult --who sol,fable` / `consult --panel` |
| Dispatch a small task (no intend node) | `oneshot` / `oneshot --who terra` |

`--wait` may still `act` until an elicitation. “Run it by me”
never `act`s — the plan *is* the question.

## Current intention

Which DAG this **tab** is holding. Not the repo’s. Two agents on the
same clone must not share a pin.

```
map --current bazaar-tvm    # pin and print that DAG
map                         # same DAG again
map bazaar-db8              # peek; pin stays tvm
map --current -             # clear → epic index, not every bead
```

After `/intend`, pin the root. Storage is
`~/.intention/sessions/<GROK_SESSION_ID>/current.json` (or
`INTENTION_SESSION` / `--session`). Never `openspec/current` or
`.omc/current`.

Bare `map` with no pin is a one-line **index** of open epics.

## Status

`/status` unions two sources (`/ready` is an alias). An empty OpenSpec
lens is not an empty board.

- **READY / PENDING / ADVISE / PARKED** — OpenSpec. JSON `ready` is
  this list only, so `/run --until empty` does not `act` a bead id.
- **BEADS** — `bd list --ready`. JSON `beads`. Bare `/run`
  already walks it (landing → `change`, leftover task → `intend`).
- **`--queue`** — honest open pile. Unblocked leaves (no umbrella
  epics) + OpenSpec READY, then BLOCKED with waiting-on. No empty
  ASK/EYES/(none) faces. JSON `{queue, blocked, waiting}`.

Do not run `bd ready` as a second report.

## Run it by me

Optional gates on `intend` and `run` (`--plan` `--advise` `--ask`).
“Work out a plan then run it by me” is **plan + ask**. Architecture /
instrument also gets **advise** unless declined.

| Gate | Do | Do not |
|---|---|---|
| `--plan` | Intend the DAG. Skip if current already is it. | Re-plan unasked |
| `--advise` | `change` then `advise` | `act` |
| `--ask` | Pin current, present `map`, wait | `act`, `/run`. Next verb is `steer`. |

## Run campaign

`run.py` observes; the conductor follows one sibling skill per wave.
Bare `/run` walks away (roll). `--wait` is desk mode. `--tidy` folds.
`/status` is the morning pile. `--until *` / `--interrupt` / `--only fold`
are one-release aliases.
A refused fold is not a stop — `--skip` that id and still **advise**
it. Same-family advise (ADR-005) **spawns** the other-family reader
(Fable vs a Grok author; Grok/Sol vs a Claude author). `--punt` only
when no other-family route exists — not a fake send-back, not a halt.

## Install

Claude: `claude --plugin-dir ./plugins/intention` or marketplace
`intention`. After a `main` commit or pull, `scripts/sync-harness-plugins.py`
refreshes the versioned marketplace cache so auto-update is not stuck on
the last version number. Enable the git hook once:
`python3 scripts/sync-harness-plugins.py --install-hooks`.

Grok: clone is enough (`.agents/skills/`). Or
`grok plugin marketplace add <this-repo>` and
`grok plugin install intention --trust`.

Codex: install the complete plugin so shared references, scripts, workflows,
and agents stay beside the skills:

```bash
codex plugin marketplace add /path/to/agent-plugin-bazaar
codex plugin add intention@agent-plugin-bazaar
```

Start a new Codex thread after install or update. Invoke by `$intend`,
`@intention:intend`, or skill match—never as a Claude slash command.

Hermes / Prime use the Agent Skills standard from a checkout whose
`.agents/skills/` entries point into this complete plugin tree. Do not
globally copy only `skills/`: Intention verbs also load the sibling
`references/`, `scripts/`, `workflows/`, and `agents/` directories. Matrix:
[`references/harness.md`](references/harness.md).

Contracts: `docs/contracts/agent-surface.md`. Living specs:
`openspec/specs/`. Verb bodies: `references/` (shared vocabulary;
skills do not fork the surface).
