# steer update-run-operator-flags

**When.** 2026-09-02
**Depth.** standard

## Decided

- Morning pile: on `/ready` (user | recommended)
  Why: looking is observation; run acts.
- `--until` tokens: collapse to interrupt + opt-outs (user | recommended)
  Why: walk is roll; stops and restrictions are named booleans.
- `--autonomous`: kill; `--interrupt` is the opposite of default
  (user | recommended)
  Why: roll already parks ASK/EYES and does not flip PENDING.

## Skipped

- (none)

## Feeds change

`ready` is the mailbox. Bare `/run` walks away. `/run --interrupt`
halts at the first elicitation. `--until` remains aliases for one
release. `--autonomous` warns and does nothing.
