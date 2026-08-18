## ADDED Requirements

### Requirement: Sectioned paste is a face of existing objects

A paste of sectioned text SHALL parse into existing work objects. A
gathering or description category SHALL map to a dossier’s
self-description and citations. An intention or intend-dag category
SHALL mint or select intentions and their work nodes. A task
category SHALL map to work nodes. The parse SHALL NOT introduce a
new document work-object kind.

#### Scenario: A gathering section is pasted

- GIVEN a paste whose category is a gathering or description section
- WHEN it is parsed
- THEN it updates a dossier’s self-description or citations
- AND it does not become a work node solely because it was pasted

#### Scenario: An intend-dag section is pasted with a gathering

- GIVEN a paste that includes a gathering section and an intention
  or intend-dag section
- WHEN it is parsed
- THEN each intend-dag item is an intention and its work nodes
- AND no new kind is created for “parsed document”

#### Scenario: A lone task section is pasted

- GIVEN a paste whose only category is a task section, with no
  gathering and no named dossier
- WHEN it is parsed
- THEN each item is a work node (or an attribute on one)
- AND no dossier is created
- AND no new kind is created for “parsed document”

### Requirement: Mixed paste keeps provenance

When a paste contains a gathering category, or names an existing
dossier, together with an intention or intend-dag category, those
intention items SHALL be minted or selected from that dossier and
SHALL cite it (ADR-007). Work nodes parsed from that section SHALL
belong to those intentions. A paste that contains only a task
category SHALL map to work nodes and SHALL NOT invent a dossier.
Intentions minted with no gathering and no named dossier SHALL NOT
be recorded as emerged from a dossier.

#### Scenario: Mixed paste of gathering and intend-dag

- GIVEN a paste with a gathering section and an intend-dag section
- WHEN it is accepted
- THEN a dossier is updated from the gathering
- AND each intend-dag intention cites that dossier
- AND the dossier is not consumed

#### Scenario: Mixed paste drops the cite

- GIVEN a proposal parses a mixed gathering + intend-dag paste into
  a dossier and work nodes that do not cite it
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: Lone task section invents a dossier

- GIVEN a paste that is only a task section
- WHEN a change records a new dossier for it
- THEN it is rejected against this requirement

### Requirement: Attributes and bytes are different persistences

Parsed attributes SHALL persist with the object they mapped to.
Pasted bytes and cited artifacts SHALL be citations to the store
named by `bazaar-ja7`. This capability SHALL NOT add a blob store.

#### Scenario: An attribute is parsed

- GIVEN a task or intend-dag section names an attribute the mapped
  object already has
- WHEN the paste is accepted
- THEN that attribute is stored on that object
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
