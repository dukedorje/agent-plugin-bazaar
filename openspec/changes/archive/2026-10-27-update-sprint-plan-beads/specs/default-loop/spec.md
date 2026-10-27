## ADDED Requirements

### Requirement: A story is a bead and a checkbox

Intake SHALL record each story as a bead with acceptance criteria.
The parent change's `tasks.md` SHALL carry one checkbox per story
acceptance. Intake SHALL NOT write `stories/*.md` or a story template
file. Beads materialization SHALL run at the end of intake without a
separate flag.

#### Scenario: Decomposition finishes

- GIVEN a change directory and a decomposed story list
- WHEN intake records the stories
- THEN each story is a bead
- AND each acceptance line is an open checkbox in `tasks.md`
- AND no `stories/` directory is created

#### Scenario: Ready queue

- GIVEN those beads are unblocked
- WHEN someone asks what to work on
- THEN `bd ready` lists them
