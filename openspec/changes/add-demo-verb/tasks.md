# Tasks

- [x] `plugins/intention/skills/demo/SKILL.md` + `.agents/skills/demo` symlink
- [x] `shared.md` verb table row
- [x] Catalogs and check-skills list `demo`
- [x] verbs / packaging / default-loop deltas
- [x] Focused verify: `python3 plugins/intention/scripts/check-skills.py`
- [ ] Fold living specs when this change folds (union packaging with `add-run-wave-workflow` if still inflight)

## Owed (advise send-back 2026-09-02, fable-5.1-arch-review)

Delta / design text only. See `reviews/2026-09-02-advise.md`.

- [x] `verbs` delta: "demo invents no tracker" clause + scenario.
      Journey source is the proposal journey section and/or the Next
      command on the change's owed boxes (inflight or archived).
      Residue at most a bead comment / signed result `permission:
      read`. No `demo.md`, no minted box, no `demo` token in the
      EYES / by-eye / human-verify vocabulary (`run.py` `EYES_RE`).
- [x] `verbs` delta + `design.md`: slice-one demo is not a fold gate
      (single predicate stays `update-run-ooda`'s); bare `/run` may
      fold first; `demo <id>` resolves `openspec/changes/<id>/` then
      `openspec/changes/archive/*-<id>/`. Add the **Empty** scenario
      (no landed act in either → print `/status`, stop). Move "every
      act owes a demo?" out of *Not decided*.
- [x] `packaging` delta: strip "Fold MUST union this list … (today:
      `add-run-wave-workflow` …)" from the requirement body. Union
      instruction stays in `tasks.md` / `design.md` only.
