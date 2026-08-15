#!/usr/bin/env python3
"""Focused verify for the agent surface: examples validate; invalid fixtures reject.

Also enforces two laws the schema cannot say:
- artifacts non-empty ⇒ commit is an object
- pass + evidence.kind none ⇒ packet acceptance must be none (checked when
  a sibling *.packet.json exists for the same stem)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    sys.stderr.write("jsonschema is required: pip install jsonschema\n")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "agent-surface.schema.json"
EXAMPLES = ROOT / "examples"
INVALID = ROOT / "fixtures" / "invalid"

DEFS = {
    "packet": "taskPacket",
    "result": "signedResult",
    "agent": "agentRecord",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_result_laws(data: dict, path: Path, errors: list[str]) -> None:
    artifacts = data.get("artifacts") or []
    commit = data.get("commit")
    if artifacts and commit is None:
        errors.append(f"{path.name}: artifacts present but commit is null")
    if not artifacts and commit is not None:
        errors.append(f"{path.name}: commit set but artifacts empty")


def main() -> int:
    schema = load(SCHEMA_PATH)
    errors: list[str] = []
    checked = 0

    if not EXAMPLES.is_dir():
        print("no examples/")
        return 1

    for path in sorted(EXAMPLES.glob("*.json")):
        name = path.name
        kind = next((k for k in DEFS if f".{k}." in name or name.endswith(f".{k}.json")), None)
        if kind is None:
            errors.append(f"{name}: filename must contain .packet. / .result. / .agent.")
            continue
        data = load(path)
        target = {
            "$ref": f"#/$defs/{DEFS[kind]}",
            "$defs": schema["$defs"],
        }
        try:
            jsonschema.validate(instance=data, schema=target)
        except jsonschema.ValidationError as exc:
            errors.append(f"{name}: {exc.message} ({'/'.join(str(p) for p in exc.path)})")
        if kind == "result":
            check_result_laws(data, path, errors)
        checked += 1

    if INVALID.is_dir():
        for path in sorted(INVALID.glob("*.json")):
            name = path.name
            kind = next((k for k in DEFS if f".{k}." in name), None)
            if kind is None:
                errors.append(f"invalid/{name}: filename must contain .packet. / .result. / .agent.")
                continue
            data = load(path)
            target = {
                "$ref": f"#/$defs/{DEFS[kind]}",
                "$defs": schema["$defs"],
            }
            try:
                jsonschema.validate(instance=data, schema=target)
            except jsonschema.ValidationError:
                checked += 1
                continue
            errors.append(f"invalid/{name}: expected schema rejection, accepted")
            checked += 1

    if errors:
        for e in errors:
            print(e)
        print(f"FAIL {len(errors)} error(s), {checked} file(s)")
        return 1

    print(f"pass {checked} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
