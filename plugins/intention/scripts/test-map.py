#!/usr/bin/env python3
"""Focused verify: map.py prints intend-dag shape with live residue."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = Path(__file__).resolve().parents[1] / "skills" / "map" / "scripts" / "map.py"
DROP_ENV = (
    "INTENTION_SESSION",
    "GROK_SESSION_ID",
    "CLAUDE_SESSION_ID",
    "CODEX_SESSION_ID",
)


def run(
    args: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(MAP), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd),
        env=env,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def blocks(issue_id: str, depends_on: str) -> dict:
    return {
        "issue_id": issue_id,
        "depends_on_id": depends_on,
        "type": "blocks",
    }


def section_after(out: str, heading: str) -> str:
    token = "## " + heading
    if token not in out:
        raise AssertionError(f"missing {heading}: {out}")
    return out.split(token, 1)[1].split("\n## ", 1)[0]


def ids_in(section: str) -> list[str]:
    text = section.strip()
    if not text or text == "(none)":
        return []
    return [part.split(" (on ", 1)[0].strip() for part in text.split(",") if part.strip()]


def map_fixture(root: Path, fixture: dict) -> str:
    (root / "openspec").mkdir(exist_ok=True)
    path = root / "fix.json"
    path.write_text(json.dumps(fixture), encoding="utf-8")
    proc = run(["--fixture", str(path)], cwd=root)
    expect(proc.returncode == 0, proc.stderr + proc.stdout)
    return proc.stdout


def write_change(
    root: Path,
    change_id: str,
    banner: str,
    advise: str | None = None,
) -> None:
    dest = root / "openspec" / "changes" / change_id
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "proposal.md").write_text(
        f"> **{banner}**\n\n# {change_id}\n",
        encoding="utf-8",
    )
    if advise:
        reviews = dest / "reviews"
        reviews.mkdir(exist_ok=True)
        (reviews / "2026-09-15-advise.md").write_text(
            f"> **ADVISE:** {advise}\n\nnotes\n",
            encoding="utf-8",
        )


def test_fixture_epic() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {
                "id": "bazaar-6os",
                "title": "debrief: expand a finished or failed unit",
                "status": "open",
                "description": "Opposite analog of brief.",
            },
            "children": [
                {
                    "id": "bazaar-6os.1",
                    "title": "add-debrief-verb: opposite analog of brief",
                    "status": "closed",
                    "issue_type": "feature",
                    "close_reason": "act landed 3f054b9",
                    "dependencies": [],
                }
            ],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = proc.stdout
        expect("# debrief: expand a finished or failed unit" in out, out)
        expect("### bazaar-6os.1" in out, out)
        expect("Status: closed" in out, out)
        expect("act landed 3f054b9" in out, out)
        expect("## Ready-set" in out, out)
        expect("## Done" in out, out)
        expect("bazaar-6os.1" in out.split("## Done", 1)[1], out)


def test_unresolved_scope() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = {
            "epic": {"id": "nope", "title": "nope", "status": "missing"},
            "children": [],
        }
        path = Path(td) / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path), "nope"], cwd=Path(td))
        expect(proc.returncode == 1, proc.stdout)
        expect("unresolved" in proc.stderr, proc.stderr)


def test_index_not_a_dump() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu sibling host", "issue_type": "epic"},
                {"id": "bazaar-db8", "title": "Dossier becomes a Project", "issue_type": "epic"},
            ]
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(["--fixture", str(path)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = proc.stdout
        expect("# Intentions" in out, out)
        expect("`bazaar-tvm`" in out, out)
        expect("`bazaar-db8`" in out, out)
        expect("## DAG" not in out, out)
        expect("No current intention" in out, out)


def test_pin_current_and_reuse() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        fixture = {
            "epic": {"id": "bazaar-tvm", "title": "Tatastu", "status": "open"},
            "children": [
                {
                    "id": "bazaar-tvm.2",
                    "title": "add-tatastu-host: kernel ADR",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["--fixture", str(path), "--store", str(store), "--current", "bazaar-tvm"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("Current: `bazaar-tvm`" in proc.stdout, proc.stdout)
        expect("### bazaar-tvm.2" in proc.stdout, proc.stdout)
        pin = json.loads((store / "current.json").read_text(encoding="utf-8"))
        expect(pin["roots"] == ["bazaar-tvm"], pin)

        index = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu", "issue_type": "epic"},
                {"id": "bazaar-db8", "title": "Dossier", "issue_type": "epic"},
            ]
        }
        idx_path = root / "idx.json"
        idx_path.write_text(json.dumps(index), encoding="utf-8")
        listed = run(
            ["--fixture", str(idx_path), "--store", str(store)],
            cwd=root,
        )
        expect(listed.returncode == 0, listed.stderr + listed.stdout)
        expect("Current: `bazaar-tvm`" in listed.stdout, listed.stdout)
        expect("`bazaar-tvm` *" in listed.stdout, listed.stdout)


def test_peek_does_not_change_pin() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        store.mkdir()
        (store / "current.json").write_text(
            json.dumps({"roots": ["bazaar-tvm"]}),
            encoding="utf-8",
        )
        fixture = {
            "epic": {"id": "bazaar-db8", "title": "Dossier", "status": "open"},
            "children": [],
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["bazaar-db8", "--fixture", str(path), "--store", str(store)],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect("Current: `bazaar-tvm`" in proc.stdout, proc.stdout)
        expect("Peek: `bazaar-db8`" in proc.stdout, proc.stdout)
        pin = json.loads((store / "current.json").read_text(encoding="utf-8"))
        expect(pin["roots"] == ["bazaar-tvm"], pin)


def test_clear_current() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        store = root / "sess"
        store.mkdir()
        (store / "current.json").write_text(
            json.dumps({"roots": ["bazaar-tvm"]}),
            encoding="utf-8",
        )
        fixture = {
            "epics": [
                {"id": "bazaar-tvm", "title": "Tatastu", "issue_type": "epic"},
            ]
        }
        path = root / "fix.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        proc = run(
            ["--fixture", str(path), "--store", str(store), "--current", "-"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        expect(not (store / "current.json").is_file(), "pin still on disk")
        expect("No current intention" in proc.stdout, proc.stdout)


def test_current_needs_session() -> None:
    with tempfile.TemporaryDirectory() as td:
        env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
        proc = run(["--current", "bazaar-tvm"], cwd=Path(td), env=env)
        expect(proc.returncode == 2, proc.stderr + proc.stdout)
        expect("no session id" in proc.stderr, proc.stderr)


def test_ready_set_inbound_edges() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {"id": "dag-1", "title": "edge dag", "status": "open"},
            "children": [
                {
                    "id": "n-root",
                    "title": "add-root-node: start here",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                },
                {
                    "id": "n-closed",
                    "title": "closed sibling",
                    "status": "closed",
                    "issue_type": "task",
                    "dependencies": [],
                },
                {
                    "id": "n-wait-a",
                    "title": "add-wait-a: blocked on root",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [blocks("n-wait-a", "n-root")],
                },
                {
                    "id": "n-wait-b",
                    "title": "add-wait-b: blocked on root",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [blocks("n-wait-b", "n-root")],
                },
                {
                    "id": "n-miss",
                    "title": "add-wait-x: cross-epic missing",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [blocks("n-miss", "other-epic.9")],
                },
            ],
        }
        out = map_fixture(root, fixture)
        ready = ids_in(section_after(out, "Ready-set"))
        waiting = ids_in(section_after(out, "Waiting"))
        nxt = section_after(out, "Next")
        expect(ready == ["n-root"], ready)
        expect(waiting == ["n-wait-a", "n-wait-b", "n-miss"], waiting)
        expect("other-epic.9" in section_after(out, "Waiting"), out)
        expect("waiting on n-root" in out, out)
        expect("- `change`: n-root" in nxt, nxt)
        expect("`act`" not in nxt, nxt)
        expect("n-wait-a" not in nxt, nxt)
        expect("n-wait-b" not in nxt, nxt)
        expect("n-miss" not in nxt, nxt)


def test_closed_dep_is_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {"id": "dag-2", "title": "closed dep", "status": "open"},
            "children": [
                {
                    "id": "n-done",
                    "title": "already landed",
                    "status": "closed",
                    "issue_type": "task",
                    "dependencies": [],
                },
                {
                    "id": "n-next",
                    "title": "add-next-node: unblocked",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [blocks("n-next", "n-done")],
                },
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == ["n-next"], out)
        expect(ids_in(section_after(out, "Waiting")) == [], out)


def test_outside_closed_dep_is_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {"id": "dag-3", "title": "outside closed", "status": "open"},
            "children": [
                {
                    "id": "n-here",
                    "title": "add-here-node: cross-epic closed",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [blocks("n-here", "other-epic.9")],
                }
            ],
            "outside": [
                {"id": "other-epic.9", "status": "closed", "title": "landed elsewhere"}
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == ["n-here"], out)
        expect(ids_in(section_after(out, "Waiting")) == [], out)


def test_in_progress_not_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = {
            "epic": {"id": "dag-4", "title": "inflight", "status": "open"},
            "children": [
                {
                    "id": "n-fly",
                    "title": "add-fly-node: being written",
                    "status": "in_progress",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == [], out)
        expect(ids_in(section_after(out, "Waiting")) == [], out)
        expect("`act`" not in section_after(out, "Next"), out)


def test_pending_unblocked_needs_activation() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-pend-it", "PENDING")
        fixture = {
            "epic": {"id": "dag-5", "title": "pending", "status": "open"},
            "children": [
                {
                    "id": "n-pend",
                    "title": "add-pend-it: draft",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == [], out)
        expect("n-pend" in section_after(out, "Needs activation"), out)
        nxt = section_after(out, "Next")
        expect("`change` / activate: n-pend" in nxt, nxt)
        expect("`act`" not in nxt, nxt)
        brief = section_after(out, "Decision briefing")
        expect("n-pend" in brief, brief)
        expect("PENDING" in brief, brief)
        expect("`steer` first" in nxt, nxt)


def test_active_build_is_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-live-act", "ACTIVE BUILD")
        fixture = {
            "epic": {"id": "dag-6", "title": "activated", "status": "open"},
            "children": [
                {
                    "id": "n-live",
                    "title": "add-live-act: go",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == ["n-live"], out)
        nxt = section_after(out, "Next")
        expect("`act` or `/run --until roll`: n-live" in nxt, nxt)
        expect("`change`: n-live" not in nxt, nxt)


def test_send_back_next_is_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-sent-back", "ACTIVE BUILD", advise="send-back")
        fixture = {
            "epic": {"id": "dag-7", "title": "sent back", "status": "open"},
            "children": [
                {
                    "id": "n-back",
                    "title": "add-sent-back: revise",
                    "status": "open",
                    "issue_type": "task",
                    "dependencies": [],
                }
            ],
        }
        out = map_fixture(root, fixture)
        expect(ids_in(section_after(out, "Ready-set")) == [], out)
        expect("n-back" in section_after(out, "Failed / send-back"), out)
        nxt = section_after(out, "Next")
        expect("`change` (send-back): n-back" in nxt, nxt)
        expect("`act`" not in nxt, nxt)


def main() -> int:
    tests = [
        test_fixture_epic,
        test_unresolved_scope,
        test_index_not_a_dump,
        test_pin_current_and_reuse,
        test_peek_does_not_change_pin,
        test_clear_current,
        test_current_needs_session,
        test_ready_set_inbound_edges,
        test_closed_dep_is_ready,
        test_outside_closed_dep_is_ready,
        test_in_progress_not_ready,
        test_pending_unblocked_needs_activation,
        test_active_build_is_act,
        test_send_back_next_is_change,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"pass {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    if failed:
        print(f"FAIL {failed}/{len(tests)}")
        return 1
    print(f"pass {len(tests)} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
