## MODIFIED Requirements

### Requirement: Work objects are the named kinds

The method SHALL talk in these objects: intention, capability, change,
work node, agent, evidence, learning, dossier. A project SHALL NOT be
a separate work-object kind: it is a named graph (an intention and its
work nodes with a public address). Values SHALL be named preferences a
project carries, not a work-object kind. Documents SHALL be how some
of them are shown, not a parallel store.

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
