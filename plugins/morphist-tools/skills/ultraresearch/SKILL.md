---
name: ultraresearch
description: >
  Multi-agent research swarm with tree-structured hypothesis exploration and synthesized output.
  Use when a question requires broad exploration, multiple perspectives, or deep investigation.
  Triggers on: ultraresearch, research swarm, deep research, explore hypotheses.
user-invocable: true
argument-hint: "<question> [--depth 1|2|3] [--mode research|engineering|quick] [--max-branches N] [--output-dir PATH]"
model: opus
---

# Ultra-Research: Tree-Structured Research Swarm

A multi-agent research orchestrator. Decomposes a question into ranked hypotheses,
fans out parallel specialist agents to explore each branch, allows controlled sub-branching,
then synthesizes findings into a referenced document with inline source citations.

## Parameters

Parse these from the user's input. Apply defaults for anything not specified.

| Parameter        | Default                                    | Description                                    |
| ---------------- | ------------------------------------------ | ---------------------------------------------- |
| `QUESTION`       | *(required)*                               | The research question or goal                  |
| `DEPTH`          | `2`                                        | Max tree depth (1 = flat, 2 = one sub-level, 3 = deep) |
| `MODE`           | `research`                                 | `research` (synthesis doc), `engineering` (action plan), `quick` (single-pass summary) |
| `OUTPUT_DIR`     | *(context-dependent, see below)*           | Root directory for all output artifacts        |
| `MAX_BRANCHES`   | `5`                                        | Max parallel hypothesis branches per level     |
| `MAX_AGENTS`     | `8`                                        | Hard cap on total concurrent agents            |

### Output Directory Resolution

The default `OUTPUT_DIR` depends on how ultra-research was invoked:

| Invocation | Default OUTPUT_DIR |
| ---------- | ------------------ |
| **User** (`/ultraresearch` with a question) | `docs/research/<slug>/` |
| **Change in context** (a current `openspec/changes/<change-id>/`, or the request names one) | `openspec/changes/<change-id>/research/<slug>/` |
| **Explicit** (`--output-dir` or `OUTPUT_DIR` in the request) | That path. It wins. |

`<slug>` is a short kebab-case name of the question, not the whole sentence.
Do not write `.omc/`, `docs/sprints/`, or a `research_artifacts/` directory.

A prompt that contains `## Ultra-Research Request` is an agent caller.
Use the caller's `OUTPUT_DIR` when it set one. Otherwise use the change
path when a change is in context, and `docs/research/<slug>/` when it is not.

### Quick Mode

When `MODE = quick`, collapse the workflow to a single pass:
1. Use `decomposer` to generate 3 hypotheses max
2. Explore each with a single agent (no sub-branching, DEPTH forced to 1)
3. Produce a condensed synthesis (skip verification stage)

This is appropriate for questions that need breadth but not depth.

## Progress Tracking

Use `notepad_write_working` at each stage transition to persist progress:

```
## Ultra-Research: {{QUESTION}}
Stage: [1-Decomposition | 2-Exploration | 3-Synthesis | 4-Verification]
Hypotheses: N total, N explored, N pending
Output: {{OUTPUT_DIR}}
```

This ensures state survives context compaction. On resume, read notepad first
and skip completed stages.

## Workflow

### Stage 1 — Decomposition

Spawn `morphist-tools:decomposer` (opus) with this prompt. Fill the
braces from the request. Omit the Caller Context section when there is
none.

```
Research question: {QUESTION}
MAX_BRANCHES: {MAX_BRANCHES}

## Caller Context
{CONTEXT}

Decompose this question into ranked hypotheses following your protocol.
Write the output as a single markdown document. The caller saves it.

Your final message is the only thing the caller sees. Put the complete
markdown document in that message.
```

Save the agent's output to `{{OUTPUT_DIR}}/decomposition.md`.

**Failure handling**: If the decomposer fails or returns empty, retry once with a
simplified prompt. If it fails again, report the error and stop gracefully.

### Stage 2 — Exploration (parallel, depth-bounded)

For each selected hypothesis from decomposition.md, spawn one
`morphist-tools:investigator` (sonnet) in parallel. Queue any past
`MAX_AGENTS` and launch them as slots free. Prompt:

```
## Hypothesis Assignment
**Title**: {hypothesis.title}
**Investigation Type**: {hypothesis.investigation_type}
**Plausibility**: {hypothesis.plausibility}
**Info Value**: {hypothesis.information_value}
**Context**: {hypothesis.rationale}

DEPTH_REMAINING: {DEPTH minus the current level}

When DEPTH_REMAINING is greater than 0, you may identify up to 3
sub-hypotheses. Write each as its own document and list them in your
Sub-Hypotheses section. When DEPTH_REMAINING is 0, do not generate
sub-hypotheses.

Investigate this hypothesis following your protocol. The investigation
type tells you whether to focus on web search, codebase exploration,
analysis, or a hybrid.

Write your output as a single markdown document. The caller saves it.

Your final message is the only thing the caller sees. Put the complete
markdown document in that message.
```

Save each agent's output to `{{OUTPUT_DIR}}/hypotheses/{{hypothesis-slug}}/findings.md`.

If sub-hypotheses are generated and DEPTH allows, spawn additional investigator agents
for each sub-hypothesis. Save sub-findings to
`{{OUTPUT_DIR}}/hypotheses/{{parent-slug}}/sub/{{child-slug}}/findings.md`.

**Time-box**: If an investigator has not produced findings after exploring 4+ sources,
it must write what it has and move on — do not block the swarm.

### Stage 3 — Synthesis & Verification

Spawn `morphist-tools:synthesizer` (opus). The caller passes paths, not
a paste of every findings file, unless a finding is short enough that
the path alone would hide it. Prompt:

```
## Synthesis Task
**Original Question**: {QUESTION}
**Mode**: {MODE}
**Output Directory**: {OUTPUT_DIR}

## Decomposition
Read {OUTPUT_DIR}/decomposition.md

## Findings
Read each file under {OUTPUT_DIR}/hypotheses/.

Follow your synthesis protocol:
1. Cross-reference all findings by theme.
2. Draft the narrative synthesis with inline citations.
3. Run verification checks (citation audit, coverage, claim validation).
4. For each hypothesis, emit the structured metadata block in
   "Per-Hypothesis Spike Metadata". `confidence: high` requires
   reproducible evidence. `version-pinned` is mandatory for any
   library-API claim. `spike-required` is true unless confidence is
   high and verification is empirically-tested.
5. Write both files under the output directory:
   - synthesis.md (narrative, spike metadata, verification)
   - summary.json (machine-readable summary with the hypotheses array)

Your final message is the only thing the caller sees. Report the exact
file paths you wrote and a short status. Include blockers when there
are any.
```

The synthesizer handles both synthesis AND verification in a single pass.
If verification status is FAIL, report issues to the user rather than silently
patching — the human should decide how to proceed.

## Output Structure

```
{{OUTPUT_DIR}}/
├── decomposition.md          # Stage 1: ranked hypotheses
├── synthesis.md              # Stage 3+4: final output with verification
└── hypotheses/
    ├── hypothesis-one/
    │   ├── findings.md       # Stage 2: agent findings
    │   └── sub/
    │       └── sub-hyp/
    │           └── findings.md
    ├── hypothesis-two/
    │   └── findings.md
    └── ...
```

## Agent-Callable Interface

Ultra-research can be invoked by other skills/workflows via agent dispatch. When called
programmatically (not by a human typing `/ultra-research`), the caller provides structured
parameters and receives structured output.

### Dispatch Contract

Other skills invoke ultra-research by spawning an agent with these parameters in the prompt:

```
## Ultra-Research Request
- QUESTION: Where should an architecture decision live when the story is already a bead?
- MODE: engineering
- DEPTH: 2
- OUTPUT_DIR: openspec/changes/retarget-intake/research/decision-home
- MAX_BRANCHES: 4
- CONTEXT: |
    Stories are beads (bd). Narrative for this intake is
    openspec/changes/retarget-intake/ (proposal.md, design.md, tasks.md).
    Do not write docs/sprints/ or .omc/.
```

Substitute the question, mode, depth, branch cap, and context. Set
`OUTPUT_DIR` to `openspec/changes/<change-id>/research/<slug>/` when the
caller is an intake change, or to `docs/research/<slug>/` when it is not.
`CONTEXT` seeds decomposition with constraints the caller already has.

When the caller cannot run this skill itself, spawn a general-purpose
agent (opus) with that request, then these lines:

```
Follow the ultra-research workflow. Spawn morphist-tools:decomposer,
morphist-tools:investigator, and morphist-tools:synthesizer as that
workflow describes. Write every artifact under OUTPUT_DIR.

Your final message is the only thing the caller sees. Report the exact
file paths you wrote and a short status.
```

The caller then reads `{OUTPUT_DIR}/summary.json` and cites it from the
change's `design.md`. It does not copy the synthesis into a bead.

### Output Contract

After completion, ultra-research guarantees these files exist at `{{OUTPUT_DIR}}`:

1. **`synthesis.md`** — the full narrative output (always present). MUST embed a structured metadata block for each hypothesis, near the top of the document, with the schema below.
2. **`summary.json`** — a machine-readable summary for agent callers:

```json
{
  "question": "...",
  "mode": "research|engineering|quick",
  "status": "complete|partial|failed",
  "confidence": "low|medium|high",
  "executive_summary": "3-5 sentence answer",
  "key_findings": [
    {
      "finding": "one-sentence finding",
      "confidence": "low|medium|high",
      "verification": "empirically-tested|inferred-from-source|docs-only",
      "version_pinned": "library@version or null",
      "spike_required": true,
      "sources": ["hypotheses/foo/findings.md", "https://..."]
    }
  ],
  "hypotheses": [
    {
      "id": "H1",
      "claim": "one-sentence claim",
      "confidence": "low|medium|high",
      "verification": "empirically-tested|inferred-from-source|docs-only",
      "version_pinned": "library@version or null",
      "spike_required": true,
      "spike_prompt": "concrete test the caller should run to validate",
      "spike_artifact": null
    }
  ],
  "open_questions": ["..."],
  "contradictions": ["..."],
  "hypotheses_explored": 5,
  "hypotheses_total": 5,
  "verification_status": "PASS|PASS_WITH_WARNINGS|FAIL|SKIPPED",
  "output_dir": "..."
}
```

### Per-Hypothesis Spike Metadata (required in synthesis.md)

Each hypothesis the synthesis references MUST carry a structured YAML frontmatter-style block, either at the top of the document under `## Hypothesis Metadata` or inline inside the hypothesis's section. The schema:

```yaml
- id: H3                             # stable identifier used by decisions.md citations
  claim: "one-sentence claim"        # what the hypothesis asserts
  confidence: medium                 # low | medium | high
  verification: inferred-from-source # empirically-tested | inferred-from-source | docs-only
  # empirically-tested: the research agent ran code / reproduced it and recorded evidence
  # inferred-from-source: read the library source or an authoritative doc, did not run
  # docs-only: relied on external tutorials / blog posts / forum threads

  version-pinned: playcanvas@2.17.2  # REQUIRED whenever the claim cites library behavior
                                     # (null only if the claim is version-independent)
  spike-required: true               # auto-derived:
                                     # true  iff confidence != high OR verification != empirically-tested
                                     # false iff confidence == high AND verification == empirically-tested

  spike-prompt: |                    # agent's best guess at a minimal test
    "Build the smallest repro: load any SOG with unified:true,
    setWorkBufferModifier with a sin-wave shader on modifySplatCenter,
    assert canvas hash changes between two frames 900ms apart."

  spike-artifact: null               # path to docs/spikes/{id}/finding.md
                                     # populated by the /spike skill after validation;
                                     # null until then
```

**Calibration rules** — the synthesizer must apply these honestly:
- `confidence: high` requires BOTH `verification: empirically-tested` AND a cited evidence artifact (log snippet, screenshot, test command and result). If the agent can't produce the evidence, downgrade to `medium`.
- `version-pinned` is mandatory whenever a claim cites library API behavior. "PlayCanvas 2.13–2.16" ≠ "PlayCanvas 2.17" — do not omit the version and do not paper over a range mismatch.
- `spike-required` is automatically `true` unless both `confidence == high` AND `verification == empirically-tested`. The synthesizer must not lower this flag without evidence.
- `spike` treats a hypothesis that omits this block as `confidence: low` and does not land it. See `plugins/intention/references/from-sprint-exec.md`.

### Why this exists (from sprint-004 retro)

In sprint-004, an ultraresearch synthesis output read like a verified prescription. In fact two of its recommendations were unvalidated hypotheses — the recipe for Blocker B didn't work when applied. The fix landed only after the team built three spike pages to empirically test the mechanism. The spike-metadata contract above makes the calibration visible so downstream consumers can make the right gate decisions.

3. **`decomposition.md`** — the hypothesis tree (always present)
4. **`hypotheses/*/findings.md`** — individual findings (always present)

### Synthesis Stage: summary.json Generation

At the end of Stage 3 (Synthesis), the synthesizer agent MUST also write `summary.json`
alongside `synthesis.md`. Extract the structured fields from the narrative synthesis.
This is mandatory — agent callers depend on it to decide whether to consume the full
synthesis or just the summary.

---

## Error Handling

- **Agent spawn failure**: Log the error, skip that hypothesis, note it as "unexplored" in synthesis
- **Empty findings**: If an agent returns no useful findings, record "inconclusive" rather than omitting
- **Timeout**: If Stage 2 takes too long, proceed to synthesis with whatever findings are available
- **All agents fail**: Report to user with error details; do not produce a hollow synthesis. Write `summary.json` with `"status": "failed"`
