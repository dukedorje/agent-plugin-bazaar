# Tasks

- [x] Add `plugins/intention/skills/status/scripts/refusal.py`. It reads a beads export (fixture or `bd export`) and prints the card in `design.md`.
- [x] Cover the specimen: four `outside` beads, one human gate, one `internal` blocker, one `deferred` bead. A second call prints the same text. An action the outside rows do not name moves those rows to Separate. A missing export prints the unreadable line and no project.
- [x] `status` Blocked and `map` waiting lines use those outside and review rows.
- [x] `change`, `act`, and `run` paste the printer stdout first when they refuse to activate or flip a banner for a node that has a recorded wait.

## Advise pins (reviews/2026-10-28-advise.md)

- [x] Deferred link: the node points to a deferred bead with a `related` dep (`bd dep add <node> <deferred> -t related`). The printer finds deferred items through that dep.
- [x] `status` Blocked keeps `waiting on <id>` and names no project when the export can't be read.
- [x] A node id missing from the export prints unreadable (or its own line), never `No outside wait recorded`.
- [x] An `outside` bead missing `project:` or `external:` prints id + title with the field marked missing. No project from the title.
- [x] The local bead's description `external:` is the printed value. The node-level `external:` dep is a mirror.
- [x] When a verb refuses for another reason (grant, stale contract, advise), its own reason line comes right after the card.
