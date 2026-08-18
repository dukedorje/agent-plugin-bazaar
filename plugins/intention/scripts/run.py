#!/usr/bin/env python3
"""Campaign observe + stop predicate. Does not spawn workers.

  python3 plugins/intention/scripts/run.py
  python3 plugins/intention/scripts/run.py --until advise --ready-json FILE
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
READY = REPO / "scripts" / "ready.py"

STOPS = ("empty", "advise", "activation", "ask", "fold")


def load_ready(path: Path | None) -> dict[str, Any]:
    if path:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SystemExit("ready-json must be an object")
        return data
    proc = subprocess.run(
        [sys.executable, str(READY), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or "ready.py failed")
    return json.loads(proc.stdout)


def ids(rows: Any) -> list[str]:
    if not isinstance(rows, list):
        return []
    out: list[str] = []
    for row in rows:
        if isinstance(row, dict) and row.get("id"):
            out.append(str(row["id"]))
        elif isinstance(row, str):
            out.append(row)
    return out


def decide(data: dict[str, Any], until: str, pause_before: str | None) -> dict[str, Any]:
    ready = ids(data.get("ready"))
    waiting = ids(data.get("waiting"))
    needs_advise = ids(data.get("needs_advise"))
    asks = ids(data.get("ask"))
    if pause_before and (pause_before in ready or pause_before in waiting or pause_before in needs_advise):
        return stop("pause-before", pause_before, until, ready, waiting, needs_advise, asks)
    if until == "ask" and asks:
        return stop("ask", asks[0], until, ready, waiting, needs_advise, asks)
    if until == "activation" and waiting:
        return stop("activation", waiting[0], until, ready, waiting, needs_advise, asks)
    if until == "advise" and needs_advise:
        return stop("advise", needs_advise[0], until, ready, waiting, needs_advise, asks)
    if not ready:
        return stop("empty", None, until, ready, waiting, needs_advise, asks)
    nxt = "act"
    if until == "fold":
        nxt = "act"
    return {
        "stop": None,
        "next": nxt,
        "focus": ready[0],
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
    }


def stop(
    why: str,
    focus: str | None,
    until: str,
    ready: list[str],
    waiting: list[str],
    needs_advise: list[str],
    asks: list[str],
) -> dict[str, Any]:
    return {
        "stop": why,
        "next": None,
        "focus": focus,
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
    }


def card(face: dict[str, Any]) -> str:
    stop = face["stop"] or "continue"
    focus = face.get("focus") or "—"
    return (
        f"┌─ RUN ─────────────────────────────────────────\n"
        f"│ until {face['until']} · stop {stop} · workers {face['workers_launched']}\n"
        f"│ next {face['next'] or '—'} · focus {focus}\n"
        f"│ ready {len(face['ready'])} · pending {len(face['waiting'])} · "
        f"advise {len(face['needs_advise'])} · ask {len(face['ask'])}\n"
        f"└───────────────────────────────────────────────"
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--until", choices=STOPS, default="empty")
    p.add_argument("--autonomous", action="store_true")
    p.add_argument("--pause-before")
    p.add_argument("--ready-json", type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    until = args.until
    if args.autonomous and until == "empty":
        until = "empty"
    data = load_ready(args.ready_json)
    face = decide(data, until, args.pause_before)
    if args.json:
        print(json.dumps(face, indent=2))
    else:
        print(card(face))
        print(json.dumps(face))
    return 0


if __name__ == "__main__":
    sys.exit(main())
