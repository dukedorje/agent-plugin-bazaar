# add-paste-objects — settlements

Architecture write. Act copies these into ADR-008. It does not reopen
them. Kinds, Project, and Values were settled in `add-dossier-objects`.

## Settled

1. **Parsed records are a face of existing objects.** A task /
   intend-dag section maps to work nodes. A gathering section maps to
   a dossier’s self-description and citations. Not a new document
   kind.

2. **Authoritative store is the kernel tracker** (and the dated
   export a host consumes) for work nodes. A host MAY later project a
   dossier in SQLite. A TUI-local DB SHALL not be a source of truth.
   Taskmaster does not become a second kernel.

3. **The TUI is a sibling client** of this face. Claude Code / Prime
   *feel* is a sketch input for `add-paste-tui`. It is not an agent
   host and does not unpark Prime or MetaDev.

4. **The leftover `task` table is not this face.** It is scaffold. Do
   not extend it into a ticket tracker.

5. **Cards are a document view.** `/` stays the ready-set. Signal
   colour still means READY and nothing else.

6. **Attributes vs bytes.** Parsed attributes persist with the object
   they mapped to. Pasted bytes and cited artifacts wait on
   `bazaar-ja7`. This change does not pick G Brain / MetaCoding /
   Dreamballs.

## Why not the other forks

- New document type: store number four under another name.
- TUI-local authority: two truths, and the host’s export law dies.
- Promote the scaffold `task` table: PRODUCT already refuses a ticket
  tracker.
- Cards on `/`: replaces the ready-set, which was a stated non-goal.
