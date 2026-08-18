## ADDED Requirements

### Requirement: Paste parse is deterministic

Parsing the same sectioned paste SHALL produce the same records.
An item with a missing title SHALL fail the parse. The command and
fixtures that witness this SHALL live in the Taskmaster sibling
app’s tree, not as a framework `SHALL` in this marketplace.

#### Scenario: Mixed fixture is stable

- GIVEN the mixed gathering + intend-dag fixture
- WHEN the focused parse command runs twice
- THEN both runs emit the same intentions
- AND those intentions cite the dossier from the gathering

#### Scenario: Lone task fixture invents no dossier

- GIVEN the lone-task fixture
- WHEN the focused parse command runs
- THEN work nodes are present
- AND no dossier record is produced

#### Scenario: Empty title fails

- GIVEN a paste whose item heading is empty
- WHEN it is parsed
- THEN the parse fails
- AND no records are accepted
