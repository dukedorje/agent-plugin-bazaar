## ADDED Requirements

### Requirement: Execution frontier preparation

Before dispatch, the conductor SHALL reconcile each candidate with its
upstream results and usable artifacts, current code and living specs, and
relevant learnings. Activation SHALL NOT establish preparedness. Blocked
descendants SHALL remain provisional goals, dependencies, assumptions, and
intended acceptance rather than require fully designed contracts up front.

Change/architecture/instrument nodes SHALL use `change`; brief nodes SHALL
use `brief`; direct fixes SHALL use a lightweight check. A preparation note
in the existing bead or proposal SHALL identify input references, outcome,
and authority. Unchanged inputs and contracts MAY reuse preparation after
checking them, including on resume; unrelated commits SHALL NOT invalidate
it. Still-valid contracts SHALL NOT require manufactured delta edits.

Routine refinements within authority SHALL continue. Changed scope or
architectural commitments SHALL return through intend/steer for a human
decision; stale nodes SHALL NOT dispatch. Revised architecture/instrument
contracts SHALL add the owed task `Fresh advise after preparation`.
An unchecked marker SHALL make `needs_advise` true despite historical
acceptance; only a fresh accepting reader SHALL close that marker, recording
the reviewed contract reference. Send-back SHALL leave it open.

The conductor SHALL re-observe after contract, dependency, activation, or
review changes. Every parallel candidate SHALL be prepared before packets
are refreshed and disjointness computed; dispatch SHALL be restricted to
prepared, authorized, in-scope candidates. The run card SHALL expose
`prepare_before_act` candidates for act decisions and an empty list for
non-act decisions. This metadata SHALL NOT claim semantic preparation or
grant authority; direct act and older cards SHALL obey the same policy.

#### Scenario: Activated downstream design is stale
- GIVEN an activated node whose upstream result changes its assumptions
- WHEN it becomes dispatchable
- THEN change reconciles the contract before act and revised architecture
  requires fresh advise even when an old accept exists

#### Scenario: No design change needed
- GIVEN prepared inputs and contract remain unchanged
- WHEN the conductor checks again
- THEN it may dispatch without rewriting deltas or repeating a change loop

#### Scenario: Parallel preparation
- GIVEN two disjoint ready candidates and an unrelated global wave candidate
- WHEN run selects a wave
- THEN every selected member has current preparation and refreshed packets
  and the unrelated candidate is excluded

### Requirement: Bounded campaign activation

A human instruction to run a whole named intention SHALL grant continuing
activation/write authority within its agreed goals, non-goals, and
architectural commitments. The conductor SHALL record the instruction and
bounds on the existing root bead or chat DAG. Bare run SHALL NOT invent
this grant. Only change SHALL apply it after preparation to dependency-ready
PENDING nodes, including existing proposals; blocked descendants SHALL NOT
be pre-activated by the conductor. Explicit activation SHALL remain valid
within its approved scope but SHALL NOT waive preparation.

Run SHALL consider eligible PENDING nodes covered by that recorded grant
before treating activation as terminal, follow change, then re-observe.
Explicit plan/ask/advise/wait/tidy/pause boundaries and skip/punt policy
SHALL take precedence. PARKED, sensitive permission, unresolved ambiguity,
explicit human gates, and ASK/EYES SHALL NOT be bypassed. Missing authority
SHALL leave PENDING. Changed commitments SHALL require a human decision.

#### Scenario: Existing draft within campaign bounds
- GIVEN a recorded whole-intention grant and a dependency-ready PENDING draft
- WHEN change confirms or refines its contract within the grant
- THEN change may activate it and run re-observes before execution

#### Scenario: No grant or explicit stopping boundary
- GIVEN bare run without campaign authority, or run with an explicit wait gate
- WHEN a PENDING node is encountered
- THEN existing activation and stopping rules apply without automatic activation

#### Scenario: Discovery changes commitments
- GIVEN a whole-intention grant
- WHEN preparation discovers a scope or architectural commitment change
- THEN the affected branch returns to the human and unrelated eligible work
  can continue under existing campaign policy
