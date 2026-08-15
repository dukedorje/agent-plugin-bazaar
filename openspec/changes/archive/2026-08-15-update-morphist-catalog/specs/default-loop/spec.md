## ADDED Requirements

### Requirement: Catalogs list only skills that exist

CLAUDE.md and marketplace versions SHALL match disk. Dropped names SHALL
NOT appear as invocable.

#### Scenario: Stranger reads CLAUDE.md

- GIVEN the Skills Reference
- WHEN they look for `backlog` or `status`
- THEN those names are absent

#### Scenario: validate.sh versions

- GIVEN `./validate.sh`
- WHEN it checks morphist-tools
- THEN marketplace version equals plugin.json
