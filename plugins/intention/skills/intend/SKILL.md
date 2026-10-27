---
name: intend
description: >
  Capture an intention, observe the system, orient (load class × blast ×
  lifecycle), and split a DAG of named change-ids. Open groups when work is
  complementary or contested. Use when starting from a goal, "let's build
  this", or when asked to intend / plan work without a sprint factory.
  Also when asked to work out a plan, run it by me, show me first, or
  plan then advise/ask before acting. Default next is steer (decision
  briefing, then menus). --extract-from names beads/epics to read first.
  Optional gates: --plan --advise --ask --go --autonomous.
user-invocable: true
argument-hint: "[--extract-from <items>] [--plan] [--advise] [--ask] [--go] [--autonomous] <intention>"
---

# intend

Conductor of the loop. You observe, orient, split, and assign. You do not
implement. You do not write a sprint folder.

Load `../../references/shared.md` and `../../references/intend-dag.md`.
Read the citation table in `shared.md` from disk. Do not paste those files.

## Procedure

1. **Observe.** If `--extract-from <items>` is set (usual: bead / epic
   ids, repeatable), read those records first: descriptions, acceptance,
   comments, close reasons, signed results, blocking edges that resolve.
   Report **records of action** and **insight into the intent** they
   imply. Do not dump transcripts. A missing or unreadable item is named
   **unresolved** — do not invent its trail. Then, with or without the
   flag: code that the intention touches. `openspec/specs/` (built).
   `openspec/changes/*/proposal.md` excluding `archive/` and `PARKED`.
   `docs/LEARNINGS.md`. Who is available (human, which harnesses).
   No flag keeps this blank-page observe; the run is not rejected for
   lacking extract-from. Dossier ids wait on `add-intend-extract-dossier`.
2. **Orient.** Load class × blast × lifecycle → rigor for the *highest*
   node. If you cannot name the capability, stay here.
3. **Skip?** Restore / typo / pin / comment / test-for-existing → print
   `direct fix` and stop. No DAG, no change.
4. **Split.** Keep blocked descendants provisional: goal, dependencies,
   assumptions, and intended acceptance; defer detailed contracts until their
   dependencies deliver evidence. Do not activate the entire DAG as a
   prerequisite for a campaign. One acceptance surface per node. Landing is `add-<id>`,
   `brief`, or `direct fix`. Edges are real dependencies (B cannot start
   until A committed a usable artifact). Set `density` from
   `docs/contracts/dispatch.md` (capability order is the inverse of
   depth). Blast raises density, never lowers it. Assign with
   `python3 plugins/intention/scripts/ladder.py assign --shape …`
   (known → Sonnet then Terra; implementation/thinking → Sol then Opus;
   plan → Opus then Astra; design → Opus + designer skills). Real architecture
   opens a review-pair. Gating advise uses `vary-reader`
   (`references/reviewers.md`): Astra when the blast is schema, deletion,
   protocol, or durability; otherwise rotate eligible readers and skip
   the author's vendor. Versions live only in ladder.json.
5. **Group.** Complementary jobs → `weave`. Contested expensive → `fork`
   only under the gates in `shared.md`. `ambiguous` / `sensitive` /
   architecture write → `human-gate`. Members are agents (or groups).
6. **Write** the DAG in the shape in `intend-dag.md`. Chat is enough;
   beads (`bd create --type node`) if they want a tracker. No
   `.beads/`, or `node` rejected as a type → run `setup` first. Title is
   the kebab, not `nod-…`. No `.omc/`. No SHALLs in the DAG.
7. **Spike.** Load `../../references/from-sprint-exec.md`. If this goal
   depends on an unverified hypothesis, record
   `- Spike: <id> <claim> — unverified (<confidence>, <verification>)`
   on that node's description (chat DAG and the bead, when one exists).
   Name it in the decision briefing. Do not run `spike`. `steer` menus
   the three choices.
8. **Stop.** Report ready-set, needs activation, and a **Decision
   briefing** (same section `map` prints). Pin this DAG
   (`map --current <root-id>`). Then apply **After the DAG**. Never
   `fold` from here.

Do not start write work on architecture or instrument nodes until
they are activated (human, or a recorded grant on a prepared
dependency-ready node).

## After the DAG

Default: **steer** (briefing, then menus). `--ask` / “run it by me”
is the same pause with no act. Skip the pause only when they said
`--go`, “don't pause”, or `--autonomous`.

| Gate / phrase | Means |
|---|---|
| (none) | Steer. Briefing + menus. Do not `act`. |
| `--plan` | This skill — the DAG. Default on. Skip only when a current DAG already is the plan and they said not to re-plan. |
| `--advise` | After steer (or skip), `change` then `advise` on architecture / instrument. Do not `act`. |
| `--ask` | Present DAG + briefing. Stop. Wait. Next conversation is `steer`. Do not `act`. |
| `--go` / “don't pause” | Skip steer menus; auto-log remaining forks lean. Not a grant. |
| “activate this set” / “activate what we just intended” | Record **campaign authority** on the root bead (or chat DAG). Then `change` → `advise` until contracts are ready. **Pause** (map + briefing). | 
| “activate this set and run” / “run this whole intention” / a grant followed by “and run” | Same grant, and it implies `--go` for that intention. After contracts are ready, enter `/run` (waves when two+ disjoint writes are ready). Do not pause for another utterance. Explicit `--ask`, `--plan`, `--advise`, `--wait`, `--tidy`, and `--pause-before` still win. |
| `--autonomous` / “I'll review after” | `--go` plus, if a grant is recorded, `/run` (roll). Do not halt for steer. Do not flip PENDING without the grant. Do not check EYES. Review afterwards is `map` / `demo` / `status`. |

Do not treat “run it by me” as `/run` or `/run --wait`. Those act.
You do not need `/run-wave` after this; `/run` takes waves.
