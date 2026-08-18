# add-paste-objects — settlements

Architecture write. Act copies these into ADR-008. It does not reopen
them. Kinds, Project, Values, and emerge/provenance were settled in
ADR-007 (`add-dossier-objects`, folded).

Amended after advise send-back (2026-08-18): mixed paste keeps
provenance; a lone task section does not invent a dossier.

## Why a face

Without a named parse face, `add-paste-grammar` invents the mapping
and the leftover `task` table becomes the product. This change names
the face. It does not write a parser.

## Settled

1. **Parsed records are a face of existing objects.** A gathering
   section maps to a dossier’s self-description and citations. An
   intention or intend-dag section mints or selects intentions and
   their work nodes. A task section maps to work nodes. Not a new
   document kind.

2. **Mixed paste keeps ADR-007 provenance.** Gathering (or a named
   existing dossier) plus intention / intend-dag in the same paste
   means those intentions emerge from that dossier and cite it.
   Their work nodes belong to those intentions. Independent
   category piles that drop the cite are a defect.

3. **A lone task section does not invent a dossier.** Task items
   become work nodes. No gathering and no named dossier means no
   emerge record. Those work nodes are not “emerged from a dossier.”

4. **Authoritative store is the kernel tracker** (and the dated
   export a host consumes) for work nodes. A host may later project
   a dossier in SQLite. A TUI-local DB is not a source of truth.
   Taskmaster does not become a second kernel.

5. **The TUI is a sibling client** of this face. Claude Code / Prime
   *feel* is a sketch input for `add-paste-tui`. It is not an agent
   host and does not unpark Prime or MetaDev.

6. **The leftover `task` table is not this face.** It is scaffold.
   Do not extend it into a ticket tracker.

7. **Cards are a document view.** `/` stays the ready-set. Signal
   colour still means READY and nothing else.

8. **Attributes vs bytes.** Parsed attributes persist with the
   object they mapped to. Pasted bytes and cited artifacts wait on
   `bazaar-ja7`. This change does not pick G Brain / MetaCoding /
   Dreamballs.

## Why not the other forks

- New document type: store number four under another name.
- Independent mappings that skip the cite: silent provenance loss
  against ADR-007.
- Inventing a dossier from a lone task list: a ticket table under
  another name.
- TUI-local authority: two truths, and the host’s export law dies.
- Promote the scaffold `task` table: PRODUCT already refuses a
  ticket tracker.
- Cards on `/`: replaces the ready-set, which was a stated non-goal.
