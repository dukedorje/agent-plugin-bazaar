---
name: brief
description: >
  Write a short, high-signal brief for one unit of work — goal, testable
  acceptance criteria, external API contracts you had to look up, inherited
  gotchas, and explicit out-of-scope. Replaces heavyweight story templates.
  Use when starting a discrete piece of work, or when asked to write a brief
  or spec this out.
user-invocable: true
argument-hint: "[<issue-id> | \"<description of the work>\"] [--out=<path>]"
---

# brief: one unit of work, on one page

A brief is what a capable agent actually needs to do a piece of work correctly, and
nothing else. It is roughly 40 lines. If yours is 200, you are writing a story template.

## Why this is short

Long story templates were rational when models were weaker: restating the goal three
times in three formats kept an agent from wandering. That is no longer the failure mode.
The remaining failures are different, and only three things address them:

| Failure mode | What fixes it |
|---|---|
| Model invents a plausible-but-wrong API signature | The **contract** section — real signatures, pasted from real docs |
| Model re-learns something the team already learned painfully | The **inherited** section — carried from `LEARNINGS.md` |
| Model does adjacent work nobody asked for | The **out of scope** section |

Everything else in a classic story is derivable from the codebase or tracked
in the work graph. Do not write it.

## Inputs

- **A bead ID** (`brief ik-4f2`) — read it with `bd show`, use its title/description/acceptance.
- **Or a plain description** — write the brief, then offer to create the bead.

## Procedure

1. **Read the bead** (if given one) and the code it touches. Do not skip this; the
   contract and gotchas sections are worthless if written from imagination.
2. **Look up every external API** the work calls into. Paste real signatures. If you
   cannot verify a signature, say so explicitly in the brief rather than guessing.
3. **Read `docs/LEARNINGS.md`** (or `.omc/notepad.md`) and carry forward anything that
   touches these files or this subsystem.
4. **Write the brief** to `--out`, or `.omc/briefs/<id>.md` by default.
5. **State what you are NOT doing.** This is the section that most reliably prevents
   scope creep, and the one most often omitted.

## Template

```markdown
# <id>: <one-line goal>

**Goal.** One or two sentences. What is true after this that isn't true now.

## Acceptance
- [ ] Assertions, each independently checkable. Not tasks — outcomes.
- [ ] If you cannot say how you'd test it, it is not an acceptance criterion.

## Contract
Real signatures for anything external, verified against the actual docs or source.

```<lang>
// pasted, not remembered
```

## Inherited
Gotchas from prior work on this subsystem, carried from LEARNINGS.md.
- <fact> — <why it bit us> (<file:line>)

## Out of scope
- <the adjacent thing you are deliberately not doing, and where it is tracked instead>
```

## What to do afterwards

- Anything learned the hard way while executing → append to `docs/LEARNINGS.md`.
- Status lives in the work graph, not in the brief. Do not add a `Status:` line.
- Briefs are disposable. The durable artifacts are the code, the graph,
  `ARCHITECTURE.md`, and `LEARNINGS.md`.
