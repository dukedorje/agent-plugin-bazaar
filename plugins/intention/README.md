# intention

Five verbs from intention to a running system. Canonical skill files live
here. In this repo, `.agents/skills/<name>` is a symlink at each skill so
Grok, Hermes, and Prime load the same files without a plugin install.

Claude: `claude --plugin-dir ./plugins/intention` or install from this
marketplace as `intention`.

Grok: clone is enough (`.agents/skills/`). Or
`grok plugin marketplace add <this-repo>` and `grok plugin install intention --trust`.

Codex / Hermes / Prime: Agent Skills standard. Invoke by name, never as a
Claude slash command. Matrix: [`references/harness.md`](references/harness.md).

Other repos (Vercel `skills` CLI):

```bash
skills add ./plugins/intention \
  --skill intend --skill change --skill act --skill fold --skill brief \
  --agent claude-code --agent codex -y
```

Contracts: `docs/contracts/agent-surface.md`. Living specs: `openspec/specs/`.
Verb bodies: `references/` (shared vocabulary; skills do not fork the surface).
