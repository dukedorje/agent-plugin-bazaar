#!/usr/bin/env python3
"""Observe-only map: intend-dag shape plus live status / wave / outcome.

  python3 <skill-dir>/scripts/map.py [scope]
  python3 <skill-dir>/scripts/map.py --fixture FILE.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

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
    epics = bd_json(["list", "--status", "open"])
    rows = epics if isinstance(epics, list) else []
    open_epics = [r for r in rows if isinstance(r, dict) and r.get("issue_type") == "epic"]
    if not open_epics:
        return {"id": "", "title": "open work", "status": "open"}, []
    if len(open_epics) == 1:
        eid = str(open_epics[0].get("id") or "")
        kids = bd_json(["children", eid]) if eid else []
        return open_epics[0], [k for k in (kids or []) if isinstance(k, dict)]
    # Several epics: flatten children under a synthetic root.
    kids: list[dict[str, Any]] = []
    for ep in open_epics:
        kids.append(ep)
        eid = str(ep.get("id") or "")
        more = bd_json(["children", eid]) if eid else []
        if isinstance(more, list):
            kids.extend(k for k in more if isinstance(k, dict))
    return {"id": "", "title": "open work", "status": "open", "description": ""}, kids


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


def render(epic: dict[str, Any], children: list[dict[str, Any]], repo: Path, openspec: Path | None) -> str:
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
    body = [
        f"# {title}",
        "",
    ]
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
    p.add_argument("scope", nargs="?")
    p.add_argument("--fixture", type=Path)
    args = p.parse_args()
    fixture = None
    if args.fixture:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        if not isinstance(fixture, dict):
            raise SystemExit("fixture must be a JSON object")
    repo = find_repo()
    openspec = find_openspec(repo)
    epic, children = load_epic(args.scope, fixture)
    if epic.get("status") == "missing":
        print(f"unresolved: {epic.get('id')}", file=sys.stderr)
        return 1
    print(render(epic, children, repo, openspec), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
