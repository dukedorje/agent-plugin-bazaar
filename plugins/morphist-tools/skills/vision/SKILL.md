---
name: vision
description: Strategic product vision — create, evolve, and align project and product-level vision documents. The strategic layer above sprint planning.
user-invocable: true
argument-hint: "[create|update|align|archive|merge|split] [--product=<name>] [path]"
---

# Vision — Strategic Product Layer

Manages the vision and product dimension artifacts in `docs/`. This is the strategic counterpart to `/sprint-plan` (tactical) and `/prd` (requirements).

**Artifact locations:**
- Umbrella vision: `docs/vision.md`
- Product dimensions: `docs/products/{name}/` (vision.md, prd.md, architecture.md)
- Standalone PRDs: `docs/prd-{slug}.md`

---

## 1. Argument Parsing

Parse `$ARGUMENTS` for:

1. **Subcommand** (optional): First positional word. One of: `create`, `update`, `align`, `archive`, `merge`, `split`. If omitted → **landscape** mode.

2. **Flags**:

| Flag | Effect |
|------|--------|
| `--product=<name>` | Target a product dimension (kebab-case) |
| `--into=<name>` | Target for merge/split operations |

3. **Positional path** (optional): Path to an existing vision or PRD file to operate on.

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

Scan the `docs/` directory to build a product map.

### 3a. Discovery

Check for:
- `docs/vision.md` — umbrella vision
- `docs/products/*/` — product dimensions (check each for: vision.md, prd.md, architecture.md)
- `docs/prd-*.md` — standalone PRDs not in a product dimension
- `docs/sprints/*/requirements.md` — scan frontmatter for `product` field to map sprints → products
- `docs/decisions/` — cross-cutting ADRs

### 3b. Render Landscape

Display a structured overview:

```
Project: {repo name}
Vision: {docs/vision.md status — exists/missing, last modified}

Products:
  {name}/
    Vision: {exists/missing, date}
    PRD: {exists/missing, title, version}
    Architecture: {exists/missing}
    Sprints: {list of sprint slugs referencing this product}

  {name}/
    ...

Standalone PRDs:
  {path} — {title} (not in a product dimension)

Decisions: {count} cross-cutting ADRs in docs/decisions/
```

After the landscape, display available actions:

```
Actions:
  /vision create                    — Create umbrella vision
  /vision create --product=<name>   — Create a new product dimension
  /vision update [product]          — Evolve a vision
  /vision align                     — Check alignment across all levels
```

---

## 4. Create Mode

### 4a. Determine Target

- With `--product=<name>`: target is `docs/products/{name}/vision.md`. Create `docs/products/{name}/` if it doesn't exist.
- Without `--product`: target is `docs/vision.md`.
- If the target file already exists, suggest `update` instead and halt.

### 4b. Context Gathering

Before the interview, silently gather context:

1. If creating a product vision, read `docs/vision.md` (umbrella) if it exists — the product vision should serve the umbrella vision.
2. Read any existing PRDs in `docs/` or `docs/products/{name}/` — they may contain problem/user context.
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
{contents of docs/vision.md}
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
```

### 4e. Save and Report

Write the generated vision to the target path. Report:

```
Vision saved to {path}

Next steps:
  /prd {path}                   — Create a PRD seeded from this vision
  /vision align                 — Check alignment (after PRD exists)
```

---

## 5. Update Mode

### 5a. Resolve Target

- If `--product=<name>`: target is `docs/products/{name}/vision.md`
- If positional path: use that
- Otherwise: target is `docs/vision.md`
- If target doesn't exist, suggest `create` instead and halt.

### 5b. Read Current Vision

Read the current vision document in full.

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
```

### 5e. Drift Check

After updating, check the changelog length. If there are 3+ entries, or any entry is marked as a major revision:

```
This vision has evolved significantly. Consider:
  /vision archive {--product=<name>}  — Archive current version and start fresh
```

---

## 6. Align Mode

### 6a. Build Artifact Manifest

Scan `docs/` to build a manifest of paths (do NOT read file contents yet — pass paths to the analyst):

- `docs/vision.md` (umbrella)
- All `docs/products/*/vision.md` (product visions)
- All `docs/products/*/prd.md` and `docs/prd-*.md` (PRDs)
- All `docs/sprints/*/requirements.md` (sprint requirements)

### 6b. Dispatch Alignment Analysis

Dispatch `analyst` (opus) with the **file paths**, not contents. The analyst reads files itself:

```
You are checking strategic alignment across a project's vision and product artifacts.

Read the following files (skip any that don't exist):

Umbrella Vision: docs/vision.md

Product Dimensions:
{for each product dimension found}
- docs/products/{name}/vision.md
- docs/products/{name}/prd.md
{end for}

Standalone PRDs:
{for each standalone PRD path}
- {path}
{end for}

Sprint Requirements (read frontmatter only — look for `product` field):
{for each sprint}
- docs/sprints/{slug}/requirements.md
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
- Are any PRDs significantly newer than their vision (vision may be stale)?

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
```

### 6c. Present Results

Display the alignment report. Suggest specific actions:

```
Recommended actions:
  /vision update --product=auth     — Auth vision is stale (PRD is 3 months newer)
  /vision create --product=billing  — Standalone PRD docs/prd-billing.md has no product dimension
  /vision update                    — Umbrella vision doesn't mention the mobile product
```

---

## 7. Archive Mode

### 7a. Resolve Target

Same resolution as Update mode (section 5a).

### 7b. Archive

1. Determine version number: count existing archived versions (`vision-v1.md`, `vision-v2.md`, etc.) and increment.
2. Move current file: `vision.md` → `vision-v{N}.md` (or `prd.md` → `prd-v{N}.md`).
3. Report: "Archived to {path}. Run `/vision create` to write a fresh vision with the archived version as context."

The next `create` will detect the archived version and use it as seed context — inheriting lessons without carrying the changelog burden.

---

## 8. Merge Mode

Usage: `/vision merge <from> --into=<to>`

### 8a. Validate

Verify both `docs/products/<from>/` and `docs/products/<to>/` exist.

### 8b. Read Both Dimensions

Read all artifacts from both product dimensions.

### 8c. Merge Interview

Ask the user:
1. "Why are these merging? What changed?"
2. "Which vision better represents the merged product?"
3. "Are there PRD requirements from {from} that don't apply to the merged product?"

### 8d. Execute Merge

1. Dispatch `writer` (sonnet) to produce a merged vision from both visions + interview.
2. Write merged vision to `docs/products/{to}/vision.md`.
3. If both have PRDs, flag: "Both dimensions have PRDs. You'll need to reconcile these manually or run `/prd --product={to}` to generate a merged PRD."
4. Archive `docs/products/{from}/` to `docs/products/{from}-v{N}/` where N is the next unused version number (don't delete — archive).
5. Update any sprint requirements that reference the old product name (via `product` frontmatter field in `docs/sprints/*/requirements.md` — no-op if sprints don't have this field yet).

---

## 9. Split Mode

Usage: `/vision split <product> --into=<a>,<b>`

### 9a. Validate

Verify `docs/products/<product>/` exists. Verify neither `<a>` nor `<b>` exist as product dimensions.

### 9b. Split Interview

Ask the user:
1. "What's driving the split?"
2. "How do you draw the line between {a} and {b}?"
3. "Which users go where?"

### 9c. Execute Split

1. Create `docs/products/{a}/` and `docs/products/{b}/`.
2. Dispatch `writer` (sonnet) to draft two vision documents from the original vision + interview.
3. Write both visions.
4. Archive the original: `docs/products/{product}/` → `docs/products/{product}-v{N}/` where N is the next unused version number.
5. Report: "Split complete. Review both visions and run `/prd --product={a}` and `/prd --product={b}` when ready."

---

## Interaction Style

Vision work is **collaborative and reflective**, not procedural. Guidelines:

- Ask questions one at a time. Let the user think.
- Don't rush to generate — understanding the problem is more important than producing a document.
- Use the user's language, not framework jargon. No "value propositions" or "synergies."
- The vision should sound like the user talking to a colleague, not a committee writing a memo.
- When updating, preserve the original voice. Don't homogenize.
- The anti-vision section ("how we lose the plot") is one of the most valuable — push for specificity here.
