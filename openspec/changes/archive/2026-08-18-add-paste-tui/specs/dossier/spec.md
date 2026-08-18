## ADDED Requirements

### Requirement: A sibling TUI may submit a paste

A sibling paste TUI MAY send sectioned text to the host’s parse and
persist surface and show the resulting records. It SHALL NOT be the
authoritative store. It SHALL remain a client of this face.

#### Scenario: A fixture is piped with save

- GIVEN a valid intend-DAG or sectioned fixture on stdin
- WHEN the TUI runs with save
- THEN it shows the parsed records
- AND the host stores a projection id
- AND the TUI does not keep a second database of those records
