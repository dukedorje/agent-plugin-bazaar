## ADDED Requirements

### Requirement: A dossier or parsed record is not a ready-set row

When a host presents a dossier or parsed records, it SHALL NOT place
them in the derived ready set unless they are open work nodes whose
dependencies have landed. Signal colour SHALL remain reserved for
ready work nodes. A card or document view SHALL NOT replace `/` as
the ready-set.

#### Scenario: A gathered dossier is shown

- GIVEN a host can show a dossier
- WHEN the ready set is computed
- THEN the dossier is not a ready row
- AND `/` still lists only startable work nodes

#### Scenario: Cards are proposed on `/`

- GIVEN a change puts parsed-record cards on `/` as the primary page
- WHEN it is reviewed
- THEN it is rejected against this requirement
