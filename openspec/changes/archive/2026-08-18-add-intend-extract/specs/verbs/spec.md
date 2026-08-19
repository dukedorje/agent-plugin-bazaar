## ADDED Requirements

### Requirement: intend extract-from named items

When `intend` is given `--extract-from` with one or more items, it
SHALL observe those items before orient and split. Usual items SHALL
be bead ids and epic ids. Observe SHALL report records of action
(descriptions, acceptance, comments, close reasons, signed results,
blocking edges that resolve) and insight into the intent those
records imply. It SHALL NOT dump full transcripts into the DAG. It
SHALL NOT implement. A missing or unreadable item SHALL be named as
unresolved and SHALL NOT be invented. Absence of the flag SHALL keep
today’s observe (living specs, in-flight changes, learnings).

#### Scenario: Extract from an epic

- GIVEN epic `bazaar-db8` has children, comments, and a close on
  `bazaar-db8.1`
- WHEN `intend --extract-from bazaar-db8` runs
- THEN the output includes action records from that epic and insight
  into intent
- AND then Orient and a DAG
- AND no product paths were edited for architecture nodes that still
  need activation

#### Scenario: No flag stays blank-page

- GIVEN no `--extract-from`
- WHEN `intend` runs
- THEN observe is living specs, in-flight changes, and learnings
- AND the run is not rejected for lacking extract-from

#### Scenario: Missing item is named

- GIVEN `--extract-from` names an id that does not resolve
- WHEN `intend` observes
- THEN that id is reported unresolved
- AND no invented trail is presented as fact
