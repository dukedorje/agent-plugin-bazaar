#!/usr/bin/env bash
# Launch MetaCoding MCP serve.
#
# Resolution order:
#   1. $METACODING_ROOT — a local checkout (src/cli/bin.ts + package name)
#   2. cwd / git-root if that tree *is* the MetaCoding repo
#   3. `metacoding` on PATH (published `bun add -g @identikey/metacoding`)
#
# Never use bunx: it skips ladybugdb's native binary.
set -euo pipefail

is_checkout() {
  local root="$1"
  [[ -f "$root/src/cli/bin.ts" && -f "$root/package.json" ]] || return 1
  grep -q '"name": "@identikey/metacoding"' "$root/package.json"
}

run_checkout() {
  exec bun run "$1/src/cli/bin.ts" serve "$@"
}

if [[ -n "${METACODING_ROOT:-}" ]]; then
  if is_checkout "$METACODING_ROOT"; then
    run_checkout "$METACODING_ROOT" "$@"
  fi
  echo "metacoding plugin: METACODING_ROOT=$METACODING_ROOT is not a MetaCoding checkout (need src/cli/bin.ts)." >&2
  exit 1
fi

if command -v git >/dev/null; then
  git_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  if [[ -n "$git_root" ]] && is_checkout "$git_root"; then
    run_checkout "$git_root" "$@"
  fi
fi

if is_checkout "$(pwd)"; then
  run_checkout "$(pwd)" "$@"
fi

if command -v metacoding >/dev/null; then
  exec metacoding serve "$@"
fi

echo "metacoding plugin: no local checkout and no 'metacoding' on PATH." >&2
echo "Set METACODING_ROOT to a clone, or: bun add -g @identikey/metacoding" >&2
exit 1
