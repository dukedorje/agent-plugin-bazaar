## ADDED Requirements

### Requirement: Dossier is a work object

A dossier SHALL be a work object: the gathering corpus that exists
before an intention has much identity. It SHALL hold a self-description
and citations. It SHALL NOT replace intention, capability, change,
work node, agent, evidence, or learning.

#### Scenario: Gathering has no intention yet

- GIVEN a self-description and cited artifacts for a thing that is
  not yet a named graph
- WHEN the method names that corpus
- THEN it is a dossier
- AND it is not an intention and not a work node

### Requirement: Project is the named graph

A project SHALL be the named graph an intention already is: that
intention and its work nodes with a public address. Promoting a
dossier SHALL address that graph and cite the dossier. Promotion
SHALL NOT mutate the dossier into a project or drop the gathering.

#### Scenario: A gathered dossier is promoted

- GIVEN a dossier with a self-description
- WHEN it is promoted
- THEN a project address exists
- AND the dossier remains citable

### Requirement: Values are named preferences

Values (including the spoken name “Value Function”) SHALL be named
preferences a project carries. A project SHALL be breakable into
intentions together with those values. They SHALL NOT be a
work-object kind, a score, or a function runtime in this capability.

#### Scenario: A project carries a value

- GIVEN a project
- WHEN someone names a preference it should hold
- THEN that name is a value on the project
- AND no function is evaluated

#### Scenario: A project is broken down

- GIVEN a project that has been addressed from a dossier
- WHEN it is split
- THEN the split may name intentions and values
- AND neither the values nor a “value function” become a new
  work-object kind

### Requirement: Self-description is not identity

A dossier’s self-description MAY seed a project’s public lede. It
SHALL NOT become the project’s identity. A project’s identity SHALL
be its public address.

#### Scenario: Self-description is rewritten

- GIVEN a promoted dossier whose self-description later changes
- WHEN a reader asks what the project is
- THEN they use the public address
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
