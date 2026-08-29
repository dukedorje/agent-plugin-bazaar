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
- Group: solo | weave | fork | human-gate | conductor-workers | …
- Members / roles: conductor · worker · consultant · reader · human · group
- Density: lean | standard | explicit   ← from ladder.py; inverse of capability
- Surface: skill-host | packet-only
- Assignee: `ladder.py assign --shape <known|thinking|design|plan|architecture-review>`
- Consult: plan/replan → Fable 5; write stays here
- Architecture: review-pair, reader = Grok (Sol only if ladder says available)
- Activation: none | needs human | already activated
- Acceptance: command `…` | journey | contrast | none

## Ready-set
Nodes with all inbound edges satisfied.

## Needs activation
Architecture / instrument / sensitive writes still PENDING.

## Next
- `change <id>` for each activated (or just-drafted) change node
- `advise <id>` after architecture / instrument `change`
- `brief` for brief nodes
- `direct fix` for vibe
- `act` only after activation, and after advise accept when required
- `--ask` / “run it by me”: pin current, present this page, stop.
  Do not `act`.
```

Node ids: `nod-<kebab>`. Change ids: verb-led (`add-`, `update-`, `remove-`,
`refactor-`). Do not invent sprint numbers.
