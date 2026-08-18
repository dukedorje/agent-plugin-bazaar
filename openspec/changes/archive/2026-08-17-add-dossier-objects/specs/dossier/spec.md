## ADDED Requirements

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
