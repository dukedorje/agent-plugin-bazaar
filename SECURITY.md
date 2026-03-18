# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in a marketplace plugin, please report it privately by opening a GitHub security advisory on this repository. Do not open a public issue.

## Plugin Security Standards

All plugins in this marketplace are reviewed against these criteria:

### Must Not

- Contain hardcoded secrets, tokens, or credentials
- Exfiltrate user data via hooks or MCP servers
- Make unauthorized network requests
- Contain prompt injection in skill definitions
- Execute arbitrary code without user awareness
- Modify files outside their declared scope

### Must

- Use `${CLAUDE_PLUGIN_ROOT}` for path references (not hardcoded paths)
- Use `${CLAUDE_PLUGIN_DATA}` for persistent state
- Declare all external dependencies
- Document any network access in the README

## Review Process

- All PRs are reviewed for security before merging
- External plugin sources are pinned by SHA
- Automated validation runs on every PR via CI

## Known Risks

Community plugins execute in the user's environment with the permissions granted by Claude Code. Users should:

- Review plugin source code before installing
- Use project-scoped installation for untrusted plugins
- Monitor hook behavior via Claude Code's hook logging
