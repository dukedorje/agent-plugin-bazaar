---
name: retro
description: >
  Write a retrospective for a body of work: an OpenSpec change, an epic,
  or a named set of beads. Reads the change, closed beads, git, LEARNINGS,
  and human chat. Optionally pulls a Conduit (Matrix) room. Does not
  implement, fold, or start the next plan.
  Triggers on: retro, retrospective, what did we learn, after-action.
user-invocable: true
argument-hint: "[<change-id | epic-id>] [--room=<matrix-room-id>] [--since=YYYY-MM-DD]"
model: opus
---

# retro

A retrospective is one write-up for a body of work. It says what was
attempted, what landed, what people actually said, and what the next
intend should carry. It is not `debrief` (that expands a single bead or
change after one act). It does not implement, fold, archive, or open
the next change.

## 1. Name the body of work

Use the argument if one was given.

- A change id: `openspec/changes/<id>/`, or
  `openspec/changes/archive/*-<id>/` if that is where it lives.
- An epic id: `bd show <id> --json` and its children.
- Neither: use the change or epic this session has been working. If
  that is still ambiguous, ask. Do not pick the newest folder.

`--since=YYYY-MM-DD` bounds `git log`. If omitted, start at the change
directory's first commit, or the epic's created date.

Partial work is a valid retro. Say what is still open. Do not wait for
every child to close, and do not look for an execution skill.

## 2. Read

Read these. Do not invent files that are not there.

1. **Change.** `proposal.md`, `design.md`, `tasks.md` when the directory
   exists. Note the disposition banner. An archived change is read-only.
2. **Beads.** The epic and its children (`bd children`, `bd show`).
   Close reasons, notes, and anything left open or blocked. Acceptance
   that is still unchecked in `tasks.md`.
3. **Git.** `git log --oneline --since=<date>` on the paths the notes
   and the change mention. Attribute a commit when the message names a
   bead id. Leave the rest as unattributed.
4. **`docs/LEARNINGS.md`.** Only lines that already touch this work.
   Do not rewrite the file.
5. **Human chat.** Use what the human has said in this session about
   the work, and any transcript they paste. Then, optionally, Conduit
   (section 3).

## 3. Conduit (optional)

Conduit is a Matrix homeserver. Pull a room only when the human asks
or passes `--room`. This is context, not a spec.

- Room id is required (`!room:server`). If they say "from Conduit" and
  do not name a room, ask which room. Do not call `/sync` across every
  room they belong to.
- Homeserver: `MATRIX_HOMESERVER`, else `http://127.0.0.1:8008`.
- Token: `MATRIX_ACCESS_TOKEN` in the environment. Never print it, never
  write it into the retro, never ask them to paste it into a file.
- Request, with the room id URL-encoded:

```
GET {MATRIX_HOMESERVER}/_matrix/client/v3/rooms/{roomId}/messages?dir=b&limit=40
Authorization: Bearer $MATRIX_ACCESS_TOKEN
```

Keep human text messages in the window. Skip notices, membership, and
reactions. If the variable is missing, the call fails, or they decline
a room, skip the room and write **Chat:** not connected, plus why
(no room, no token, or the HTTP error without headers).

## 4. Write

While `openspec/changes/<id>/` exists and is not archived, write
`openspec/changes/<id>/retrospective.md`.

Otherwise write the retro in chat. When they named an epic, also offer
to `bd note` the epic with the "Carry forward" lines. Do not edit an
archive. Do not create `.omc/`, `docs/sprints/`, `phase-state.json`, or
a second LEARNINGS store.

```markdown
# retro <id>

**Scope.** change | epic | both
**Window.** <since> … <today>
**Chat.** this session | Conduit room <id> | not connected (<why>)

## What we set out to do
Two or three sentences from the proposal or the epic. Cite the file.

## What landed
- <closed bead or commit>: <what is true now>

## What did not
- <open, blocked, or reverted>: <what is still true>

## What people said
Short quotes or paraphrases from this session and, when connected, the
room. Attribute a person when the message has a sender. If chat was
not connected, say so in one line.

## Carry forward
- <concrete line the next intend should start from>
- <one more, only if the sources support it>

## LEARNINGS candidates
- YYYY-MM-DD — <one hard-won fact> (`<file>`)
```

Three to five carry-forward lines is enough when the sources support
them. Fewer is fine. Append a LEARNINGS candidate only when they ask,
or when the fact is already the kind `docs/LEARNINGS.md` keeps (a
surprise, with a file).

## 5. Stop

Report the path you wrote, or say the retro is in chat. Do not open a
change, check a box, fold, or start planning the next body of work.
