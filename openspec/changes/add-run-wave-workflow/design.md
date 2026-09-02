# Design — run-wave

## Two dispatch paths

| Host / assignee | How |
|---|---|
| This session is Grok, wave size ≥ 2 | `workflow` `run-wave` |
| This session is Grok, wave size 1, assignee grok | `spawn_subagent` `general-purpose` |
| Assignee claude / codex | `spawn.py` adapter |

The packet is the brief in every path. Foreign hosts still never see
a slash command.

## Why not host isolation_worktree

Grok `isolation_worktree` does not merge into the parent. Our merge
path is `conductor.py isolate` + `persist --worktree`. Wave children
use that.

## Disjoint subset

`conductor.py ready` `dispatchable` is capped by `max_inflight` and
disjoint from *in-flight* paths, not from each other. `wave` walks
that list and keeps a node only when its paths miss the ones already
picked.

## Take before launch

The conductor `take`s every wave node before `workflow` starts. A
child that `take`s again fails. Release on infra-red.

## One wave, not the campaign

Rhai does not read OpenSpec banners or spawn Sol. `/run` still
observes, picks fold/advise/change, and re-enters the loop. The
workflow is only the act fan-out inside a wave.
