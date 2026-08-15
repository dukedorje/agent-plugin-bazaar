# Conventions — the three-artifact system

*Portable to any repo. Adopting it is: create two files, run `bd init`.*

---

## The claim

A project needs exactly three durable process artifacts. Anything else is scaffolding
that outlived its model generation.

| Artifact | Question it answers | Lives in |
|---|---|---|
| **`ARCHITECTURE.md`** | Why is it shaped this way? | The repo, versioned, ADRs inline |
| **beads** (`bd`) | What is the state of the work? | `.beads/`, queryable |
| **`docs/LEARNINGS.md`** | What did we learn the hard way? | The repo, append-only |

Plus one disposable artifact — the **brief** (`/brief`) — one page per unit of work,
deleted or ignored after the work lands.

---

## Why this replaces heavier methodologies

The evidence that motivated this (measured on a real repo, `identikey-core`, 2026-07):

- ~10,000 lines of process artifacts against ~11,800 lines of source, half of which
  was tests. **Process documentation at ~1.7× production code.**
- Per-story XML context files were generated for the first two epics, then silently
  abandoned — they duplicated the story markdown.
- One retrospective existed across nine epics; the rest were marked optional.
- Tech specs existed for 3 of 13 epics.
- The one retro that was written produced four action items; the documentation one
  was never done.

The methodology had already voted with its feet. The format stayed constant while the
*value* migrated: late stories were dense with genuinely useful specifics (real API
signatures, encoding gotchas, learnings carried from prior stories), while early stories
were full of template filler. Keep what the late stories were doing. Drop the template.

**None of this means the heavy process was wrong when it was written.** Restating a story
three ways kept weak models on task. It is scaffolding for a building that now stands.

---

## 1. `ARCHITECTURE.md`

One file. Living. ADRs inline with an explicit status, and **amend rather than delete**
when reality diverges:

```markdown
### ADR-007: Passkeys stored in Keycloak credentials ✅ → Amended
Superseded 2026-02 — Keycloak Admin API has no programmatic WebAuthn credential
creation. Passkeys live in Postgres (`passkey_credentials`). Original rationale kept
below for provenance.
```

The amendment trail is the point. An ADR marked "amended" with a reason is how you
detect drift between the plan and the code — and it is the one thing in a heavyweight
process that reliably earns its keep.

## 2. beads

State lives in the tracker, never in markdown. If you are hand-maintaining a YAML file
with a status enum and a comment block explaining the enum, that is a database with
extra steps.

```bash
bd ready                  # what can I start right now
bd list --priority 0      # what matters
bd show <id>              # the spec
bd dep tree <id>          # what's blocking
```

Use `decision` type for ADRs so the decision and the work that depends on it live in one
graph. Wire the dependency to the *task* the decision blocks, not the epic — beads
disallows a non-epic blocking an epic.

## 3. `docs/LEARNINGS.md`

**Append-only. One line per hard-won fact. Dated, with a file reference.**

```markdown
- 2026-07-14 — stored passkey publicKey is standard base64, not base64url; convert with
  `Buffer.from(s, 'base64')` before passing to the verifier. (src/lib/passkey/verify-registration.ts)
- 2026-07-20 — challenge deletion is wrapped in try/catch on purpose: the credential is
  already verified, so a delete failure must not fail the request.
```

This is the highest-value convention here, and the one most likely to be skipped because
it feels like overhead in the moment. It is the *only* artifact that captures knowledge a
model genuinely cannot derive from the codebase. Everything else in a story template can
be re-derived; this cannot.

**Write to it at the end of any work that involved a surprise.** `/review-fix` should
append to it as a matter of course.

## 4. The brief

See `skills/brief/SKILL.md`. Roughly 40 lines: goal · acceptance · contract · inherited ·
out of scope. Disposable.

---

## Adopting this in a new repo

```bash
bd init                                  # state
touch docs/LEARNINGS.md                  # knowledge
# write ARCHITECTURE.md when the first real decision gets made — not before
```

Do not create an `ARCHITECTURE.md` full of headings on day one. It earns its existence
at the first decision someone would otherwise re-litigate.

---

## What was dropped, and why

Removed from morphist-tools 2026-07-28 (recoverable from git history):

| Dropped | Why |
|---|---|
| `status`, `update-status`, `log`, `exec-report`, `sprint-review`, `sprint-validate`, `backlog`, `scope` | A tracker with real state makes status-reporting skills redundant. `bd list`/`ready`/`show`/`dep tree` do this natively. |
| `refine`, `replan`, `audit`, `reconcile`, `post-mortem` | Drift-repair tooling. With beads as the source of truth and smaller units of work, drift is cheaper to just fix than to orchestrate a repair pass over. |
| `doc`, `blocker-triage`, `help` | Absorbed into the surviving skills, or obsolete once the skill count is small enough to read. |

Kept: `sprint-exec`, `sprint-to-beads`, `sprint-from-beads`, `prd`,
`vision`, `ultraresearch`, `retro`, `review-fix`, `verify`, `done-validate`, `spike`,
`release`, and `brief`.

`sprint-plan` is **parked** (D1, 2026-08-15). Default planning is `intend`.
Revive when someone explicitly wants the 10-phase / `--thorough` factory.

The kept set preserves the thing that actually earned its keep: **a long planning session
you can start, walk away from, and come back to** — plus the quality gates that stop an
agent reporting fake completion.
