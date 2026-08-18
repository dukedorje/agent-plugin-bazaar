## ADDED Requirements

### Requirement: Sectioned paste is a face of existing objects

A paste of sectioned text SHALL parse into existing work objects. A
task or intend-dag category SHALL map to work nodes. A gathering
category SHALL map to a dossier’s self-description and citations. The
parse SHALL NOT introduce a new document work-object kind.

#### Scenario: A task section is pasted

- GIVEN a paste whose category is a task or intend-dag section
- WHEN it is parsed
- THEN each item is a work node (or an attribute on one)
- AND no new kind is created for “parsed document”

#### Scenario: A gathering section is pasted

- GIVEN a paste whose category is a gathering or description section
- WHEN it is parsed
- THEN it updates a dossier’s self-description or citations
- AND it does not become a work node solely because it was pasted

### Requirement: Attributes and bytes are different persistences

Parsed attributes SHALL persist with the object they mapped to.
Pasted bytes and cited artifacts SHALL be citations to the store
named by `bazaar-ja7`. This capability SHALL NOT add a blob store.

#### Scenario: An attribute is parsed

- GIVEN a task section names an attribute the work node already has
- WHEN the paste is accepted
- THEN that attribute is stored on the work node
- AND the raw paste is not kept as a fourth knowledge store

#### Scenario: An image or article is cited

- GIVEN a gathering paste names an image or article
- WHEN the paste is accepted
- THEN the dossier records a citation
- AND the bytes live in the store `bazaar-ja7` chose, or the write
  waits on that sit-down

### Requirement: Authority stays in the kernel tracker

Authoritative work-node state SHALL remain the kernel tracker and the
dated export a host consumes. A host or a sibling TUI MAY project a
dossier or parsed records. Neither SHALL become a second kernel, a
TUI-local source of truth, or a stored ready-set.

#### Scenario: A TUI-local database is proposed as source of truth

- GIVEN a change makes a paste client’s database authoritative
- WHEN it is reviewed
- THEN it is rejected against this requirement

### Requirement: A leftover task table is not this face

A scaffold `task` table in a host SHALL NOT be treated as the parse
face, as a dossier, or as a work-node store.

#### Scenario: Someone extends the scaffold task table

- GIVEN Taskmaster’s leftover `task` table
- WHEN a change maps pasted records onto it as the product model
- THEN it is rejected against this requirement

### Requirement: A paste client is not an agent host

A sibling paste TUI SHALL be a client of this face. It SHALL NOT be
an agent host of ADR-001. It SHALL NOT unpark Prime or the MetaDev
overlay.

#### Scenario: The TUI is proposed as a third host

- GIVEN a change names the paste TUI as a host of the agent surface
- WHEN it is reviewed
- THEN it is rejected against this requirement
