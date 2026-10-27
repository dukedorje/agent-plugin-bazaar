---
name: vision
description: Strategic product vision — create, evolve, and align project and product-level vision documents. The strategic layer above sprint planning.
user-invocable: true
argument-hint: "[create|update|align|archive|merge|split] [--product=<name>] [--change=<change-id>] [path]"
---

# Vision — Strategic Product Layer

Manages strategic vision and product dimensions within one `openspec/changes/<change-id>/` per workshop. This is the strategic counterpart to `/sprint-plan` (tactical) and `/prd` (requirements).

**Artifact locations:**
- Vision: `openspec/changes/<change-id>/proposal.md`, in `## Why` and `## What`.
- PRD: the same proposal, with requirements in `specs/<capability>/spec.md` deltas when present.
- Architecture: `openspec/changes/<change-id>/design.md` only when the vision changes the architecture.
- Never create or write `docs/vision.md`, `docs/products/`, or `docs/prd-*.md`.

**Change selection and write rules (all modes):**
- `--change=<change-id>` selects an existing change. A positional path inside a change selects that id; resolve conflicting selectors before writing. Otherwise derive a verb-led kebab-case id from the workshop topic, such as `add-billing`. Resolve collisions before writing rather than overwriting another change.
- `--product=<name>` is product metadata and a section label within the selected proposal, not another directory. Multiple dimensions remain sections of the same proposal.
- New proposals are `PENDING`. Preserve existing disposition banners, PRD content, and unrelated sections. Do not activate, fold, move a change into the archive, or edit living specs.
- Every writing mode saves vision material into the proposal's Why and What: problem, users, insight, and motivation in Why; solution, differentiators, success, scope boundaries, anti-vision, and product relationships in What. Retain workshop headings as subsections and keep the changelog in the proposal.
- Create or update design.md only for architectural changes, recording decisions and rationale. Otherwise keep the vision in proposal.md.

---

## 1. Argument Parsing

Parse `$ARGUMENTS` for:

1. **Subcommand** (optional): First positional word. One of: `create`, `update`, `align`, `archive`, `merge`, `split`. If omitted → **landscape** mode.

2. **Flags**:

| Flag | Effect |
|------|--------|
| `--product=<name>` | Target a product dimension (kebab-case) |
| `--into=<name>` | Target product section(s) for merge/split operations within the selected change |
| `--change=<change-id>` | Select the OpenSpec change to read or update |

3. **Positional path** (optional): An existing proposal path selects its containing change; another vision or PRD file is read-only seed context. Outputs always use the selected change directory.

---

## 2. Mode Dispatch

| Subcommand | Mode | Description |
|------------|------|-------------|
| *(none)* | Landscape | Show what exists across all product dimensions |
| `create` | Create | Interactive workshop to write a new vision |
| `update` | Update | Evolve an existing vision with changelog |
| `align` | Align | Check alignment across all levels |
| `archive` | Archive | Version rollover — archive current, start fresh |
| `merge` | Merge | Combine two product dimensions |
| `split` | Split | Divide one product dimension into two |

---

## 3. Landscape Mode (default)

Scan `openspec/changes/` (excluding `archive/`) to build a product map from change proposals.

### 3a. Discovery

Check for:
- `openspec/changes/*/proposal.md` — vision in Why and What, product metadata, and PRD sections
- `openspec/changes/*/specs/*/spec.md` — requirement deltas
- `openspec/changes/*/design.md` — architectural decisions, when present
- `openspec/changes/*/sprint.md` — sprint plans associated with each change

### 3b. Render Landscape

Display a structured overview:

```
Project: {repo name}
Vision: {selected change id, proposal disposition, last modified}

Products:
  {name} (change: {change-id})
    Vision: {exists/missing, date}
    PRD: {exists/missing, title, version}
    Architecture: {exists/missing}
    Sprint: {sprint.md exists/missing in this change}

  {name} (change: {change-id})
    ...

Other change proposals:
  {change-id} — {title}

Decisions: {count} changes with design.md
```

After the landscape, display available actions:

```
Actions:
  /vision create                    — Seed a change with a project vision
  /vision create --product=<name>   — Seed a change with a product vision
  /vision update --change=<change-id> — Evolve a vision in that change
  /vision align                     — Check alignment across all levels
```

---

## 4. Create Mode

### 4a. Determine Target

- Resolve the change id using the shared selection rules. The target is `openspec/changes/<change-id>/proposal.md`.
- With `--product=<name>`, label the product dimension within that proposal. Without it, write the project-level vision there.
- If the target already contains the requested vision, suggest `update --change=<change-id>` instead and halt. An existing PRD alone can receive vision sections without being replaced. A preserved revision alone is seed context, not a current vision.

### 4b. Context Gathering

Before the interview, silently gather context:

1. If creating a product vision, read any project-level vision in the selected proposal; other explicitly identified change proposals may supply read-only umbrella context.
2. Read the PRD and requirement deltas in the selected change, plus any supplied seed file — they may contain problem/user context.
3. Dispatch an `explore` agent (haiku) to scan the codebase for a 1-paragraph project summary (tech stack, structure, what it does).

### 4c. Vision Interview

Conduct an adaptive interview. Ask questions **one at a time**. After each answer, assess coverage before moving to the next question.

**Core questions (ask in this order, skip if already covered by context):**

| # | Question | What it elicits |
|---|----------|-----------------|
| 1 | "What problem are you solving?" | Problem space — the pain, not the solution |
| 2 | "Who feels this most acutely?" | Primary users and their context |
| 3 | "How do they cope today, and what's broken about that?" | Current state and gap analysis |
| 4 | "What's your key insight — the non-obvious thing that shapes your approach?" | Core insight — what makes this different |
| 5 | "What does success look like for the people you're helping?" | Success vision — concrete, not abstract |
| 6 | "What is this explicitly NOT?" | Scope boundaries and anti-goals |
| 7 | "What would make you say 'we've lost the plot'?" | Anti-vision — guardrails for drift |

**Adaptive rules:**
- If context (existing PRDs, codebase scan) already covers a dimension, skip or ask a targeted follow-up instead
- If an answer covers multiple questions at once, update coverage accordingly
- **Target: 4-7 questions total.** Stop when you have enough signal to write a compelling vision.
- For product visions: include a question about how this dimension relates to the broader project vision

### 4d. Vision Generation

Dispatch `writer` (sonnet):

```
You are writing a product vision document from an interview transcript.

{if product vision}
Umbrella Vision:
---
{project-level vision from the selected proposal or explicitly identified context proposal}
---

This product dimension ({name}) should serve and align with the umbrella vision above.
{end if}

Interview Transcript:
---
{full interview transcript}
---

Codebase Context:
---
{explore agent findings}
---

Write a vision document following this structure:

# {Project or Product Name}

## Executive Summary
[2-3 sentences: what this is, why it matters, what future it enables]

## Problem Statement
[The pain. Who feels it. What happens if it goes unsolved.]

## Core Insight
[The non-obvious realization that shapes the approach. This is the "aha" that makes the solution different from the obvious alternative.]

## Proposed Solution
[How we address the problem, at a high level. Not implementation details — the shape of the solution.]

## Key Differentiators
[Why this approach, not the alternatives. What's hard to copy.]

## Target Users
[Primary personas: who they are, what they need, what success looks like for them.]

## What This Is NOT
[Explicit scope boundaries. Anti-goals. Things we will actively resist adding.]

## Anti-Vision: How We Lose the Plot
[Guardrails. Signals that we've drifted from the vision. "If we find ourselves doing X, we've gone wrong."]

{if product vision}
## Relationship to Project Vision
[How this product dimension serves the umbrella vision. Where it fits in the larger picture.]
{end if}

## Changelog
[Empty on creation. Updated by /vision update.]

---

Write in the voice of someone who deeply understands the problem. Be specific and concrete — not corporate-speak. The vision should feel like a conversation with a smart person who cares, not a committee document.

IMPORTANT — final message contract: Your final message IS your return value. The orchestrator sees ONLY your final message, never your earlier turns or tool calls. Put the complete output specified above directly in your final message. Do not end with a sign-off like "Done" or "see above".
```

### 4e. Save and Report

Merge the generated vision into Why and What in the selected proposal using the shared write rules. Save design.md only if architecture changes. Report:

```
Vision saved to openspec/changes/<change-id>/proposal.md

Next step:
  /sprint-plan <change-id>       — Begin sprint planning for this change
```

If requirements need further refinement first, `/prd --change=<change-id>` continues in this same change.

---

## 5. Update Mode

### 5a. Resolve Target

- Resolve the selected change; target `openspec/changes/<change-id>/proposal.md` and its Why/What vision sections.
- If `--product=<name>`, select that product's subsections within the proposal.
- If the requested vision doesn't exist, suggest `create` with the same change id instead and halt.

### 5b. Read Current Vision

Read the current proposal in full, including its vision, PRD, and disposition, plus design.md if present.

### 5c. Update Interview

Ask focused questions about what's changed:

1. "What has shifted since this was written?"
2. "Has the problem changed, or has your understanding of it changed?"
3. "Are there new users, or have priorities shifted?"
4. "Has anything moved from 'not this' to 'maybe this' (or vice versa)?"

**Target: 2-4 questions.** This is a focused update, not a full re-interview.

### 5d. Update Generation

Dispatch `writer` (sonnet) with the current vision + interview transcript. Instructions:

```
You are updating an existing vision document based on new information from the user.

Current Vision:
---
{current vision document}
---

Update Interview:
---
{transcript}
---

Instructions:
1. Update the vision sections that have changed. Preserve sections that haven't.
2. Append a changelog entry at the bottom:

## Changelog

### {today's date}
- {1-2 line summary of what changed and why}

3. If the changes are fundamental (core insight shifted, problem redefined, users changed significantly), add a note at the top:

> **Major revision ({date})**: {1-sentence summary of what pivoted}

Keep the same voice and style as the original. Don't rewrite sections that haven't changed.

IMPORTANT — final message contract: Your final message IS your return value. The orchestrator sees ONLY your final message, never your earlier turns or tool calls. Put the complete output specified above directly in your final message. Do not end with a sign-off like "Done" or "see above".
```

Merge the updated vision into the same proposal using the shared write rules. Synchronize design.md only if architecture changes. Report `/sprint-plan <change-id>` as the next step.

### 5e. Drift Check

After updating, check the changelog length. If there are 3+ entries, or any entry is marked as a major revision:

```
This vision has evolved significantly. Consider:
  /vision archive --change=<change-id> {--product=<name>} — Preserve current revision and start fresh
```

---

## 6. Align Mode

### 6a. Build Artifact Manifest

Scan `openspec/changes/` (excluding `archive/`) to build a manifest of proposal, requirement delta, design, and sprint paths (do NOT read file contents yet — pass paths to the analyst). Identify project and product visions by their sections in each proposal; keep the report read-only.

### 6b. Dispatch Alignment Analysis

Dispatch `analyst` (opus) with the **file paths**, not contents. The analyst reads files itself:

```
You are checking strategic alignment across a project's vision and product artifacts.

Read the following files (skip any that don't exist):

Project and Product Visions / PRDs:
{for each discovered change}
- openspec/changes/{change-id}/proposal.md (vision in Why/What, PRD and product metadata)
- openspec/changes/{change-id}/specs/{capability}/spec.md (each requirement delta, if present)
- openspec/changes/{change-id}/design.md (if present)
{end for}

Sprint Plans:
{for each discovered change with a sprint plan}
- openspec/changes/{change-id}/sprint.md
{end for}

Read each file, then run these alignment checks:

**1. Vertical Alignment**
- Does each product vision serve the umbrella vision?
- Does each PRD implement its product vision's problem statement and users?
- Do sprint requirements trace to PRD functional requirements?
- Flag misalignments with specific quotes from both documents.

**2. Horizontal Alignment**
- Do product dimensions contradict each other?
- Are there capability gaps between dimensions (something no product owns)?
- Are there overlapping claims (two products claiming the same user or problem)?

**3. Drift Detection**
- Do any vision changelogs suggest fundamental drift from original intent?
- Does proposal content or its changelog show PRD updates that the vision has not incorporated?

**4. Orphan Detection**
- Standalone PRDs without product dimensions
- Product dimensions without visions
- Sprints without product references
- PRDs that don't connect to any vision

**5. Coherence**
- Is the umbrella vision still a good summary of all product dimensions?
- Are there product dimensions that have outgrown the umbrella vision?

Format:

## Alignment Report

### Vertical Alignment
{findings with quotes}

### Horizontal Alignment
{findings}

### Drift Detection
{findings}

### Orphans
{findings}

### Coherence
{assessment}

## Recommendations
{actionable next steps, ordered by priority}

IMPORTANT — final message contract: Your final message IS your return value. The orchestrator sees ONLY your final message, never your earlier turns or tool calls. Put the complete output specified above directly in your final message. Do not end with a sign-off like "Done" or "see above".
```

### 6c. Present Results

Display the alignment report. Suggest specific actions:

```
Recommended actions:
  /vision update --change=<change-id> --product=auth — Refresh stale Auth vision
  /vision create --change=<change-id> --product=billing — Add vision to a billing PRD
  /vision update --change=<change-id> — Include the mobile product in the project vision
```

---

## 7. Archive Mode

### 7a. Resolve Target

Same resolution as Update mode (section 5a).

### 7b. Archive

1. Determine the next unused vision revision number within the selected proposal.
2. Preserve the current vision as a dated `Vision revision {N}` subsection in that proposal; retain its PRD, requirements, and disposition. This is a vision version rollover, not an OpenSpec fold or change archive.
3. Report: "Vision revision preserved in openspec/changes/<change-id>/proposal.md. Run `/vision create --change=<change-id>` to write a fresh vision using that revision as context."

The next `create` uses the preserved revision as seed context — inheriting lessons without carrying the changelog burden. After saving a replacement vision, the next planning step is `/sprint-plan <change-id>`.

---

## 8. Merge Mode

Usage: `/vision merge <from> --into=<to> --change=<change-id>`

### 8a. Validate

Verify both source product sections exist in the selected proposal, or are explicitly identified read-only context in other proposals. The output remains in the single selected change.

### 8b. Read Both Dimensions

Read both product visions, their PRD sections, and associated requirement deltas.

### 8c. Merge Interview

Ask the user:
1. "Why are these merging? What changed?"
2. "Which vision better represents the merged product?"
3. "Are there PRD requirements from {from} that don't apply to the merged product?"

### 8d. Execute Merge

1. Dispatch `writer` (sonnet) to produce a merged vision from both visions + interview.
2. Merge the vision into Why and What under the target product label in the selected proposal, following the shared write rules. Update design.md only for architectural changes.
3. If both have PRDs, flag: "Both dimensions have PRDs. Reconcile them in this proposal or run `/prd --change=<change-id> --product={to}`."
4. Preserve prior source vision sections as dated revisions in the selected proposal; leave any external source changes intact.
5. Record product mapping changes in the proposal for sprint planning to consume. Report `/sprint-plan <change-id>` as the next step.

---

## 9. Split Mode

Usage: `/vision split <product> --into=<a>,<b> --change=<change-id>`

### 9a. Validate

Verify the source product section exists in the selected proposal. Verify neither `<a>` nor `<b>` already exists as a product section there.

### 9b. Split Interview

Ask the user:
1. "What's driving the split?"
2. "How do you draw the line between {a} and {b}?"
3. "Which users go where?"

### 9c. Execute Split

1. Add product labels `{a}` and `{b}` within the selected proposal.
2. Dispatch `writer` (sonnet) to draft two vision sections from the original vision + interview.
3. Merge both visions into Why and What in that same proposal; update design.md only for architectural changes.
4. Preserve the original vision as a dated revision in the proposal. Do not create additional change directories for the split.
5. Report: "Split complete in openspec/changes/<change-id>/proposal.md. Review both product sections, then run `/sprint-plan <change-id>`. Refine requirements with `/prd --change=<change-id> --product=<name>` if needed."

---

## Interaction Style

Vision work is **collaborative and reflective**, not procedural. Guidelines:

- Ask questions one at a time. Let the user think.
- Don't rush to generate — understanding the problem is more important than producing a document.
- Use the user's language, not framework jargon. No "value propositions" or "synergies."
- The vision should sound like the user talking to a colleague, not a committee writing a memo.
- When updating, preserve the original voice. Don't homogenize.
- The anti-vision section ("how we lose the plot") is one of the most valuable — push for specificity here.
