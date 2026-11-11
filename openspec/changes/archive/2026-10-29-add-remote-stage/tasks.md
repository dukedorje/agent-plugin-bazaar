# Tasks

- [x] Add optional `stage` to `taskPacket` in `docs/contracts/agent-surface.schema.json` (`src`, `dest`, optional `delete` boolean; extra properties refused). Note it in one line in `docs/contracts/agent-surface.md`. Leave `openspec/specs/agent-surface/spec.md` a pointer.
- [x] `cmd_stage` copies a present `stage` array onto `spec.json`. Absent stays absent.
- [x] After the idle check and before `write_prompt`, `run_turn` runs each step while `run_pi` still holds the lock. Same session as the paste. No second process. No Ctrl-C.
- [x] Non-zero step, or a non-empty `stage` with no runner registered: return without `write_prompt` and without `submit`. Blocker `pi-stage-failed`.
- [x] Absent `stage`, or an empty list: today's one-file prompt and one-line paste.
- [x] A step prunes `dest` only when that step's `delete` is `true`. No env flag. No adapter default.
- [x] `python3 plugins/intention/scripts/test-pi-tmux.py` covers failed step (no paste), zero step (paste), and no declaration.
- [x] One paragraph in `plugins/intention/references/act-io.md` on the order and the fail-closed rule.

The rsync argv is `add-rsync-before-keys`. This change fails closed until that runner is registered.

## Preparation

- [x] Fresh advise after preparation

## Owed from advise — 2026-10-29, astra-arch-review

- [x] Pin the shared runner contract: inputs (including the selected session/transport), return/failure shape, declaration-order execution, and first-failure short circuit. Assign timeout ownership and expected launch/transport exception normalization so failures produce `pi-stage-failed` without `write_prompt` or `submit`; the existing post-submit turn timer does not bound staging. Keep rsync implementation in the child change.
- [x] Extend focused verification to cover packet → spec → turn propagation and `pi-stage-failed` face mapping, especially non-empty stage with no runner. Assert event ordering under the lock, empty-stage compatibility, multi-step short circuit, dirty composer and unavailable lock running no stages, and the agreed runner exception/timeout path. Verify old packets remain schema-valid and malformed stage entries fail validation. Use local fakes, not a live remote copy.
