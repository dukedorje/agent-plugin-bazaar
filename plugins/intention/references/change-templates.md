# change templates

## proposal.md

First body line is the banner. Status lives in the file.

```markdown
# <change-id>

> **PENDING**

## Why
One paragraph.

## What
Bullets. Name capabilities touched.

## Impact
- Capabilities: ADDED / MODIFIED / REMOVED
- ADRs: none | will amend ARCHITECTURE.md

## User journey & surfaces
Who, from which existing surface, working / empty / failed / off.

Or exactly: `No new UI because <reason>` naming the surface the outcome
already reaches.

## Out of scope
Bullets, not checkboxes. Where each item is tracked.
```

Activated in chat (`activate <id>`) → replace the banner with
`> **ACTIVE BUILD**` before implementation.

Parked → `> **PARKED** — revive when <condition>`.

## tasks.md

```markdown
# Tasks

- [ ] Work this change owes
```

A checkbox is work **this** change owes. Findings and handoffs are bullets.
A box that can never close is a lie.

## specs/<capability>/spec.md

```markdown
## ADDED Requirements

### Requirement: <name>
The system SHALL …

#### Scenario: <name>
- GIVEN …
- WHEN …
- THEN …
```

`MODIFIED` pastes the **entire** living requirement, then edits. Fold
replaces that block wholesale. `REMOVED` names the requirement only.

`design.md` only when cross-cutting, new deps, security, or genuine
ambiguity.
