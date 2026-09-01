# intention

Default loop from intention to a running system:

`intend` → `steer` → `change` → `advise` → `act` → `fold`

Plus `brief` / `debrief` (disposable), `ready` / `map` (observe), `run`
(campaign). `steer` is the human-gated guidance pass (not a `/run`
wave; not `/ask`). Canonical skill files live here. In this repo,
`.agents/skills/<name>` is a symlink at each skill so Grok, Hermes, and
Prime load the same files without a plugin install.

## Say this

| You want | Say / run |
|---|---|
| Work out a plan, then show me | “work out a plan then run it by me” or `intend --ask …` |
| Give architecture / direction on the current DAG | `steer` (menus: recommended, skip, decide-for-me) |
| Plan + architecture review, then me | `intend --advise --ask …` |
| Switch which DAG this tab is on | `map --current <epic-or-id>` |
| Lay of *this* DAG (inflight / done / pending) | `map` (uses current) or `map <id>` (peek) |
| What’s on deck (OpenSpec **and** beads) | `ready` |
| Keep going while unblocked | `run --until roll` |
| Walk until a question appears | `run --until ask` |
| Scaffold + advise, never implement | `run --until advise` |

`--until ask` may still `act` until an elicitation. “Run it by me”
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

## Ready

`/ready` unions two sources. An empty OpenSpec lens is not an empty
board.

- **READY / PENDING / ADVISE / PARKED** — OpenSpec. JSON `ready` is
  this list only, so `/run --until empty` does not `act` a bead id.
- **BEADS** — `bd list --ready`. JSON `beads`. `/run --until roll`
  already walks it (landing → `change`, leftover task → `intend`).

Do not run `bd ready` as a second report.

## Run it by me

Optional gates on `intend` and `run` (`--plan` `--advise` `--ask`).
“Work out a plan then run it by me” is **plan + ask**. Architecture /
instrument also gets **advise** unless declined.

| Gate | Do | Do not |
|---|---|---|
| `--plan` | Intend the DAG. Skip if current already is it. | Re-plan unasked |
| `--advise` | `change` then `advise` | `act` |
| `--ask` | Pin current, present `map`, wait | `act`, `--until roll`. Next verb is `steer`. |

## Run campaign

`run.py` observes; the conductor follows one sibling skill per wave.
`--until roll`: fold → send-back amend → advise → act → beads.
A refused fold is not a stop — `--skip` that id and still **advise**
it. Same-family advise (ADR-005) is `--punt`, not a fake send-back.

## Install

Claude: `claude --plugin-dir ./plugins/intention` or marketplace
`intention`.

Grok: clone is enough (`.agents/skills/`). Or
`grok plugin marketplace add <this-repo>` and
`grok plugin install intention --trust`.

Codex / Hermes / Prime: Agent Skills standard. Invoke by name, never as
a Claude slash command. Matrix:
[`references/harness.md`](references/harness.md).

Other repos (Vercel `skills` CLI) — run from `$HOME`, not inside this
clone:

```bash
skills add /path/to/agent-plugin-bazaar/plugins/intention \
  --skill intend --skill steer --skill change --skill advise --skill act --skill fold \
  --skill brief --skill debrief --skill map --skill ready --skill run \
  --agent claude-code --agent codex --agent grok --agent hermes-agent \
  -g -y
```

Contracts: `docs/contracts/agent-surface.md`. Living specs:
`openspec/specs/`. Verb bodies: `references/` (shared vocabulary;
skills do not fork the surface).
