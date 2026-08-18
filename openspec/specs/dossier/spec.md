# dossier

What **is** built: Dossier is a work object — a gathering of a
self-description and citations. Project is the named graph, not a
kind. Values are named preferences, not ready-set rows. Intentions
emerge from a dossier with provenance; the gathering is not consumed.
A sectioned paste is a face of those objects: mixed paste cites;
a lone task list invents no dossier. The parse is deterministic; the
fixture lives in the Taskmaster sibling app. Folded from
`add-dossier-objects` (ADR-007), `add-paste-objects` (ADR-008), and
`add-paste-grammar` on 2026-08-18.

This spec is stack-neutral. Framework, TUI toolkit, language, driver,
and look tokens are not requirements here.

## Purpose

Name the gathering that sits before an intention, and the rule by
which intentions come out of it, so a host cannot invent a ticket
table or a fourth store.

## Requirements

### Requirement: Dossier is a work object

A dossier SHALL be a work object: the gathering corpus of a
self-description and citations. It MAY exist before any intention. It
SHALL remain after intentions emerge from it. It SHALL NOT replace
intention, capability, change, work node, agent, evidence, or
learning.

#### Scenario: Gathering has no intention yet

- GIVEN a self-description and cited artifacts for a thing that is
  not yet a named graph
- WHEN the method names that corpus
- THEN it is a dossier
- AND it is not an intention and not a work node

#### Scenario: Gathering after an intention has emerged

- GIVEN a dossier from which an intention has already emerged
- WHEN a reader asks what the gathering is
- THEN it is still a dossier
- AND it is not that intention

### Requirement: Project is the named graph

A project SHALL be the named graph an intention already is: that
intention and its work nodes with a public address. A dossier SHALL
NOT be a project. This marketplace SHALL NOT mint public addresses;
a host MAY show one.

#### Scenario: An emerged intention is addressed

- GIVEN an intention that emerged from a dossier
- WHEN that intention’s graph has a public address
- THEN that named graph is a project
- AND the dossier is not that project

### Requirement: Intentions emerge from a dossier with provenance

An intention MAY be minted or selected from a dossier. One dossier
SHALL be allowed to give rise to many intentions over time. Each
emerged intention SHALL cite the dossier. It MAY cite specific assets
already cited on the dossier. Those citations SHALL be the
provenance. Emergence SHALL NOT mutate the dossier into an intention
or a project, consume the gathering, copy bytes into a new store, or
introduce a second task-packet or signed-result shape.

#### Scenario: First intention emerges

- GIVEN a dossier with a self-description and citations
- WHEN an intention is minted from it
- THEN that intention exists
- AND it cites the dossier
- AND the dossier remains citable

#### Scenario: A second intention emerges later

- GIVEN a dossier from which one intention has already emerged
- WHEN a second intention is minted from the same gathering
- THEN both intentions exist
- AND both cite the dossier
- AND the dossier is not consumed

#### Scenario: Emergence without provenance

- GIVEN a proposal records an intention as emerged from a dossier
- WHEN that intention does not cite the dossier
- THEN it is rejected against this requirement

#### Scenario: First intention consumes the dossier

- GIVEN a change treats emerge as “the dossier becomes the project”
  or otherwise consumes the gathering
- WHEN it is reviewed
- THEN it is rejected against this requirement

### Requirement: Values are named preferences

Values (including the spoken name “Value Function”) SHALL be named
preferences a project carries. A project SHALL be breakable into
intentions together with those values. They SHALL NOT be a
work-object kind, a work node, a ready-set row, a score, or a
function runtime in this capability.

#### Scenario: A project carries a value

- GIVEN a project
- WHEN someone names a preference it should hold
- THEN that name is a value on the project
- AND no function is evaluated

#### Scenario: A project is broken down

- GIVEN a project whose intention emerged from a dossier
- WHEN it is split
- THEN the split may name intentions and values
- AND neither the values nor a “value function” become a new
  work-object kind
- AND those values are not work nodes and do not enter the ready-set

### Requirement: Self-description is not identity

A dossier’s self-description MAY seed a project’s public lede. It
SHALL NOT become the project’s identity. A project’s identity SHALL
be its public address.

#### Scenario: Self-description is rewritten

- GIVEN a dossier from which an intention has emerged, whose
  self-description later changes
- WHEN a reader asks what that intention’s project is
- THEN they use the project’s public address
- AND they may still cite the dossier

### Requirement: Packet and result stay one surface

Dossier, project, and values SHALL NOT introduce a second task-packet
or signed-result shape. A dossier SHALL NOT be an agent: it does not
accept a task packet or sign a result. If a hosted product needs a
field the surface lacks, the change SHALL amend
`docs/contracts/agent-surface.md`.

#### Scenario: A host wants a dossier-only packet

- GIVEN a proposal adds a Taskmaster-only or dossier-only packet
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: Dossier proposed as an agent

- GIVEN a proposal treats a dossier as an agent or a group
- WHEN it is reviewed
- THEN it is rejected against this requirement

### Requirement: The capability is materialized by fold

The `dossier` capability SHALL exist under `openspec/specs/` only
after `add-dossier-objects` folds. Until then these requirements
SHALL remain a delta in `openspec/changes/`.

#### Scenario: Change is still in flight

- GIVEN `add-dossier-objects` has not been folded
- WHEN an agent resolves the `dossier` capability id
- THEN it resolves as a capability a change is ADDing, not as built
  behavior (ADR-002)

### Requirement: Stack is not a living-spec requirement

Living specs under `openspec/specs/` SHALL NOT contain requirements
naming a web framework, TUI toolkit, systems language, database
driver, or look tokens for dossier or project. Those decisions SHALL
live in a sibling sketch and carry no `SHALL` (ADR-002).

#### Scenario: Reader greps for Ratatui or SvelteKit

- GIVEN a reader searching `openspec/specs/` for a dossier stack
- WHEN they find nothing
- THEN they follow ADR-007 to the sibling sketches

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
