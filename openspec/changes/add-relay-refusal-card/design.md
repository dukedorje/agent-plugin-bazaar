# add-relay-refusal-card

## Record

Each outside wait is one open bead of the same type as the node it blocks. Tasks block tasks. Epics block epics. A gate issue cannot block an epic.

The local bead:

- Title: the one-line outcome owed elsewhere.
- Label: `outside`.
- Description, one field per line:

```
project: identikey-protocol
external: external:identikey-protocol:guild-holder
blocks: live-execute
upstream: ik-123
```

`upstream` is omitted when the other repo's bead id is unknown. The printer does not invent it.

`bd dep add <node> <local-bead>` is the edge `bd ready` honors. The same `external:` id is also stored as a dependency on the node when `bd dep add` accepts it. The printer reads `bd export` for that id. `bd blocked --json` is not the source. On this `bd`, an external-only dependency stays in `bd ready` and never appears in `blocked_by`.

A review that is not a repository:

- On a task, `bd gate create --type=human --blocks <node> --reason="…"`. The reason is the line.
- On an epic, a same-type bead labeled `review`, with the reason as its title, because a gate cannot block an epic.

An internal lock is a same-type blocker labeled `internal`. A deferred item is a same-type bead labeled `deferred` and is not a blocks edge. Both print under Separate.

`blocks:` lists the actions this row refuses, comma-separated. An empty `blocks:` means the row refuses activation of the node itself.

## Card

The printer is `plugins/intention/skills/status/scripts/refusal.py`. Invocation: `python3 <that-path> <node-id> --action <action>`. Stdout is the card. `change`, `act`, and `run` paste it as the first lines of a refusal when the node has any outside, review, internal, or deferred record. They do not paraphrase it and they do not research the waits again.

```
Refused: <id> stays as it is
Action: <action>
This refusal does not unlock <surface>.

Outside
- <project> · <title>
  <local-id> · <external>
  upstream: <id>          # only when recorded

Review
- <gate-or-bead-id> · <reason>

Separate
- internal · <id> · <title>
- deferred · <id> · <title>
```

`<surface>` is the `blocks:` value being refused, or the node id when the row has an empty `blocks:`. A row whose `blocks:` does not include `--action` moves to Separate.

No recorded waits: one line, `No outside wait recorded for <id>.` Unreadable export: one line, `Could not read beads for <id>.` No project names in either line.

## Surfaces

`status` Blocked replaces `waiting on <id>` with the outside and review lines when the blocker is an outside bead, a review bead, or a human gate. `map` uses those lines for a waiting dep of the same kind. Internal and deferred stay labeled as such.

The printer does not flip a banner, close a bead, or decide the refusal. The verb decides. The printer renders.
