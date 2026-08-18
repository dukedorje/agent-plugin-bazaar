# add-paste-grammar — wire format

Sibling implementation: `taskmaster-web/src/lib/paste.ts`.
This file is reasoning. The living SHALL is “deterministic + title
required.”

## Categories

A level-1 or level-2 ATX heading whose first word (case-insensitive)
is one of:

| Heading | Category |
|---|---|
| `gathering`, `description`, `dossier` | gathering |
| `intend`, `intention`, `intend-dag`, `dag` | intend |
| `task`, `tasks` | task |

Any other category heading fails the parse.

## Items

`### id-or-title` starts an item. The heading text is required
(trim, non-empty). Attributes are `- key: value` lines.

- Gathering body before any `-` / `###` is the self-description.
- `- cite: url` or `- cite: label | url` is a citation.
- `- id:` on gathering names the dossier record.
- In intend: `- kind: intention` or no `needs` → intention.
  `- kind: node` or `- needs:` → work node, attached to the most
  recent intention in the paste.
- In task: every item is a work node. No dossier is created.
- `- select: <id>` marks select-not-mint. The parse does not write
  the tracker.

## Mixed paste

If a gathering section is present (or `- dossier: <id>` names one),
every intention from an intend section cites that dossier.

## Failures

- Unknown category heading
- `###` with empty title
- Empty input
