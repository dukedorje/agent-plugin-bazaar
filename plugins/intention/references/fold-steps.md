# fold algorithm

Today's date is the archive prefix (`YYYY-MM-DD`).

1. **Admit.** `openspec/changes/<id>/proposal.md` banner is
   `ACTIVE BUILD`. Refuse PENDING and PARKED. Assign
   `ladder.py assign --shape fold` (latest Opus unless the human picked
   another folder). Spawn in the background when this session is not
   that route.
2. **Checkboxes.** Every owed task is `[x]` or still `[ ]` with a note
   (human journey not yet exercised, etc.). No eternal empty boxes that
   mean “not our work” — those are bullets.
3. **Base check.** Run `plugins/intention/skills/fold/scripts/fold_base.py check`
   on this change directory (or the skill-local `scripts/fold_base.py`).
   - Any `stale` row: apply nothing. Leave the change where it is.
     Return to the conductor. `run` already routes that id to `change`
     for a union re-paste. Do not `--skip` it into advise.
   - `unstamped` only: diff each named requirement against the living
     block by hand. If the paste still matches, `stamp`, then apply.
     If it does not match, treat it as stale. Do not apply.
   - Clean: apply.
4. **Apply deltas** from `openspec/changes/<id>/specs/<cap>/spec.md`
   onto `openspec/specs/<cap>/spec.md`:
   - ADDED → append after existing requirements (create the living spec
     if this change introduces the capability).
   - MODIFIED → replace the whole `### Requirement: <name>` block with
     the pasted block, omitting the `<!-- base: ... -->` line. That
     comment is fold metadata. It is not living text.
   - REMOVED → delete that requirement block.
5. **Confirm.** Every SHALL this change claimed now appears in
   `openspec/specs/`. A SHALL only in `changes/` or `archive/` is not
   living truth.
6. **Archive.**

   ```bash
   mkdir -p openspec/changes/archive
   git mv openspec/changes/<id> openspec/changes/archive/YYYY-MM-DD-<id>
   ```

7. **Amend** `ARCHITECTURE.md` if the shape changed. Keep prior ADR text.
8. **Learn.** One dated line in `docs/LEARNINGS.md` per surprise.
9. **Report** living spec paths + archive path. That report is the result.

Do not implement leftover work during fold. Send it back to `act` or
open a new change.
