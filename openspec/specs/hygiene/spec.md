# hygiene

G1 measuring stick. Folded from `add-hygiene-check` on 2026-08-15.

Enforces a few living-specs properties mechanically. It does not grade
journey quality. Empty allowlists; adding a name is a visible edit.

## Purpose

A convention with no check is decoration. This script is the check.

## ADDED Requirements

### Requirement: In-flight banners

`python3 scripts/check-hygiene.py` SHALL fail when an
`openspec/changes/<id>/proposal.md` (not under `archive/`) lacks a
`PENDING`, `ACTIVE BUILD`, or `PARKED` banner in the first 40 lines.

#### Scenario: Path is not status

- GIVEN a change directory with no banner in proposal.md
- WHEN the check runs
- THEN it exits non-zero

### Requirement: Fold-debt is empty

An `ACTIVE BUILD` change still under `openspec/changes/` (not `archive/`)
SHALL fail when it has no open owed checkbox. That includes all owed
boxes `[x]`, a missing `tasks.md`, and a `tasks.md` with no checkbox
syntax. A `PENDING` change SHALL fail only when owed boxes exist and
are all `[x]`. `FOLD_DEBT_ALLOWLIST` SHALL start empty.

#### Scenario: Shipped-looking change

- GIVEN all owed boxes checked and the dir still in `changes/`
- WHEN the check runs
- THEN it exits non-zero

#### Scenario: Lie by omission

- GIVEN an ACTIVE BUILD change with no `tasks.md`
- WHEN the check runs
- THEN it exits non-zero

### Requirement: Journey or no-new-UI

PENDING and ACTIVE BUILD proposals SHALL fail the check unless they
contain `## User journey` or `No new UI because`.

#### Scenario: Active proposal with neither

- GIVEN `> **ACTIVE BUILD**` and no journey sentence
- WHEN the check runs
- THEN it exits non-zero

### Requirement: Checkboxes are owed

The check SHALL fail a checkbox whose heading or text is out-of-scope,
handoff, or not-in-this-change, and SHALL fail stall phrasing
(`someday`, `nice to have`, …).

#### Scenario: Out-of-scope as a box

- GIVEN `- [ ] the adjacent thing` under `## Out of scope`
- WHEN the check runs
- THEN it exits non-zero

### Requirement: Discriminating fixtures

`scripts/test-hygiene.sh` SHALL pass the live tree and SHALL fail the
no-banner, fold-debt, fold-debt-no-tasks, fold-debt-prose, no-journey,
scope-box, findings-box, and stall fixtures. `validate.sh` SHALL run
this harness, not only the live tree.

#### Scenario: A broken check still greens the live tree

- GIVEN a regression that accepts fold-debt
- WHEN `test-hygiene.sh` runs
- THEN it fails on the fold-debt fixture even if the live tree is empty
