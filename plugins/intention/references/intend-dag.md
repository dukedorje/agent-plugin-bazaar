# intend output

Write this when the user wants a file. Otherwise print the same shape in
chat. Durable copy is beads. Do not write `.omc/`. SHALLs do not live here.

```markdown
# <one-line intention>

**Non-goals.** …

## Extract
Only when `--extract-from` was given. Omit this section if there was
no flag (blank-page observe still happened).

- From: <bead / epic ids that resolved>
- Unresolved: <ids that did not, or omit if none>
- Records of action: descriptions, comments, closes, results, edges
  (short; not transcripts)
- Insight into intent: what those records imply about why

## Orient
- Load class: structure-clear | intention-critical | ambiguous
- Blast: …
- Lifecycle: vibe | brief | change | architecture | instrument (highest node)
- Why: one sentence

## DAG

### <node-id>
- Goal: what is true after
- Landing: `add-<id>` | brief | direct fix
- Capability: <kebab> | (omit at vibe/brief)
- Rigor: …
- Depends on: <node-ids or none>
- Assumptions: provisional facts to revisit when dependencies land
- Group: solo | weave | fork | human-gate | conductor-workers | …
- Members / roles: conductor · worker · consultant · reader · human · group
- Density: lean | standard | explicit   ← from ladder.py; inverse of capability
- Surface: skill-host | packet-only
- Assignee: `ladder.py assign --shape <known|thinking|design|plan|architecture-review|fold>`
- Consult: plan/replan → Fable 5.1; write stays here
- Architecture: review-pair, reader = Fable 5.1 (Grok for second family; Sol via `codex exec` or OPENAI_API_KEY)
- Activation: none | needs human | already activated
- Acceptance: command `…` | journey | contrast | none

## Campaign authority
User instruction and agreed scope / non-goals / architectural commitments,
or none. “Activate this set” / “run this whole intention” fills this.
This grants permission, not preparation of downstream designs.

## Ready-set
Nodes with all inbound edges satisfied.

## Needs activation
Architecture / instrument / sensitive writes still PENDING.

## Decision briefing
Upcoming forks, why they matter, downstream, last steer skipped.
Enough to prime a context switch. Same section `map` prints.

## Next
- Default: `steer` (briefing + menus). `--go` / `--autonomous` skips.
- Grant (“activate this set”) → `change` then `advise` until ready,
  then pause unless `--go` / autonomous, then `/run`
- `change <id>` for each activated (or just-drafted) change node
- `advise <id>` after architecture / instrument `change`
- `brief` for brief nodes
- `direct fix` for vibe
- `act` only after activation, and after advise accept when required
- `--ask` / “run it by me”: pin current, present this page, stop.
  Do not `act`.
```

Node ids: kebab (`paste-cards`), no `nod-` prefix. Track as a bead
with `bd create --type node` (Type column). Change ids stay verb-led
(`add-`, `update-`, `remove-`, `refactor-`). Do not invent sprint
numbers. Legacy titles starting `nod-` still count as graph nodes.
