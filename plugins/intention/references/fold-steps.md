# fold algorithm

Today's date is the archive prefix (`YYYY-MM-DD`).

1. **Admit.** `openspec/changes/<id>/proposal.md` banner is
   `ACTIVE BUILD`. Refuse PENDING and PARKED.
2. **Checkboxes.** Every owed task is `[x]` or still `[ ]` with a note
   (human journey not yet exercised, etc.). No eternal empty boxes that
   mean “not our work” — those are bullets.
3. **Apply deltas** from `openspec/changes/<id>/specs/<cap>/spec.md`
   onto `openspec/specs/<cap>/spec.md`:
   - ADDED → append after existing requirements (create the living spec
     if this change introduces the capability).
   - MODIFIED → replace the whole `### Requirement: <name>` block with
     the pasted block.
   - REMOVED → delete that requirement block.
4. **Confirm.** Every SHALL this change claimed now appears in
   `openspec/specs/`. A SHALL only in `changes/` or `archive/` is not
   living truth.
5. **Archive.**

   ```bash
   mkdir -p openspec/changes/archive
   git mv openspec/changes/<id> openspec/changes/archive/YYYY-MM-DD-<id>
   ```

6. **Amend** `ARCHITECTURE.md` if the shape changed. Keep prior ADR text.
7. **Learn.** One dated line in `docs/LEARNINGS.md` per surprise.
8. **Report** living spec paths + archive path. That report is the result.

Do not implement leftover work during fold. Send it back to `act` or
open a new change.
