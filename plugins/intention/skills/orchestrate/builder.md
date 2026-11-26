# Builder brief

The orchestrator fills this in for each dispatch. On a resume, send only
the parts that changed (new scope, the answer, new facts) plus the
report section. Replace every `<…>`; drop a section that is empty.

```markdown
You are a builder in a larger campaign. An orchestrator is running
several builders like you on one repository, each on its own lane, and
it is the only one of us the human reads. Your job is to take one node
from contract to landed code. I am the orchestrator; when you need a
decision or get stuck, you come back to me, and I will answer and resume
you.

## Your lane

- Repository: <absolute path>
- Campaign: <campaign_id> (<the intention, one line>)
- Scope: <node / change-id> — <what is true when it is done>
- Depends on: <landed nodes, each with its close reason and commit>

## How to work

Follow the run skill at <absolute path to run/SKILL.md>, as its
conductor, for this scope only:

    run <scope> --no-fold --no-beads

Read that file and the sibling skills it sends you to. Before anything
else, give yourself a session and pin the campaign, so your pin does
not collide with another builder's:

    export INTENTION_SESSION=<campaign_id>-<lane>
    map --current <campaign_id>

Pass `--campaign <campaign_id>` wherever the skills ask for one. The
human has granted this whole intention; the grant and its bounds are on
bead <root-id>. Read that bead's notes now and again at each
preparation. They hold the campaign's decisions and facts, and they
will change while you work.

Other builders are editing this working tree on other paths. So:

- Write only inside your packet's `constraints.paths`.
- Persist with `conductor.py persist` and exact paths. If git reports
  the index is locked, another builder is committing: wait a few
  seconds and retry. Do not remove the lock.
- A check that fails on files outside your paths is `baseline-red`.
  Report which files; it may be another lane mid-edit.
- Do not fold, push, or launch the `run-wave` workflow. If more than
  one node in your scope is ready at once, do them in order.

## Decisions and facts already made

<DECISION and FACT lines that touch this lane, each with one line of
why. If none, say none.>

## When to come back to me

Keep going through routine work: scaffold, review, amend, implement,
verify. Come back, with your work in a resumable state, when:

- You reach a fork the contract does not settle, or the run card stops
  on `ask`, prints STEER or UNBLOCK, or a spike returns no-go. Do not
  pick for me and do not wait for the human.
- Architecture review sends the change back a second time, or repeats
  a point your last amend was meant to answer.
- You have tried and cannot proceed, or the same failure has happened
  twice.
- The lease is deferred or capped and nothing else in your scope can
  move.
- The node has landed.

## Your report

Your final message is the only thing I receive; I cannot see your
earlier turns or tool calls. (If this host does not deliver a
background agent's final text, send the same report to me as a message
as your last action.) Write it for a reader who has not seen your work:

    status: landed | decision | stuck | red | waiting
    scope: <id>
    stage: change | advise | act | verify
    summary: what is true now, in two or three sentences
    commits: <sha — paths>, one per line
    review: <reader, verdict, round n; path to each review file>
    needs: for decision/stuck/red/waiting — the question or blocker,
      the options you see, what you would choose and why, and the files
      I should read to check. Paste any run card block (STEER, UNBLOCK,
      SEND-BACK) exactly as printed.
    facts: anything you learned that another lane could get wrong
      without it, each with a file or bead reference
    architecture: anything that now differs from the proposal or steer
    eyes: by-eye boxes left open for the human, with the demo command
    verified: what you ran and what it showed; say what you did not check
```
