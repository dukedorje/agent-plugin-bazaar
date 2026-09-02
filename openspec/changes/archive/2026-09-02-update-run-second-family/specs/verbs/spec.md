## ADDED Requirements

### Requirement: second-family advise is spawned, not parked

When `next` is `advise` and this session’s harness is the same family
as the change author, `run` SHALL assign an available
`architecture-review` route whose `harness` differs from the author
(`ladder.py assign --shape architecture-review --not-harness <author>`)
and SHALL spawn that reader (packet + `spawn.py`). It SHALL wait for
that wave so the review can land, then re-observe. It SHALL NOT halt.
It SHALL NOT `--punt` that id unless no other-family route is
available or the spawn is `infra-red` after one retry. It SHALL NOT
write a sole-author `accept` or a fake `send-back` with no
architecture boxes. `--until roll` SHALL NOT treat same-family advise
as stuck or as an ASK park. `--punt` SHALL NOT be the first response
to ADR-005.

`advise` SHALL treat second family as any `architecture-review` harness
other than the author’s. A Grok-authored change SHALL spawn a Claude
reader when that route is available. A Claude-authored change SHALL
spawn Grok or Sol. “Sol unavailable” SHALL NOT mean no second family
while a Claude or Grok route remains available.

#### Scenario: Grok author, roll, Fable available

- GIVEN `--until roll`, Grok authored `add-x`, `add-x` is in
  `needs_advise`, and `sol-arch-review` is unavailable
- WHEN the conductor’s session is Grok
- THEN `next` is `advise` and the conductor spawns the Claude
  `architecture-review` route
- AND the campaign does not stop empty
- AND `add-x` is not `--punt`ed

#### Scenario: No other-family route

- GIVEN `next: advise` and `ladder.py assign --shape architecture-review --not-harness <author>` fails
- WHEN the conductor cannot spawn a different family
- THEN it `--punt`s that id
- AND it does not write a fake send-back
