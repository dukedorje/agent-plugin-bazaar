## ADDED Requirements

### Requirement: advise is the read between change and act

`advise` SHALL load an in-flight change, assign a review-pair from
`ladder.json` (`architecture-review` reader, optional Fable consult),
and write `openspec/changes/<id>/reviews/<date>-advise.md` plus a
signed result with `permission: read`. It SHALL NOT edit product
paths, fold, or implement nits. Verdict SHALL be `accept`,
`accept-with-nits`, or `send-back`. `send-back` SHALL add owed boxes
on the change and SHALL NOT flip the banner. The change author SHALL
NOT be the sole accepting reader.

#### Scenario: Architecture change after scaffold

- GIVEN `openspec/changes/add-buzz-local-client/` is ACTIVE BUILD
- WHEN `advise` runs
- THEN a review file exists under `reviews/`
- AND no file under `lib/` or `native/` was edited

#### Scenario: Send-back blocks act

- GIVEN the last advise verdict is `send-back`
- WHEN `conductor.py ready` lists implement nodes of that change
- THEN they are not `dispatchable`

## MODIFIED Requirements

### Requirement: Shared references, not four surfaces

The skills `intend`, `change`, `advise`, `act`, `fold`, `brief`, and
`ready` SHALL load `plugins/intention/references/shared.md` and
SHALL NOT restate packet fields or topology wirings. Adding a tenth
law to a skill body instead of `docs/contracts/` is a defect.

#### Scenario: Packet field lookup

- GIVEN an agent running `act` needs the `capability` rule
- WHEN they follow the skill
- THEN they are sent to `docs/contracts/agent-surface.md`, not a
  second field table inside `act/SKILL.md`
