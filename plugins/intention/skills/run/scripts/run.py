#!/usr/bin/env python3
"""Campaign observe + stop predicate. Does not spawn workers.

Lives next to the run skill so a global `skills add` carries it.
Uses the sibling ready skill's script against the current project's
openspec/. Does not require the project to vendor ready.py.

  python3 <skill-dir>/scripts/run.py
  python3 <skill-dir>/scripts/run.py --until advise --ready-json FILE
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

STOPS = ("empty", "advise", "activation", "ask", "fold")


def sibling_ready_py() -> Path | None:
    cand = Path(__file__).resolve().parents[2] / "ready" / "scripts" / "ready.py"
    return cand if cand.is_file() else None


def find_openspec() -> Path | None:
    here = Path.cwd()
    for root in [here, *here.parents]:
        cand = root / "openspec"
        if cand.is_dir():
            return cand
        if (root / ".git").exists():
            return cand if cand.is_dir() else None
    return None


def find_ready_py() -> Path | None:
    sib = sibling_ready_py()
    if sib:
        return sib
    here = Path.cwd()
    for root in [here, *here.parents]:
        cand = root / "scripts" / "ready.py"
        if cand.is_file():
            return cand
        if (root / ".git").exists() or (root / "openspec").is_dir():
            break
    return None


def load_ready(path: Path | None) -> dict[str, Any]:
    if path:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SystemExit("ready-json must be an object")
        return data
    ready_py = find_ready_py()
    if ready_py is None:
        return {
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
            "missing": "ready.py",
        }
    argv = [sys.executable, str(ready_py), "--json"]
    openspec = find_openspec()
    if openspec is not None:
        argv.extend(["--root", str(openspec)])
    proc = subprocess.run(
        argv,
        check=False,
        capture_output=True,
        text=True,
        cwd=str(Path.cwd()),
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
    if data.get("missing"):
        return {
            "stop": "no-ready",
            "next": None,
            "focus": None,
            "until": until,
            "workers_launched": 0,
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
        }
    ready = ids(data.get("ready"))
    waiting = ids(data.get("waiting"))
    needs_advise = ids(data.get("needs_advise"))
    asks = ids(data.get("ask"))
    if pause_before and (pause_before in ready or pause_before in waiting or pause_before in needs_advise):
        return face("pause-before", pause_before, until, ready, waiting, needs_advise, asks)
    if until == "ask" and asks:
        return face("ask", asks[0], until, ready, waiting, needs_advise, asks)
    if until == "activation" and waiting:
        return face("activation", waiting[0], until, ready, waiting, needs_advise, asks)
    if until == "advise" and needs_advise:
        return face("advise", needs_advise[0], until, ready, waiting, needs_advise, asks)
    if not ready:
        return face("empty", None, until, ready, waiting, needs_advise, asks)
    return {
        "stop": None,
        "next": "act",
        "focus": ready[0],
        "until": until,
        "workers_launched": 0,
        "ready": ready,
        "waiting": waiting,
        "needs_advise": needs_advise,
        "ask": asks,
    }


def face(
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


def card(row: dict[str, Any]) -> str:
    stop = row["stop"] or "continue"
    focus = row.get("focus") or "—"
    return (
        f"┌─ RUN ─────────────────────────────────────────\n"
        f"│ until {row['until']} · stop {stop} · workers {row['workers_launched']}\n"
        f"│ next {row['next'] or '—'} · focus {focus}\n"
        f"│ ready {len(row['ready'])} · pending {len(row['waiting'])} · "
        f"advise {len(row['needs_advise'])} · ask {len(row['ask'])}\n"
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
    data = load_ready(args.ready_json)
    row = decide(data, until, args.pause_before)
    if args.json:
        print(json.dumps(row, indent=2))
    else:
        print(card(row))
        print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
