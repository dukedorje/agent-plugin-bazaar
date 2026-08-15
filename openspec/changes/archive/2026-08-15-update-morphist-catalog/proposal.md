# update-morphist-catalog

> **ACTIVE BUILD** → folded and archived 2026-08-15.

## Why

CLAUDE.md still listed skills removed 2026-07-28. Marketplace said
morphist-tools 1.18.1 while plugin.json said 2.0.0, so `validate.sh`
failed. sprint-exec still invoked `exec-report`.

## What

Catalogs match disk. Version 2.0.0. sprint-exec huddle/report inline.

## User journey & surfaces

No new UI because the surfaces are CLAUDE.md and `./validate.sh`.
Working: the skills table is the kept set; validate is green.
Empty: a dropped name is gone. Failed: validate version mismatch.
Off: CONVENTIONS still names what was dropped.

## Out of scope

- Rewriting every `/sprint-plan first` halt string in morphist skills
- Unparking P1
