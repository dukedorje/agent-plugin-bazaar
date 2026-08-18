## MODIFIED Requirements

### Requirement: Work objects are the named kinds

The method SHALL talk in these objects: intention, capability, change,
work node, agent, evidence, learning, dossier. A project SHALL NOT be
a separate work-object kind: it is a named graph (an intention and its
work nodes with a public address). Values SHALL be named preferences a
project carries, not a work-object kind, not a work node, and not a
ready-set row. A project SHALL be breakable into intentions together
with those values. A dossier SHALL be allowed to give rise to many
intentions over time; those intentions SHALL cite the dossier.
Documents SHALL be how some of them are shown, not a parallel store.

#### Scenario: Status in a path

- GIVEN a change directory named as if it were done
- WHEN an agent decides whether the behavior exists
- THEN they read the living spec and the in-file banner, not the path

#### Scenario: Stranger asks what a dossier is

- GIVEN this change has folded
- WHEN they look for the gathering that sits before an intention
- THEN they find `dossier` as a work object in `working-method` or in
  the `dossier` living spec, not only an epic or a host table

#### Scenario: Project proposed as a new kind

- GIVEN a change adds Project as a work-object kind beside intention
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: Values proposed as a new kind

- GIVEN a change adds Value or Value Function as a work-object kind
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: Values proposed as work nodes

- GIVEN a change makes a named value a work node or a ready-set row
- WHEN it is reviewed
- THEN it is rejected against this requirement

#### Scenario: A project is broken down

- GIVEN a project whose intention emerged from a dossier
- WHEN it is split
- THEN the split may name intentions and values
- AND those values stay named preferences, not a new kind
- AND those values are not work nodes and do not enter the ready-set

#### Scenario: Several intentions cite one dossier

- GIVEN a dossier from which one intention has already emerged
- WHEN another intention is named from the same gathering
- THEN both are intentions
- AND both cite the dossier
- AND the dossier is still a dossier
