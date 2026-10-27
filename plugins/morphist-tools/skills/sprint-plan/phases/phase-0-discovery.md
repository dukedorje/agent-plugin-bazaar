# Phase 0: Intake & Discovery

Run only after explicit factory selection and initialization in `SKILL.md`.
Inputs: user brief, codebase, living specs, relevant existing changes, and
`SPEC_DIR/proposal.md`. Do not read OMC session files as project memory.

## Process

1. Classify input as raw idea, structured brief, or existing PRD. Identify
   missing context without inventing requirements.
2. Inventory relevant source files, manifests, frameworks, module boundaries,
   integration points, and existing implementation patterns. Note a new
   repository when no meaningful source/build structure exists.
3. Locate applicable specifications, architecture decisions, research, and
   UX artifacts in normal project sources. Record source paths so later
   phases can re-anchor. Existing documents are inputs, not new plan stores.
4. Detect whether the change has UI and whether usable UX guidance exists.
   Carry forward relevant learnings from existing project records without
   introducing a sprint sequence or regenerating global decision logs.
5. Summarize the problem, evidence, codebase constraints, assumptions, and
   open questions under `SPEC_DIR/proposal.md` **Why**. Link useful sources.
   At lean detail, a few sentences may suffice; full detail adds the inventory
   and input analysis as subsections of Why.

## Completion

Check Phase 0 in `SPEC_DIR/tasks.md` when discovery evidence is recorded.
Record UI detection and any missing input as short notes there. Do not mark
complete if the goal is still unknown. Next: Phase 1.
