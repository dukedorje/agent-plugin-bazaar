## ADDED Requirements

### Requirement: Matrix is the reduce

The project SHALL keep `plugins/intention/references/harness.md` covering
the five hosts.

#### Scenario: Someone asks how Codex invokes a verb

- GIVEN the matrix
- WHEN they read the Codex row
- THEN invoke is skill-name, never a slash command

### Requirement: skills CLI is optional fan-out

Other repos MAY `skills add` the plugin dir. This repo SHALL NOT create
`.claude/skills/` copies that way.

#### Scenario: List without install

- GIVEN `skills` 1.4.8+
- WHEN `skills add ./plugins/intention --list`
- THEN it names the five verbs

### Requirement: Missing CLI agents are gaps, not blockers

Missing `--agent grok` SHALL NOT block in-repo Grok (`.agents/skills/`).

#### Scenario: Grok in this clone

- GIVEN the symlinks
- WHEN Grok starts here
- THEN `intend` loads without `skills add`
