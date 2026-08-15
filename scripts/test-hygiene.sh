#!/usr/bin/env bash
# Discriminating fixtures for G1. Each bad tree must fail; the good tree must pass.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
CHECK=(python3 "$ROOT/check-hygiene.py" --root)
fail() { echo "FAIL: $1"; exit 1; }

# ok
"${CHECK[@]}" "$ROOT/fixtures/hygiene/ok-pending" >/dev/null || fail "ok-pending should pass"

# no-banner
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/no-banner" >/dev/null 2>&1; then
  fail "no-banner should fail"
fi

# fold-debt
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/fold-debt" >/dev/null 2>&1; then
  fail "fold-debt should fail"
fi

# no-journey
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/no-journey" >/dev/null 2>&1; then
  fail "no-journey should fail"
fi

# scope checkbox
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/scope-box" >/dev/null 2>&1; then
  fail "scope-box should fail"
fi

# stall checkbox
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/stall" >/dev/null 2>&1; then
  fail "stall should fail"
fi

# fold-debt by omission (no tasks.md)
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/fold-debt-no-tasks" >/dev/null 2>&1; then
  fail "fold-debt-no-tasks should fail"
fi

# fold-debt by prose-only tasks
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/fold-debt-prose" >/dev/null 2>&1; then
  fail "fold-debt-prose should fail"
fi

# findings as checkboxes
if "${CHECK[@]}" "$ROOT/fixtures/hygiene/findings-box" >/dev/null 2>&1; then
  fail "findings-box should fail"
fi

# live tree
"${CHECK[@]}" "$ROOT/../openspec" >/dev/null || fail "live openspec should pass"

echo "pass hygiene fixtures + live tree"
