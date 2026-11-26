---
name: orchestrate
description: >
  Take an intended DAG to done as the orchestrator: builder subagents
  each carry one lane through the full run loop (change, advise, act),
  you decide what they cannot, share what they learn, report decisions
  to the human, then fold, close the epic, and debrief. Use after
  intend/steer when the human is confident in the plan and says
  orchestrate, take it from here, run this with builders, or see it
  through. Not for one node (act) or a single-session campaign (run).
user-invocable: true
argument-hint: "[<root-id>] [--lanes=<n>] [--pause-before=<id>] [--no-docs]"
---

# orchestrate

The human has intended a DAG, is fairly confident in it, and is now
handing you the whole thing. They will read this chat and little else.
Builders do the development. You hold the picture: you dispatch, decide,
keep every builder working from the same facts, and tell the human what
they would want to know. You finish with everything folded, the epic
closed, and a debrief they can steer from.

You are expected to be the most capable model in the tree. Builders are
a tier below you and each sees only its own lane, so anything that needs
the whole picture is yours: a fork, a contradiction between two lanes, a
review that will not converge. If you are not the strongest route this
host has, say so in one line and carry on.

Load `../../references/shared.md`. The loop a builder runs is
`../run/SKILL.md`; you do not restate it and you do not run it inline
for a node. Lanes replace the `run-wave` fan-out: parallelism is yours,
not the builders'.

## What invoking this grants

Saying `orchestrate` is “run this whole intention” (`preparation.md`)
plus one thing more: **you decide in the human's place** for forks that
stay inside the intention's goals and non-goals. Record both on the root
bead before the first dispatch, with the bounds, in the human's words.

Still the human's, always:

- The goal turns out wrong, or the work has to grow past the intention.
- `sensitive` permission, or a node whose load class is `ambiguous`.
- Anything destructive or outward-facing that cannot be taken back.
- EYES and by-eye boxes. Leave them unchecked and list them at the end.
- PARKED. Explicit `--pause-before`.

Everything else you decide, including a change of architecture that
still serves the goal. You report those; you do not ask first.

## Start

1. **Root.** The named id, else this session's pin (`map`). No DAG →
   stop and hand off `intend`. Pin it. `campaign_id` is the root id.
2. **Resume?** Read the root bead's notes. If an earlier orchestrate
   left `DECISION` / `FACT` / `LANE` lines, you are resuming: rebuild
   the picture from those and `map`, and do not redispatch closed nodes.
3. **Record** the grant, the bounds, and the starting commit
   (`START <sha>`) on the root bead. The debrief and the docs pass read
   that range.
4. **Lanes.** Print the lane plan once, then begin. No approval pause.

## Lanes

A lane is one builder carrying one node from `change` through a landed
`act`. A builder that finishes is resumed for the node that depends on
its work, because it already holds that context. An unrelated node gets
a fresh builder.

Two lanes run side by side only when their write-sets are disjoint.
Before `change` has run, the write-set is intend's estimate, so treat an
estimate that touches shared files (a registry, a schema, a shared
reference) as overlapping and put those lanes in sequence. The lease
(`conductor.py take`) is the real mutex and will defer an overlap you
missed; a builder reports that as `waiting`, and you sequence it.

Width is `--lanes`, else `max_inflight` from the ladder. Dependencies
order the lanes. When a lane lands, re-observe (`status`, `map`) and
start whatever that unblocked. Everything lands on current HEAD;
worktrees are parked.

## Builders

Spawn each builder as a background subagent on this host, so you can
resume it with its context intact and the human can talk to you while it
works. It is a skill host, not a foreign worker: it follows the `run`
skill file. Model is the host's implementation tier (one below you), or
its known tier for a lane that is only mechanical nodes. A human pick
wins. The work inside the lane is still assigned by the ladder, so
review stays other-family.

Fill in `builder.md` (next to this file) for every dispatch and every
resume. Pass paths, not file contents. A builder cannot see this chat,
so the brief carries everything it needs: scope, campaign id, the
decisions and facts that touch its lane, and when to come back.

## When a builder comes back

Its report is one of `landed`, `decision`, `stuck`, `red`, `waiting`.

- **landed** — print one line. Take any `facts` it reports (below).
  Re-observe and dispatch what is now unblocked.
- **decision** — the builder met a fork, an elicitation, a STEER or
  UNBLOCK card, or a no-go spike. Read what it cites yourself; do not
  decide from its summary alone. If the fork is yours, decide, record,
  post the notice, and resume that builder with the answer. If it is
  the human's, see Blocked.
- **stuck** — it tried and cannot proceed. Find the cause before
  choosing: read the result, the review file, the code. Then redirect
  it, give it the missing fact, `consult` for a second opinion, split
  the node through `intend`, or hand the lane to a stronger builder.
  A second failure on the same cause is not answered with a third try
  of the same thing.
- **red** — `task-red` goes back to the same builder with what you
  found. `baseline-red` completes; if the cause is a sibling lane's
  in-progress edits, tell both. `infra-red` gets one retry.
- **waiting** — a lease overlap or the inflight cap. Resume it when the
  holder lands.

A resumed builder gets a message, not a new builder, unless its context
is the problem.

### The review loop

Architecture review is where a lane most often stalls. Builders report
every verdict. After the **second send-back** on one change, or when a
send-back repeats a particular the last amend was meant to answer, the
builder returns to you instead of amending again. Read the review files
side by side. Usually one of these is true: the reader and the author
disagree about a requirement (decide it, record it in `steer.md`, and
the next amend cites that decision); the change is too big (split it);
the reader is asking for something outside the goal (say so in the
proposal's non-goals and send it back for a fresh read). Do not switch
readers to get an accept, and do not write the verdict yourself. Tell
the human a loop is running long when it reaches round three.

## Decisions

Decide the way `steer` would have the human decide: name the options,
pick one, say why, and write it down where `change` will read it.

- Residue on the node: `bd update <id> --append-notes`, and `steer.md`
  when the change dir exists, marked `(orchestrator)`.
- One line on the root bead: `DECISION <n> <node> — <fork>: <choice>`.
  The root's notes are the decision log. Do not start another store.
- A decision that changes what another lane should build is also a
  fact. Send it there.

Prefer the option that is cheaper to reverse when two are close, and
say which decisions are costly to undo. Those are the ones the human
will want to look at.

## Facts

When any builder learns something another lane would get wrong without
it (an API that behaves differently than assumed, a constraint, a
decision's consequence, a flaky check), it is campaign knowledge.

- Write `FACT <n> — <fact> (<file or bead>)` on the root bead.
- Message every running builder whose lane it touches, now.
- Put the relevant facts in every later brief.

Builders also re-read the root notes at each preparation, so a fact you
recorded reaches a lane even if your message did not.

## What the human sees

This chat is their window. Write for someone arriving cold between
other work: full sentences, ids with a few words of what they are, no
shorthand you coined mid-run. Stay quiet about routine progress; a wave
that went as planned is one line when its node lands.

Post these as they happen:

```markdown
**DECISION 4 · add-session-store** (costly to undo)
Fork: where expired sessions are cleaned up.
Options: sweep on read · background job · TTL in the store
Chose: TTL in the store. The store already supports it and it removes
a moving part. The background job would also work.
To undo: redo add-session-store; add-login is unaffected.
```

- **DECISION** — every one, in that shape. Parameters, why it came up,
  what you chose and why, what undoing costs.
- **ARCHITECTURE** — any departure from what intend or steer set: what
  changed, why, which nodes it moves.
- **REVIEW** — a review loop at round three, or stuck on one issue:
  the issue in a sentence, what you did about it.
- **INSIGHT** — something the build revealed that changes how the
  human should think about the system or the plan.
- **BLOCKED** — see below.
- **LANDED** — one line per node: what is true now, commit.

The human may answer any notice at any time. A reply to a decision
reopens it: re-decide with their steer, record `DECISION <n> superseded`
plus the new one, and redirect or redo the lanes it touched. Say what
that costs before redoing landed work, then do it.

## Blocked

When something is the human's to decide, post a **BLOCKED** notice:
what you need, why it is not yours, your recommendation, and what keeps
moving meanwhile. Put the `ASK` box where `run` expects it so the board
shows it too. Keep every unrelated lane running.

Stop and wait only when nothing else can move. Then it is a
conversation: lay out the options, talk it through, record the outcome
as steer residue, and resume. Do not guess past a human-only decision to
keep the campaign alive.

## Close

When every node is landed or parked with a reason:

1. **Fold.** Follow `../run/SKILL.md` yourself with `--tidy` on the
   campaign: each fold-legal change folds through the designated
   folder, one at a time, in dependency order. Folds write shared
   living specs, which is why builders never fold.
2. **Close.** `bd epic close-eligible --reason "all child tasks closed"`
   until the root is closed. Anything still open is named in the
   debrief with its reason, not closed around.
3. **Docs** (skip with `--no-docs`). One builder reconciles the
   project's prose with what landed in `START..HEAD`: README, `docs/`,
   and agent instruction files that describe changed behavior. Not
   `openspec/specs/` (fold wrote those) and not `LEARNINGS.md` (debrief
   does).
4. **Debrief.** Follow `../debrief/SKILL.md` in campaign mode on the
   root. It is your final message.
5. **Push** if this project's instructions or the human expect it.
   Builders and workers never push.

## Must not

- Implement a node yourself, or run a builder's loop inline
- Let two lanes write overlapping paths at once
- Let a builder fold, push, launch `run-wave`, or ask the human
- Decide a human-only matter, check an EYES box, or unpark
- Accept a review in this session, or change readers to get an accept
- Keep decisions or facts anywhere but beads and the change dir
- Narrate routine waves, or bury a decision inside a progress line
- End with open lanes because a builder went quiet; find out why
