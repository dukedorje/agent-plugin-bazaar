# harness

How the five verbs reach Grok, Claude, Codex, Hermes, and Prime.
Folded from `add-harness-touch-ins` on 2026-08-15 (H1).

The matrix is [`plugins/intention/references/harness.md`](../../../plugins/intention/references/harness.md).
This spec does not copy the table.

## Purpose

One skill tree. Five hosts. Installer is optional (`skills` CLI). This
repo does not run `skills add` against itself.

## ADDED Requirements

### Requirement: Matrix is the reduce

The project SHALL keep a harness matrix at
`plugins/intention/references/harness.md` covering Grok, Claude, Codex,
Hermes, and Prime with: loads in-clone, how, invoke, packet-only worker,
and gaps.

#### Scenario: Someone asks how Codex invokes a verb

- GIVEN the matrix
- WHEN they read the Codex row
- THEN they see skill-name / `$` invoke, `.agents/skills/`, and “never
  a slash command”

### Requirement: skills CLI is optional fan-out

Other repos MAY install with `skills add <plugin-dir> --skill … --agent
claude-code --agent codex`. This repo SHALL NOT run that command in-tree
in a way that creates `.claude/skills/` copies of the verbs.

#### Scenario: List without install

- GIVEN `skills` 1.4.8+
- WHEN `skills add ./plugins/intention --list`
- THEN it names act, brief, change, fold, intend

### Requirement: Missing CLI agents are gaps, not blockers

Absence of `--agent grok` or `--agent hermes-agent` in the `skills` CLI
SHALL NOT block in-repo use. Grok loads `.agents/skills/`. Hermes uses
that or `~/.hermes/skills/`.

#### Scenario: Grok in this clone

- GIVEN `.agents/skills/intend` exists
- WHEN Grok starts here
- THEN `intend` loads without `skills add`
