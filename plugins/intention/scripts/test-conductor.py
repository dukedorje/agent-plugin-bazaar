#!/usr/bin/env python3
"""Focused verify for conductor.py. No live beads required."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONDUCTOR = HERE / "conductor.py"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CONDUCTOR), *args],
        cwd=cwd,
        text=True,
        capture_output=True,
    )


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_ready() -> None:
    inv = {
        "nodes": [
            {"id": "a", "status": "in_progress", "deps": [], "paths": ["src/a.py"]},
            {"id": "b", "status": "open", "deps": [], "paths": ["src/a.py", "src/a.py.bak"]},
            {"id": "c", "status": "open", "deps": [], "paths": ["docs/x.md"]},
            {"id": "d", "status": "open", "deps": ["missing"], "paths": ["docs/y.md"]},
            {"id": "e", "status": "closed", "deps": [], "paths": []},
            {"id": "f", "status": "open", "deps": ["e"], "paths": []},
            {"id": "g", "status": "parked", "deps": [], "paths": ["docs/z.md"]},
        ]
    }
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "inv.json"
        path.write_text(json.dumps(inv), encoding="utf-8")
        proc = run(["ready", "--inventory", str(path), "--max-inflight", "8"])
        expect(proc.returncode == 0, proc.stderr)
        data = json.loads(proc.stdout)
        disp = {row["id"] for row in data["dispatchable"]}
        deferred = {row["id"] for row in data["deferred"]}
        blocked = {row["id"] for row in data["blocked"]}
        expect(disp == {"c", "f"}, f"dispatchable={disp} stdout={proc.stdout}")
        expect(deferred == {"b"}, f"deferred={deferred}")
        expect(blocked == {"d"}, f"blocked={blocked}")
        expect({row["id"] for row in data["in_flight"]} == {"a"}, data)
        expect({row["id"] for row in data["parked"]} == {"g"}, data)


def test_implicated() -> None:
    inv = {
        "nodes": [
            {"id": "root", "status": "open", "deps": [], "paths": ["a"]},
            {"id": "child", "status": "open", "deps": ["root"], "paths": ["b"]},
            {"id": "other", "status": "open", "deps": [], "paths": ["c"]},
            {"id": "done", "status": "closed", "deps": ["root"], "paths": ["d"]},
        ]
    }
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "inv.json"
        path.write_text(json.dumps(inv), encoding="utf-8")
        proc = run(["implicated", "--node", "root", "--inventory", str(path)])
        expect(proc.returncode == 0, proc.stderr)
        got = set(json.loads(proc.stdout)["implicated"])
        expect(got == {"root", "child"}, got)


def test_lint() -> None:
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.json"
        bad.write_text(
            json.dumps(
                {
                    "goal": "edit",
                    "constraints": {"permission": "write", "paths": ["x"], "do_not": ["commit"]},
                }
            ),
            encoding="utf-8",
        )
        proc = run(["lint-packet", str(bad)])
        expect(proc.returncode != 0, "lint should reject do_not commit")
        prose = Path(td) / "prose.json"
        prose.write_text(
            json.dumps(
                {
                    "goal": "run NO git, the conductor commits",
                    "constraints": {"permission": "write", "paths": ["x"], "do_not": ["push"]},
                }
            ),
            encoding="utf-8",
        )
        proc = run(["lint-packet", str(prose)])
        expect(proc.returncode != 0, "lint should reject exemption prose")
        good = Path(td) / "good.json"
        good.write_text(
            json.dumps(
                {
                    "goal": "implement the node",
                    "constraints": {"permission": "write", "paths": ["x"], "do_not": ["push", "deploy"]},
                }
            ),
            encoding="utf-8",
        )
        proc = run(["lint-packet", str(good)])
        expect(proc.returncode == 0, proc.stdout + proc.stderr)


def test_classify() -> None:
    cases = {
        "pass": "close",
        "baseline-red": "complete",
        "task-red": "repair",
        "infra-red": "retry",
        "blocked": "park",
        "parked": "park",
    }
    with tempfile.TemporaryDirectory() as td:
        for disp, action in cases.items():
            path = Path(td) / f"{disp}.json"
            path.write_text(json.dumps({"disposition": disp, "summary": "x"}), encoding="utf-8")
            proc = run(["classify", str(path)])
            expect(proc.returncode == 0, proc.stderr)
            got = json.loads(proc.stdout)["action"]
            expect(got == action, f"{disp} -> {got} want {action}")


def git(repo: Path, extra: list[str]) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *extra], text=True)


def test_cap_and_take() -> None:
    inv = {
        "nodes": [
            {"id": "hold", "status": "in_progress", "deps": [], "paths": ["src/hold.py"], "holder": "a"},
            {"id": "x", "status": "open", "deps": [], "paths": ["docs/x.md"]},
            {"id": "y", "status": "open", "deps": [], "paths": ["docs/y.md"]},
        ]
    }
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        path = root / "inv.json"
        path.write_text(json.dumps(inv), encoding="utf-8")
        capped = run(
            ["--repo", str(root), "ready", "--inventory", str(path), "--max-inflight", "1"]
        )
        expect(capped.returncode == 0, capped.stderr)
        data = json.loads(capped.stdout)
        expect(data["dispatchable"] == [], data)
        expect({r["id"] for r in data["capped"]} == {"x", "y"}, data)
        expect(data["slots"]["free"] == 0, data)

        room = run(
            ["--repo", str(root), "ready", "--inventory", str(path), "--max-inflight", "3"]
        )
        expect({r["id"] for r in json.loads(room.stdout)["dispatchable"]} == {"x", "y"}, room.stdout)

        first = run(
            [
                "--repo",
                str(root),
                "take",
                "--node",
                "x",
                "--holder",
                "sonnet-5",
                "--inventory",
                str(path),
                "--max-inflight",
                "3",
            ]
        )
        expect(first.returncode == 0, first.stderr)
        taken = json.loads(first.stdout)
        expect(taken["taken"] == "x", taken)
        expect(Path(taken["lease"]).is_file(), taken)
        again = run(
            [
                "--repo",
                str(root),
                "take",
                "--node",
                "x",
                "--holder",
                "opus-5",
                "--inventory",
                str(path),
                "--max-inflight",
                "3",
            ]
        )
        expect(again.returncode != 0, "second take should fail")
        expect("already taken" in again.stderr, again.stderr)
        rel = run(["--repo", str(root), "release", "--node", "x", "--inventory", str(path)])
        expect(rel.returncode == 0, rel.stderr)
        after = json.loads(path.read_text(encoding="utf-8"))
        node = next(n for n in after["nodes"] if n["id"] == "x")
        expect(node["status"] == "open", node)


def test_isolate_persist() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "repo"
        repo.mkdir()
        subprocess.check_call(["git", "init", "-q", str(repo)])
        git(repo, ["config", "user.email", "conductor@test"])
        git(repo, ["config", "user.name", "Conductor"])
        (repo / "keep.txt").write_text("keep\n", encoding="utf-8")
        git(repo, ["add", "--", "keep.txt"])
        git(repo, ["commit", "-q", "-m", "init"])

        iso = run(["--repo", str(repo), "isolate", "--node", "nod-demo"])
        expect(iso.returncode == 0, iso.stderr)
        info = json.loads(iso.stdout)
        tree = Path(info["worktree"])
        expect(tree.is_dir(), f"missing worktree {tree}")
        (tree / "keep.txt").write_text("keep\nchanged\n", encoding="utf-8")
        (tree / "noise.txt").write_text("not this\n", encoding="utf-8")

        persist = run(
            [
                "--repo",
                str(repo),
                "persist",
                "--worktree",
                str(tree),
                "--paths",
                "keep.txt",
                "-m",
                "chore: conductor persist",
            ]
        )
        expect(persist.returncode == 0, persist.stderr + persist.stdout)
        body = json.loads(persist.stdout)
        expect(body["paths"] == ["keep.txt"], body)
        stat = git(tree, ["show", "--stat", "--oneline", "HEAD"])
        expect("keep.txt" in stat, stat)
        expect("noise.txt" not in stat, stat)

        reuse = run(["--repo", str(repo), "isolate", "--node", "nod-demo"])
        expect(json.loads(reuse.stdout)["reused"] is True, reuse.stdout)


def main() -> int:
    tests = [
        test_ready,
        test_implicated,
        test_lint,
        test_classify,
        test_cap_and_take,
        test_isolate_persist,
    ]
    failed = 0
    for fn in tests:
        try:
            fn()
            print(f"pass {fn.__name__}")
        except Exception as exc:  # noqa: BLE001 — report each focused case
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    if failed:
        print(f"FAIL {failed}/{len(tests)}")
        return 1
    print(f"pass {len(tests)} tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
