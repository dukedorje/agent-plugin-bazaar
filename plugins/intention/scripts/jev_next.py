#!/usr/bin/env python3
"""Build or send the Jev Choice for the next harness command.

The machine is references/transitions.json. --call reads the whole
conversation on stdin, posts it, and prints one SEND or HOLD line.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
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


SAY = {
    "intend": "intend",
    "intend_ask": "intend --ask",
    "steer": "steer",
    "change": "change",
    "advise": "advise",
    "act": "act",
    "activate": "activate this set",
    "activate_and_run": "activate and run",
    "run": "/run",
    "demo": "demo",
    "fold": "fold",
    "brief": "brief",
    "debrief": "debrief",
    "consult": "consult",
    "spike": "run the open spike",
    "status": "status",
    "map": "map",
}

# Leave room for the machine text under Jev's request budget.
TURN_LIMIT = 40_000


def conversation_body(data: dict, turn: str) -> dict:
    text = turn.strip()
    if len(text) > TURN_LIMIT:
        text = text[-TURN_LIMIT:]
    lines = ["Legal next commands by state:"]
    for name, state in data["states"].items():
        lines.append(f"{name}: {', '.join(state['next'])}")
    lines.append("")
    lines.append("Conversation:")
    lines.append(text)
    state_criteria = {
        name: state["means"] for name, state in data["states"].items()
    }
    return {
        "model": data["model"],
        "state": "\n".join(lines),
        "questions": {
            "current_state": {
                "type": "choice",
                "instructions": "Which intention state is this conversation in?",
                "criteria": state_criteria,
            },
            data["question"]: {
                "type": "choice",
                "instructions": data["instructions"],
                "criteria": data["commands"],
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


HUMAN = {"ask", "eyes", "spike", "advising"}
# A lead smaller than this is a tie. The gap is what matters, not a 0.5 floor.
FLAT = 0.05


def nodes_are_open(turn: str) -> bool:
    text = turn.lower()
    return (
        "still open" in text
        or "stays open" in text
        or "open nodes" in text
        or "open node" in text
    )


def verdict(data: dict, payload: dict, turn: str = "") -> dict:
    answers = payload["answers"]
    inferred = answers["current_state"]["choice"]
    command = answers["next_command"]
    waiting = float(answers["waiting_on_person"]["noul"])
    confidence = float(command["confidence"])
    probabilities = command["probabilities"]
    ranked = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    peak, top = ranked[0] if ranked else (command["choice"], 0.0)
    second = ranked[1][1] if len(ranked) > 1 else 0.0
    lead = top - second
    legal_set = data["states"].get(inferred, {}).get("next", [])
    open_nodes = nodes_are_open(turn)
    reason = "lead"
    choice = peak
    if open_nodes and inferred not in HUMAN:
        choice = "run"
        reason = "open-nodes"
        send = True
    else:
        send = choice not in {"other", "answer"} and choice in legal_set and lead >= FLAT
        if lead < FLAT:
            reason = "flat"
    return {
        "send": send,
        "say": SAY.get(choice, ""),
        "choice": choice,
        "state": inferred,
        "confidence": confidence,
        "waiting": waiting,
        "legal": choice in legal_set,
        "lead": lead,
        "reason": reason,
        "open_nodes": open_nodes,
        "probabilities": probabilities,
    }


def call(data: dict, turn: str, out: Path | None) -> dict:
    key = os.environ.get("TYPESAFE_API_KEY", "")
    if not key:
        raise SystemExit("TYPESAFE_API_KEY is unset")
    body = conversation_body(data, turn)
    request = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")[:500]
        raise SystemExit(f"Jev HTTP {error.code}: {detail}") from error
    decision = verdict(data, payload, turn)
    if out is not None:
        out.write_text(json.dumps({"decision": decision, "response": payload}, indent=2) + "\n", encoding="utf-8")
    return decision


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", help="current intention state")
    parser.add_argument("--turn", default="", help="last harness turn")
    parser.add_argument("--check", action="store_true", help="validate the machine")
    parser.add_argument("--call", action="store_true", help="post stdin to Jev")
    parser.add_argument("--out", help="write the full Jev response here")
    args = parser.parse_args()
    data = load()
    if args.call:
        decision = call(data, sys.stdin.read(), Path(args.out) if args.out else None)
        kind = "SEND" if decision["send"] else "HOLD"
        phrase = decision["say"] or decision["choice"]
        print(
            f"{kind} |||{phrase}||| "
            f"state={decision['state']} lead={decision['lead']:.2f} "
            f"reason={decision['reason']} waiting={decision['waiting']:.2f} "
            f"legal={str(decision['legal']).lower()}"
        )
        return 0
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
