## MODIFIED Requirements

### Requirement: One skill tree

The system SHALL keep canonical skill files at
`plugins/intention/skills/<verb>/SKILL.md` for
`intend`, `change`, `advise`, `act`, `fold`, `brief`, `debrief`,
`map`, `ready`, and `run`. Each `SKILL.md` SHALL have YAML
frontmatter whose `name` matches the directory.

`.agents/skills/<verb>` SHALL resolve to that same directory (symlink
in this repo) so Grok, Hermes, and Prime load the files without a
plugin install.

#### Scenario: Grok sees the verbs in-repo

- GIVEN a clone of this repo
- WHEN Grok starts in the repo root
- THEN it discovers `intend`, `change`, `advise`, `act`, `fold`,
  `brief`, `debrief`, `map`, `ready`, and `run` from
  `.agents/skills/`

#### Scenario: Claude installs the same files

- GIVEN marketplace entry `intention` → `./plugins/intention`
- WHEN Claude loads the plugin
- THEN it reads `plugins/intention/skills/*/SKILL.md`, which are the
  symlink targets
