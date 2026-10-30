#!/usr/bin/env python3
"""Build the Jev Choice body for the next harness command.

The machine is references/transitions.json. This prints the request.
It does not call the API.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACHINE = ROOT / "references" / "transitions.json"


def load() -> dict:
    data = json.loads(MACHINE.read_text(encoding="utf-8"))
    commands = data["commands"]
    if "other" not in commands:
        raise SystemExit("missing command other")
    states = data["states"]
    for name, state in states.items():
        nxt = state.get("next") or []
        if "other" not in nxt:
            raise SystemExit(f"{name}: other is not legal")
        unknown = [item for item in nxt if item not in commands]
        if unknown:
            raise SystemExit(f"{name}: unknown commands {unknown}")
        if len(nxt) != len(set(nxt)):
            raise SystemExit(f"{name}: duplicate commands")
    for flow in data.get("workflows") or []:
        missing = [item for item in flow.get("path") or [] if item not in states]
        if missing:
            raise SystemExit(f"{flow.get('name')}: unknown states {missing}")
    return data


def body(data: dict, state: str, turn: str) -> dict:
    if state not in data["states"]:
        known = ", ".join(data["states"])
        raise SystemExit(f"unknown state {state!r}. known: {known}")
    criteria = {
        command: data["commands"][command] for command in data["states"][state]["next"]
    }
    text = turn.rstrip()
    if text:
        text += "\n"
    text += f"current_state: {state}"
    return {
        "model": data["model"],
        "state": text,
        "questions": {
            data["question"]: {
                "type": "choice",
                "instructions": data["instructions"],
                "criteria": criteria,
            },
            "waiting_on_person": {
                "type": "noul",
                "instructions": (
                    "Is the harness waiting on a person for a decision, "
                    "a look, or a spike verdict?"
                ),
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", help="current intention state")
    parser.add_argument("--turn", default="", help="last harness turn")
    parser.add_argument("--check", action="store_true", help="validate the machine")
    args = parser.parse_args()
    data = load()
    if args.check and not args.state:
        print(f"ok {len(data['states'])} states")
        return 0
    if not args.state:
        parser.error("--state is required unless --check")
    json.dump(body(data, args.state, args.turn), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
