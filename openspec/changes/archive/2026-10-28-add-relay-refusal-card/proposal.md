# add-relay-refusal-card

> **ACTIVE BUILD**

**Rigor:** architecture

## Why

Asking to activate a node, or to flip its banner, can be refused for a reason that lives in another repository. The refusal is right. The reason shows up only after a drill: a long note that separates an internal lock from identikey-protocol, Tokenator, Mjolnir, and IKEYW, then says the next change inside this repo is still allowed. The next session drills again. `status` prints `waiting on <id>` and stops there.

## What

- A refusal to activate a node or flip its banner starts with a card read from beads. The card names each outside project, the outcome that project owes, and a bead or `external:<project>:<capability>` reference.
- The same rows appear on `status` Blocked and on `map` when a node is waiting.
- A human review that is not a repository is its own section. An internal lock and a deferred item print under Separate, so they are not mistaken for the outside wait.
- An outside row names the action it blocks. A refusal of a different action does not list that row as the cause.

## Impact

- Capabilities: ADDED verbs (refusal card).
- ADRs: none

## User journey & surfaces

The operator asks `change` or `act` to activate a node or flip its banner, or reads `status` / `map`.

Working: the reply opens with the card. Each outside line has the project, one sentence, the local bead id, and the `external:` ref. A review line names the gate and its reason. Separate lists the internal lock and anything deferred. A second refusal prints that same card.

Empty: the node has no outside bead, no review gate, and no internal or deferred marker. The printer says there is no recorded outside wait. It does not invent a project.

Failed: beads export cannot be read. The printer says the record could not be read and names the node. It does not guess which project is blocking.

Off: a refusal for a missing grant, a stale contract, or an unaccepted advise read stays that refusal. The card is added only when the node has recorded waits. The card does not flip the banner and does not unlock the blocked action.

## Preparation

- Inputs: the chat DAG `relay-refusal-card`. A throwaway beads database on 2026-10-28. `bd export` keeps `depends_on_id: external:<project>:<capability>`. `bd ready` and `bd blocked` leave an external-only edge off the blocked list, and the issue stays ready. A task cannot block an epic, and an epic cannot block a task. `bd gate create --type=human` blocks a task. The same gate issue is created for an epic and the blocks edge is rejected.
- Outcome: revised. The chat design treated the `external:` edge as the ready blocker. This `bd` does not. The sentence and the ready edge are a same-type local bead. The `external:` id is the reference on that bead.
- Authority: the user said "activate and run" on 2026-10-28. Scope is this change. It does not file the api-proxy waits and it does not unlock `POST /v1/execute`.

## Out of scope

- Filing identikey-protocol, Tokenator, Mjolnir, or IKEYW beads in api-proxy.
- Teaching `bd ready` to honor `external:` edges. That is beads itself.
- Unlocking live secret-use or flipping a banner the card says stays put.
