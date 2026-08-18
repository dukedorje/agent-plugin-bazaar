## MODIFIED Requirements

### Requirement: Intentions emerge from a dossier with provenance

An intention MAY be minted or selected from a dossier. One dossier
SHALL be allowed to give rise to many intentions over time. Each
emerged intention SHALL cite the dossier. It MAY cite specific assets
already cited on the dossier. Those citations SHALL be the
provenance. Emergence SHALL NOT mutate the dossier into an intention
or a project, consume the gathering, copy bytes into a new store, or
introduce a second task-packet or signed-result shape.

The landing id `add-dossier-promote` SHALL mean this emerge. It SHALL
NOT mean the dossier becomes a project. `intend --extract-from`
naming a dossier SHALL be an emerge path under this requirement, not
a second promote rule.

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

#### Scenario: Promote landing means emerge

- GIVEN the landing id `add-dossier-promote` or tracker title
  `bazaar-db8.4`
- WHEN a reader asks what that landing does
- THEN it is mint or select of an intention that cites the dossier
- AND it is not “the dossier becomes a project”

#### Scenario: Extract-from a dossier is emerge

- GIVEN `intend --extract-from` names a dossier
- WHEN an intention is minted from that run
- THEN the intention cites the dossier
- AND the gathering remains
- AND no second promote rule is invented
