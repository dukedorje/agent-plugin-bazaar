# Kept from sprint-exec

Extracted 2026-10-27 when morphist-tools `sprint-exec` was removed.
That skill dispatched `oh-my-claudecode` executors over story files in
`.omc/sprint-plan/` and `docs/sprints/`. OMC is uninstalled. Intention
`act` / `run` and `bd ready` already execute beads. Do not rebuild a
second dispatcher, a phase-state file, or a Dev Agent Record beside the bead.

## Unverified hypothesis

A hypothesis is unverified when a synthesis block has any of:

- `spike-required: true`
- `confidence` other than `high`
- `verification` other than `empirically-tested`
- `spike-artifact` missing or empty

A goal that bets on a library or a mechanism, with no `synthesis.md`
and no `docs/spikes/<id>/finding.md`, is the same offer. Say that no
synthesis exists yet.

Look in the goal, `docs/research/*/synthesis.md`,
`openspec/changes/*/research/*/synthesis.md`, and any decision the
node cites. Do not look in `.omc/`.

## When to offer spike

Offer it. Do not start it unless they choose **spike now**.

| Moment | Who |
|---|---|
| Intend, while the decision briefing is written | `intend` |
| The next steer menu, when a spike line is still open | `steer` |
| `design.md` names a decision that cites one | `change` |
| Advise has a verdict and the design list is still open | `advise` |
| Before `take`, if the node would land the recipe | `act` |

Three choices, recommended first:

1. **Spike now.** Hand off to the morphist `spike` skill. It blocks the landing until `docs/spikes/<id>/finding.md` says `go`.
2. **Spike before act.** Planning continues. `act` stops on this node until a `go` or a skip.
3. **Skip.** They accept the risk. `bd note` on the decision, and the spike line becomes `skipped`.

On **go**, the synthesis sets `spike-artifact`, `confidence: high`, and `verification: empirically-tested`. The spike line becomes `go`. On **no-go**, leave the decision open (`bd update {id} --status open` plus a note that names the finding) and do not land the recipe.

`act` does not run the spike. It refuses the launch while a line is still open. `--go` does not mark that line skipped.

### Residue

Beads and the change directory are the record. No new store.

- On the node description, one line: `- Spike: <id> <claim> — unverified (<confidence>, <verification>)`. Later values are `go` or `skipped`.
- In `design.md`, when architecture cites one: `## Unverified hypotheses`, one bullet per hypothesis (id, claim, confidence, verification, synthesis path).
- `map` reprints open lines in the decision briefing. `go` and `skipped` stay off that briefing.

## Beads is the only status record

- Work list is `bd ready`. Re-query it after a unit closes so newly
  unblocked children show up. Do not keep a private manifest.
- Start: `bd update {id} --status in_progress`.
- Success: `bd close {id} --reason "{one line}"`. File list and problems
  go on `bd note`. That note is the record.
- Blocker: leave the bead open, label it blocked, and note the type and
  detail. It then drops out of `bd ready`. Surface the blocker. Do not
  invent a workaround and close the bead.
- An epic is done when its child task beads are closed.
- Do not also write a story file, a Dev Agent Record, or
  `phase-state.json`.

## What a wave can and cannot see

Parallel units cannot read each other's notes while they run. A later
unit can. When `run` moves to the next sequential unit, put the prior
unit's hard-won fact in that unit's prompt (from the bead note or
`debrief`). Do not expect a parallel sibling to have it.

## Dry-run and resume

A dry-run prints the beads that would be picked up and stops. Resume
skips beads that are already closed. Re-running a closed bead takes an
explicit id.

## Do not port

Stop-threshold menus, huddle menus, ralph persistence, OMC `state_write`,
team fan-out, and story-file enrichment. Steer already does decision
menus. `run` already persists a campaign. `debrief` already expands one
finished unit. `retro` (morphist-tools) is the write-up for a whole body
of work.
