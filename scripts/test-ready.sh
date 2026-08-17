#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
python3 - "$ROOT" <<'PY'
import json, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
out = subprocess.check_output(
    [sys.executable, str(root / "ready.py"), "--json", "--root", str(root / "fixtures/ready/openspec")],
    text=True,
)
data = json.loads(out)
assert {r["id"] for r in data["ready"]} == {"advised-ok", "go-now", "needs-read"}, data["ready"]
assert {r["id"] for r in data["waiting"]} == {"wait-up"}, data["waiting"]
assert {r["id"] for r in data["parked"]} == {"on-ice", "fixture-host"}, data["parked"]
assert {r["id"] for r in data["needs_advise"]} == {"needs-read"}, data["needs_advise"]
print("pass ready fixture classify")
PY
python3 "$ROOT/ready.py" --json >/dev/null
echo "pass ready live tree"
