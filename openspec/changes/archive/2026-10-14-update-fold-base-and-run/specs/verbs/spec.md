## MODIFIED Requirements

### Requirement: intend default next is steer

After emitting the DAG, `intend` SHALL pin current, print a decision
briefing, and hand off to `steer` unless the human named `--go`,
“don't pause”, or `--autonomous`. `--ask` / “run it by me” SHALL
remain a pause with no `act`. “Activate this set” and “activate what we
just intended” SHALL record campaign authority on the root (bead or chat
DAG) and SHALL walk `change` then `advise` until contracts are ready,
then pause for map and briefing. “Run this whole intention” and a grant
followed by “and run” (including “activate this set and run”) SHALL
record that same authority and SHALL imply `--go` for that intention:
after contracts are ready the session SHALL enter `run` and SHALL NOT
pause for a second utterance. Explicit `--ask`, `--plan`, `--advise`,
`--wait`, `--tidy`, and `--pause-before` SHALL still win. `--go` and
`--autonomous` SHALL NOT themselves grant activation. `intend` SHALL NOT fold.

#### Scenario: Bare intend pauses at steer

- GIVEN `intend` finished a DAG with an architecture or human-gate node
- WHEN no `--go` / `--autonomous` was named
- THEN next is `steer` with a decision briefing
- AND no write `act` has started

#### Scenario: Activate this set then pause

- GIVEN the human said “activate this set” after intend
- WHEN change/advise for dependency-ready nodes in scope has finished
- THEN campaign authority is recorded
- AND the session pauses with map + briefing
- AND `run` has not started

#### Scenario: And run does not pause after contracts

- GIVEN the human said “activate this set and run” or “run this whole intention”
- WHEN change/advise for dependency-ready nodes in scope has finished
- THEN campaign authority is recorded
- AND the session enters `run` without waiting for another utterance
- AND an explicit `--wait` or `--ask` still stops on its own rule

### Requirement: fold archives

`fold` SHALL apply deltas to `openspec/specs/`, move the change to
`openspec/changes/archive/YYYY-MM-DD-<id>/`, amend `ARCHITECTURE.md`
when shape changed, and append surprises to `docs/LEARNINGS.md`. It
SHALL refuse PENDING and PARKED. Before applying a `MODIFIED` or
`REMOVED` requirement, `fold` SHALL compare that requirement's text in
the working tree with its text in the base blob recorded on the block.
When they differ, `fold` SHALL apply nothing from that change and SHALL
leave the change directory in place. A missing base comment SHALL NOT
refuse during the release that introduces the check. The folder SHALL
diff an unstamped requirement by hand and record the base before applying
when the paste still matches.

#### Scenario: Active change after act

- GIVEN `openspec/changes/<id>/` is ACTIVE BUILD and owed tasks are done
- WHEN `fold` finishes
- THEN `openspec/changes/<id>/` is gone, the archive directory exists,
  and every SHALL from the deltas appears in `openspec/specs/`

#### Scenario: Stale paste is not applied

- GIVEN an ACTIVE BUILD change whose MODIFIED block records a base blob
- AND that living requirement's text has changed since the blob
- WHEN `fold` runs
- THEN it applies nothing from that change
- AND the change directory stays under `openspec/changes/`

## ADDED Requirements

### Requirement: Stale fold base is change, not fold

A `MODIFIED` or `REMOVED` requirement whose recorded base blob does not
match that requirement's text now SHALL NOT be fold-legal. On `roll`,
`ask`, and `--until fold`, `run` SHALL set `next` to `change` for that
id, with reason `stale-base`, and SHALL NOT set `next` to `fold`. The
same campaign SHALL re-paste the requirement from the living spec before
folding it. The re-paste SHALL keep clauses that exist now and that this
change did not mean to remove. `--skip` SHALL NOT turn that id into
advise. A missing base comment SHALL leave the change fold-legal for
this release. An architecture or instrument contract whose re-paste
changes the contract SHALL owe `Fresh advise after preparation`. A clean
fold-legal change SHALL still fold ahead of a stale one.

#### Scenario: Stale paste returns to change

- GIVEN roll, and an ACTIVE BUILD change whose owed boxes are checked
- AND its MODIFIED requirement's base blob differs from the living text
- WHEN `run` observes
- THEN `next` is `change` and the reason is `stale-base`
- AND `stop` is not set

#### Scenario: A clean fold still goes first

- GIVEN roll, one stale fold-legal change, and one clean fold-legal change
- WHEN `run` observes
- THEN `next` is `fold` and the focus is the clean change
