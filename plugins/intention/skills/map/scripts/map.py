#!/usr/bin/env python3
"""Observe-only map: intend-dag shape plus live status / wave / outcome.

  python3 <skill-dir>/scripts/map.py
  python3 <skill-dir>/scripts/map.py bazaar-6os
  python3 <skill-dir>/scripts/map.py --current bazaar-6os
  python3 <skill-dir>/scripts/map.py --current -
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SESSION_ENV = (
    "INTENTION_SESSION",
    "GROK_SESSION_ID",
    "CLAUDE_SESSION_ID",
    "CODEX_SESSION_ID",
)
SESSION_KEY_RE = re.compile(r"^[A-Za-z0-9._-]+$")

CHANGE_ID_RE = re.compile(
    r"^(add|update|remove|refactor)-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
BANNER_RE = re.compile(r"^>\s*\*\*(PENDING|ACTIVE BUILD|PARKED)\b")
ADVISE_RE = re.compile(
    r"^>\s*\*\*ADVISE:\*\*\s*(accept-with-nits|accept|send-back)\b",
    re.I,
)
CHECKBOX_RE = re.compile(r"^(\s*)[-*]\s+\[([ xX])\]\s+(.*)$")


def find_repo() -> Path:
    here = Path.cwd()
    for root in [here, *here.parents]:
        if (root / ".git").is_dir() or (root / ".beads").is_dir():
            return root
        if (root / "openspec").is_dir():
            return root
    return here


def find_openspec(repo: Path) -> Path | None:
    cand = repo / "openspec"
    return cand if cand.is_dir() else None


def landing_from_title(title: str) -> str | None:
    if not title:
        return None
    head = title.strip().split()[0].rstrip(":")
    return head if CHANGE_ID_RE.match(head) else None


def first_banner(text: str) -> str | None:
    for i, line in enumerate(text.splitlines()):
        if i >= 40:
            break
        m = BANNER_RE.match(line.strip())
        if m:
            return m.group(1)
    return None


def open_owed(tasks: str) -> list[str]:
    out: list[str] = []
    for line in tasks.splitlines():
        m = CHECKBOX_RE.match(line)
        if m and m.group(2).lower() != "x":
            out.append(m.group(3).strip())
    return out


def last_advise(change_dir: Path) -> str | None:
    reviews = change_dir / "reviews"
    if not reviews.is_dir():
        return None
    files = sorted(
        p for p in reviews.iterdir() if p.is_file() and p.name.endswith(".md")
    )
    if not files:
        return None
    for line in files[-1].read_text(encoding="utf-8").splitlines()[:40]:
        m = ADVISE_RE.match(line.strip())
        if m:
            return m.group(1).lower()
    return None


def find_change_dir(openspec: Path | None, change_id: str) -> Path | None:
    if openspec is None or not change_id:
        return None
    live = openspec / "changes" / change_id
    if live.is_dir() and (live / "proposal.md").is_file():
        return live
    archive = openspec / "changes" / "archive"
    if archive.is_dir():
        for child in sorted(archive.iterdir()):
            if child.is_dir() and child.name.endswith("-" + change_id):
                if (child / "proposal.md").is_file():
                    return child
    return None


def distilled_summary(repo: Path, bead_id: str) -> str | None:
    path = repo / "groups" / bead_id / "result.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    face = data.get("distilled") if isinstance(data.get("distilled"), dict) else {}
    summary = face.get("summary") or data.get("summary")
    return str(summary) if summary else None


def wave_and_banner(openspec: Path | None, landing: str | None) -> tuple[str, str | None]:
    if not landing:
        return "—", None
    dest = find_change_dir(openspec, landing)
    if dest is None:
        return "no change dir", None
    archived = "archive" in dest.parts
    banner = first_banner((dest / "proposal.md").read_text(encoding="utf-8"))
    advise = last_advise(dest)
    tasks = dest / "tasks.md"
    owed = open_owed(tasks.read_text(encoding="utf-8")) if tasks.is_file() else []
    bits: list[str] = []
    if archived:
        bits.append("folded")
    elif banner:
        bits.append(banner.lower().replace(" ", "-"))
    if advise:
        bits.append("advise " + advise)
    if banner == "ACTIVE BUILD" and not owed and not archived:
        bits.append("fold-debt")
    elif owed:
        bits.append(f"{len(owed)} open")
    return " · ".join(bits) if bits else "—", banner


def block_deps(rec: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for edge in rec.get("dependencies") or []:
        if not isinstance(edge, dict):
            continue
        if edge.get("type") in {None, "blocks"} and edge.get("depends_on_id"):
            if edge.get("issue_id", rec.get("id")) == rec.get("id"):
                out.append(str(edge["depends_on_id"]))
    return out


def bd_json(args: list[str]) -> Any:
    try:
        proc = subprocess.run(
            ["bd", *args, "--json"],
            check=False,
            capture_output=True,
            text=True,
            cwd=str(Path.cwd()),
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def session_key(explicit: str | None) -> str | None:
    if explicit and SESSION_KEY_RE.match(explicit):
        return explicit
    for var in SESSION_ENV:
        val = (os.environ.get(var) or "").strip()
        if val and SESSION_KEY_RE.match(val):
            return val
    return None


def default_store(key: str) -> Path:
    return Path.home() / ".intention" / "sessions" / key / "current.json"


def read_current(path: Path | None) -> str | None:
    if path is None or not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    roots = data.get("roots")
    if isinstance(roots, list) and roots and isinstance(roots[0], str) and roots[0]:
        return roots[0]
    return None


def write_current(path: Path, root: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "roots": [root],
        "set_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cwd": str(Path.cwd()),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def clear_current(path: Path | None) -> None:
    if path is None or not path.is_file():
        return
    path.unlink()


def load_open_epics() -> list[dict[str, Any]]:
    rows = bd_json(["list", "--status", "open"])
    if not isinstance(rows, list):
        return []
    return [r for r in rows if isinstance(r, dict) and r.get("issue_type") == "epic"]


def render_index(
    epics: list[dict[str, Any]],
    pinned: str | None,
) -> str:
    lines = ["# Intentions", ""]
    if pinned:
        lines.append(f"Current: `{pinned}`")
        lines.append("")
    else:
        lines.append("No current intention in this session.")
        lines.append("")
    if not epics:
        lines.append("(no open epics)")
    else:
        for ep in epics:
            nid = str(ep.get("id") or "")
            title = str(ep.get("title") or nid)
            mark = " *" if pinned and nid == pinned else ""
            lines.append(f"- `{nid}`{mark}  {title}")
    lines.extend(
        [
            "",
            "Pin with `map --current <id>`. Peek with `map <id>`. Clear with `map --current -`.",
            "",
        ]
    )
    return "\n".join(lines)


def as_rec(data: Any) -> dict[str, Any] | None:
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return data[0]
    if isinstance(data, dict):
        return data
    return None


def load_epic(scope: str | None, fixture: dict[str, Any] | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if fixture is not None:
        epic = fixture.get("epic") if isinstance(fixture.get("epic"), dict) else {}
        kids = fixture.get("children") if isinstance(fixture.get("children"), list) else []
        return epic, [k for k in kids if isinstance(k, dict)]
    if scope:
        rec = as_rec(bd_json(["show", scope]))
        if rec is None:
            return {"id": scope, "title": scope, "status": "missing"}, []
        kids = bd_json(["children", str(rec.get("id") or scope)])
        if rec.get("issue_type") != "epic" and not isinstance(kids, list):
            return rec, []
        if rec.get("issue_type") != "epic" and isinstance(kids, list) and not kids:
            return rec, []
        return rec, [k for k in (kids or []) if isinstance(k, dict)]
    return {"id": "", "title": "open work", "status": "open"}, []


def render_node(rec: dict[str, Any], repo: Path, openspec: Path | None) -> str:
    nid = str(rec.get("id") or "—")
    title = str(rec.get("title") or nid)
    landing = landing_from_title(title)
    status = str(rec.get("status") or "open")
    wave, _banner = wave_and_banner(openspec, landing)
    outcome = distilled_summary(repo, nid) or rec.get("close_reason") or "—"
    deps = block_deps(rec)
    kind = rec.get("issue_type") or ""
    lines = [
        f"### {nid}",
        f"- Goal: {title}",
        f"- Landing: `{landing}`" if landing else "- Landing: —",
        f"- Status: {status}" + (f" ({kind})" if kind else ""),
        f"- Wave: {wave}",
        f"- Outcome: {outcome}",
        f"- Depends on: {', '.join(deps) if deps else 'none'}",
    ]
    return "\n".join(lines)


def render(
    epic: dict[str, Any],
    children: list[dict[str, Any]],
    repo: Path,
    openspec: Path | None,
    pinned: str | None = None,
    peek: str | None = None,
) -> str:
    title = str(epic.get("title") or epic.get("id") or "map")
    desc = (epic.get("description") or "").strip()
    nodes = children if children else ([epic] if epic.get("id") else [])
    ready, need_act, done, failed = [], [], [], []
    for rec in nodes:
        st = str(rec.get("status") or "open")
        landing = landing_from_title(str(rec.get("title") or ""))
        dest = find_change_dir(openspec, landing) if landing else None
        banner = first_banner((dest / "proposal.md").read_text(encoding="utf-8")) if dest else None
        advise = last_advise(dest) if dest else None
        nid = str(rec.get("id") or "")
        if st == "closed":
            done.append(nid)
        elif st in {"blocked"} or advise == "send-back":
            failed.append(nid)
        elif banner == "PENDING":
            need_act.append(nid or landing or "")
        elif st in {"open", "in_progress"}:
            ready.append(nid)
    body: list[str] = []
    if pinned:
        body.append(f"Current: `{pinned}`")
        if peek and peek != pinned:
            body.append(f"Peek: `{peek}`")
        body.append("")
    body.extend(
        [
            f"# {title}",
            "",
        ]
    )
    if desc:
        # Keep the gathering short: first paragraph only.
        first = desc.split("\n\n", 1)[0]
        lines = [ln for ln in first.splitlines() if not ln.startswith("#")]
        lede = " ".join(lines).strip()
        if lede:
            body.extend([lede, ""])
    body.extend(["## DAG", ""])
    if not nodes:
        body.append("(no nodes)")
    else:
        body.append("\n\n".join(render_node(r, repo, openspec) for r in nodes))
    body.extend(
        [
            "",
            "## Ready-set",
            ", ".join(ready) if ready else "(none)",
            "",
            "## Needs activation",
            ", ".join(need_act) if need_act else "(none)",
            "",
            "## Done",
            ", ".join(done) if done else "(none)",
            "",
            "## Failed / send-back",
            ", ".join(failed) if failed else "(none)",
            "",
            "## Next",
        ]
    )
    if need_act:
        body.append("- `change` / activate: " + ", ".join(need_act))
    if ready:
        body.append("- `act` or `/run --until roll`: " + ", ".join(ready))
    if not need_act and not ready and done and not failed:
        body.append("- `/fold` if a change is still inflight; else nothing dispatchable")
    if not need_act and not ready and not done:
        body.append("- `/intend` or `/run --until roll`")
    return "\n".join(body) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scope", nargs="?", help="peek this DAG without changing current")
    p.add_argument(
        "--current",
        metavar="ID",
        help="pin this DAG as current for this session (`-` to clear)",
    )
    p.add_argument("--session", help="session key (default: GROK_SESSION_ID / INTENTION_SESSION)")
    p.add_argument(
        "--store",
        type=Path,
        help="directory for current.json (default: ~/.intention/sessions/<session>/)",
    )
    p.add_argument("--fixture", type=Path)
    args = p.parse_args()
    fixture = None
    if args.fixture:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        if not isinstance(fixture, dict):
            raise SystemExit("fixture must be a JSON object")

    store_path: Path | None
    if args.store is not None:
        store_path = args.store / "current.json"
    else:
        key = session_key(args.session)
        store_path = default_store(key) if key else None

    if args.current is not None:
        if store_path is None:
            print(
                "no session id — pass --session NAME or set "
                "INTENTION_SESSION / GROK_SESSION_ID",
                file=sys.stderr,
            )
            return 2
        if args.current in {"-", ""}:
            clear_current(store_path)
        else:
            write_current(store_path, args.current)

    pinned = read_current(store_path)
    scope = args.scope
    if scope is None and args.current and args.current not in {"-", ""}:
        scope = args.current
    if scope is None and pinned:
        scope = pinned

    repo = find_repo()
    openspec = find_openspec(repo)

    if fixture is not None and isinstance(fixture.get("epics"), list) and "epic" not in fixture:
        epics = [e for e in fixture["epics"] if isinstance(e, dict)]
        print(render_index(epics, pinned), end="")
        return 0

    if scope is None and fixture is None:
        print(render_index(load_open_epics(), pinned), end="")
        return 0

    epic, children = load_epic(scope, fixture)
    if epic.get("status") == "missing":
        print(f"unresolved: {epic.get('id')}", file=sys.stderr)
        return 1
    peek = scope if pinned and scope != pinned else None
    print(
        render(epic, children, repo, openspec, pinned=pinned, peek=peek),
        end="",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
