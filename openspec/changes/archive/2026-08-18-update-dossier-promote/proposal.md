# update-dossier-promote

> **ACTIVE BUILD**

**Rigor:** change

Activated 2026-08-18 (`/activate` after intend `bazaar-yp8`).

## Why

`add-dossier-promote` still sits on `bazaar-db8.4` as “dossier
becomes a Project.” Advise and ADR-007 rejected that 1:1 consume.
The living emerge rule is already true; the landing id and the
tracker still speak the rejected rule. That lie will be implemented
if we leave it.

## What

- The landing `add-dossier-promote` means emerge-with-provenance
  (mint or select an intention that cites the dossier).
- It does not mean the dossier becomes a project or is consumed.
- `intend --extract-from` naming a dossier is an emerge path under
  this rule, not a second promote.
- Retitle `bazaar-db8.4` to match.
- Capability: MODIFIED `dossier`.

## Impact

- Capabilities: MODIFIED `dossier`
- ADRs: none (ADR-007 already accepted)

## User journey & surfaces

Duke, from the tracker or a stranger reading the landing id.

1. Opens `bazaar-db8.4` or the living `dossier` spec.
2. **Working** — title and requirement say emerge-with-cite.
3. **Empty** — no promote implementation yet; the rule is still the
   rule.
4. **Failed** — a change treats promote as rename-into-a-project;
   rejected against the living requirement.
5. **Off** — bead still says “becomes a Project”; that is this
   change’s debt.

`No new UI because` the surfaces are `bazaar-db8.4` and
`openspec/specs/dossier/spec.md`.

## Out of scope

- Implementing gather — `bazaar-db8.3`
- Dossier id on `--extract-from` — `add-intend-extract-dossier`
- Host projection / UI — `bazaar-db8.2`, `bazaar-db8.5`
- Bytes store — `bazaar-ja7`
