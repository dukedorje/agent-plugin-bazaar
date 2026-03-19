---
name: sprint-plan-help
description: Show usage information for the sprint-plan plugin. Triggers on "how do I use sprint-plan", "sprint-plan help", or "what does sprint-plan do".
user-invocable: true
argument-hint: ""
---

Display the following usage guide directly to the user. Do NOT run any agents or tools — just output this text as-is:

---

## `/sprint-plan` — Multi-Phase Sprint Planning

Transforms a product idea into implementation-ready user stories through 6 automated phases.

### Usage

```
/sprint-plan "your product idea here"
/sprint-plan path/to/prd.md
/sprint-plan --fast "quick prototype"
/sprint-plan --restart-from=architecture
```

### Phases

| # | Phase | What happens |
|---|-------|-------------|
| 0 | Discovery | Scans codebase, detects greenfield/brownfield, finds existing artifacts |
| 1 | Requirements | Expands idea into FRs, NFRs, constraints (parallel agents) |
| 2A | Architecture | Architecture decisions with RALPLAN-DR consensus |
| 2B | Epic Design | Groups requirements into user-value-focused epics |
| 3 | Stories | Breaks epics into dev-agent-sized stories with BDD criteria |
| 4 | Enrichment | Adds technical details, testing requirements, file lists |
| 5 | Validation | Checks FR coverage, dependencies, story quality |

### Modes

- **Thorough** (default) — RALPLAN-DR consensus, asks you about important decisions
- **Fast** (`--fast`) — Single-pass, all decisions auto-made, ~3x faster

### Flags

| Flag | Effect |
|------|--------|
| `--fast` | Single-pass mode, no consensus loops |
| `--thorough` | Explicit thorough mode (default) |
| `--restart-from=<phase>` | Resume from: `discovery`, `requirements`, `architecture`, `epic-design`, `story-decomposition`, `story-enrichment`, `validation` |

### Output

All artifacts land in `.omc/sprint-plan/sprint-NNN/`:
- `discovery.md` — project context
- `requirements.md` — functional and non-functional requirements
- `architecture-decisions.md` — ADR-lite architecture decisions
- `epics.md` — epic structure with stories
- `stories/*.md` — enriched story files ready for dev agents
- `readiness-report.md` — final validation summary

### Refining

Use `/ral <phase>` to refine any phase output with a Planner→Architect→Critic consensus pass:
```
/ral architecture
/ral requirements
/ral epics
```

### After Planning

Feed stories into implementation: `/team ralph`

### More Info

See the full README: `plugins/sprint-plan/README.md`
