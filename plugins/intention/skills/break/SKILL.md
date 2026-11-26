---
name: break
description: >
  Adversarial read of a change, a design, or a landed system. Try to
  break it, hack the claims, find the holes an attacker would use, and
  write those findings. Use when asked to attack it, red-team it, find
  flaws, or model an attacker. Does not accept a review, implement, or
  write an exploit.
user-invocable: true
argument-hint: "[<change-id or paths>]"
---

# break

Load `../../references/shared.md`. You are an attacker reading this
artifact. You are not the author and you are not the advise reader.
You do not implement. You do not fold. You do not write
`**ADVISE:**` and you do not flip a banner.

`advise` asks whether the design is sound. This skill asks what a
hostile party can already do with the thing as written.

## Target

The named change-id, the paths they gave, or the pinned intention.
Read the proposal, the design, and the code those cite. Read the
claims about who is trusted, what is withheld, and what cannot happen.
If there is no artifact yet, stop and say so.

## Attacker

Pick one concrete party who wants something this system is supposed to
withhold or protect: data, authority, money, integrity, or the ability
to leave with their own keys and data. Name what they want in one line.
Stay on this artifact. Do not wander into unrelated systems.

## How to try

Take each claim that something cannot happen, or that a boundary holds,
and try to make it fail with what the artifact actually allows:

- A client that lies, replays, or skips a step
- A write that finishes halfway, or two writers on the same state
- A token, grant, or role used for a job it was not given
- A deputy that acts with someone else's authority
- An exit that loses keys or data, or an action that cannot be undone
- A check that trusts a name, a path, or a caller it did not verify

Prefer the hole that needs the least and gets the attacker the most.
Drop a finding you cannot point at in the artifact. A worry without a
path is not a hole.

## Report

Print the findings in chat, worst first. Each one:

```markdown
**HOLE** <one line: what the attacker gets>
Wants: <the goal>
Assumes: <the claim that does not hold>
Evidence: <file, and the behavior>
Close: <one line on what would shut it>
```

Zero holes is a real result. Say what you tried.

When `openspec/changes/<id>/` exists, also write
`reviews/<YYYY-MM-DD>-break.md` with the same findings. No verdict
line. That file does not unblock or block `act`.

## Stop

Do not patch. Do not write a payload, a command sequence, or the steps
that carry an attack out. The finding names the hole. A repair is a
later `change` if they ask.
