# update-fold-base-and-run

> **ACTIVE BUILD**

Folded in the same commit that landed the behavior. The human asked for both changes after the architecture review.

## Why

A MODIFIED paste written before an upstream fold can drop clauses when fold replaces the living block. "Activate this set" was also pausing even when the human had already said to run.

## What

- Record a git blob of the living spec on every MODIFIED or REMOVED requirement.
- Fold applies nothing when that requirement's text has changed. The same run sends the change back through change for a union re-paste.
- A missing blob is a hand diff for this release, not a refusal.
- "Activate this set" still pauses after contracts. "And run" and "run this whole intention" enter run.

## Impact

- Capabilities: MODIFIED verbs, MODIFIED living-specs
- ADRs: none

## User journey & surfaces

No new UI because the surfaces are the intend utterance, the run card (`reason: stale-base`), and `fold_base.py check`.

## Out of scope

- A new mailbox, a rewind verb, and a default demo gate.
- Flipping banners from a future web UI.
- Pre-activating blocked descendants.
