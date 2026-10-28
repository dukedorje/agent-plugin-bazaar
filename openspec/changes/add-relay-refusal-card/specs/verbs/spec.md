## ADDED Requirements

### Requirement: A refusal names the outside project

When `change`, `act`, or `run` refuses to activate a node or flip its banner, and that node has a recorded outside wait, review, internal lock, or deferred item, the reply SHALL start with the stdout of `plugins/intention/skills/status/scripts/refusal.py` for that node and action. The reply SHALL NOT replace that stdout with a fresh account of the same waits.

The printer SHALL read dependency edges from a beads export. An outside wait SHALL be an open bead of the same issue type as the node, labeled `outside`, blocking the node, whose description names `project:`, `external: external:<project>:<capability>`, and an optional `blocks:` list. The card line SHALL show the project, the bead title, the local bead id, and that `external:` id. An `upstream:` line in the description SHALL be printed when present and SHALL NOT be invented when absent.

A human gate that blocks a task SHALL print under Review with its reason. An epic SHALL record that review as a same-type bead labeled `review`, because a gate issue cannot block an epic. A same-type blocker labeled `internal`, and a same-type bead labeled `deferred` with no blocks edge, SHALL print under Separate.

A row whose `blocks:` list does not include the refused action SHALL print under Separate. An empty `blocks:` SHALL refuse activation of the node. The printer SHALL NOT flip a banner, close a bead, or decide that the verb must refuse.

`status` Blocked and `map` waiting lines SHALL use the same outside and review rows for those beads. `bd ready` on this beads version SHALL NOT be treated as proof that an `external:` edge is clear. The ready edge SHALL be the local bead.

When the export cannot be read, the printer SHALL say the record could not be read and SHALL name no project. When the node has no recorded wait, the printer SHALL say that no outside wait is recorded.

#### Scenario: Live activation lists the other projects

- GIVEN node `gwk` blocked by four same-type `outside` beads for identikey-protocol, Tokenator, Mjolnir, and IKEYW, each with an `external:` id and `blocks: live-execute`
- AND a human gate whose reason is an independent security review
- AND an `internal` blocker and a `deferred` bead
- WHEN activation of live-execute is refused
- THEN the card lists those four projects with their bead ids and `external:` ids under Outside
- AND the review is not described as a repository
- AND the internal lock and the deferred item are under Separate
- AND the card says this refusal does not unlock live-execute

#### Scenario: A different action is not blamed on those projects

- GIVEN the outside beads in the previous scenario name `blocks: live-execute`
- WHEN the refused action is `banner-flip`
- THEN those four rows print under Separate
- AND they are not the Outside cause of the banner refusal

#### Scenario: The next refusal reprints the card

- GIVEN the card has already been printed for `gwk` and live-execute
- WHEN a later turn refuses the same node and action
- THEN the stdout is the same card
- AND the reply does not add a second explanation of those projects

#### Scenario: An unreadable record names no project

- GIVEN beads export fails for the node
- WHEN the printer runs
- THEN the line says the record could not be read
- AND no project name appears

#### Scenario: Status shows the same outside row

- GIVEN `status` lists the node under Blocked because an `outside` bead blocks it
- WHEN the board prints
- THEN that line names the project, the local bead, and the `external:` id
