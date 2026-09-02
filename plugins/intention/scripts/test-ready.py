#!/usr/bin/env python3
"""Focused verify: ready.py unions OpenSpec and beads. No worker launched."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
READY = HERE.parents[0] / "skills" / "ready" / "scripts" / "ready.py"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(READY), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def write_beads(td: Path, payload: list[dict]) -> Path:
    path = td / "beads.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def write_change(root: Path, name: str, *, banner: str = "ACTIVE BUILD", tasks: str) -> None:
    change = root / "openspec" / "changes" / name
    change.mkdir(parents=True)
    (change / "proposal.md").write_text(
        f"# {name}\n\n> **{banner}**\n",
        encoding="utf-8",
    )
    (change / "tasks.md").write_text(f"# Tasks\n\n{tasks}\n", encoding="utf-8")


def test_openspec_ready_stays_openspec() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-x", tasks="- [ ] implement the thing")
        beads = write_beads(
            root,
            [{"id": "bazaar-ja7", "title": "Information ingestion", "issue_type": "task"}],
        )
        proc = run(
            [
                "--json",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        ids = [row["id"] for row in face["ready"]]
        expect(ids == ["add-x"], face)
        expect("bazaar-ja7" not in ids, face)
        expect(face["beads"][0]["id"] == "bazaar-ja7", face)


def test_empty_openspec_still_shows_beads() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "openspec" / "changes").mkdir(parents=True)
        beads = write_beads(
            root,
            [
                {
                    "id": "bazaar-tvm.2",
                    "title": "add-tatastu-host: kernel ADR names the host",
                    "issue_type": "decision",
                }
            ],
        )
        proc = run(
            [
                "--json",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["ready"] == [], face)
        expect(face["beads"][0]["id"] == "bazaar-tvm.2", face)
        text = run(
            ["--root", str(root / "openspec"), "--beads-json", str(beads)],
            cwd=root,
        )
        expect(text.returncode == 0, text.stderr + text.stdout)
        expect("BEADS" in text.stdout, text.stdout)
        expect("bazaar-tvm.2" in text.stdout, text.stdout)
        expect("READY (OpenSpec" in text.stdout, text.stdout)
        expect("(none)" in text.stdout, text.stdout)


def test_missing_openspec_still_shows_beads() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        beads = write_beads(
            root,
            [{"id": "bazaar-ja7", "title": "G Brain", "issue_type": "task"}],
        )
        proc = run(["--json", "--beads-json", str(beads)], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face.get("missing") == "openspec", face)
        expect(face["ready"] == [], face)
        expect(face["beads"][0]["id"] == "bazaar-ja7", face)
        text = run(["--beads-json", str(beads)], cwd=root)
        expect(text.returncode == 0, text.stderr + text.stdout)
        expect("bazaar-ja7" in text.stdout, text.stdout)
        expect("beads still shown" in text.stdout, text.stdout)


def test_parked_hides_beads() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "openspec" / "changes").mkdir(parents=True)
        beads = write_beads(
            root,
            [{"id": "bazaar-ja7", "title": "G Brain", "issue_type": "task"}],
        )
        proc = run(
            [
                "--json",
                "--parked",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect("beads" not in face, face)
        expect("ready" not in face, face)
        expect(face["parked"] == [], face)


def test_ready_flag_includes_beads() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "openspec" / "changes").mkdir(parents=True)
        beads = write_beads(
            root,
            [{"id": "bazaar-ja7", "title": "G Brain", "issue_type": "task"}],
        )
        proc = run(
            [
                "--json",
                "--ready",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["beads"][0]["id"] == "bazaar-ja7", face)
        expect("parked" not in face, face)


def test_eyes_is_not_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-x", tasks="- [ ] EYES: look at the dashboard")
        write_change(root, "add-y", tasks="- [ ] implement the thing")
        beads = write_beads(root, [])
        proc = run(
            [
                "--json",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect([row["id"] for row in face["ready"]] == ["add-y"], face)
        expect([row["id"] for row in face["eyes"]] == ["add-x"], face)
        expect(face["ask"] == [], face)
        text = run(
            ["--root", str(root / "openspec"), "--beads-json", str(beads)],
            cwd=root,
        )
        expect("EYES" in text.stdout, text.stdout)
        expect("ASK" in text.stdout, text.stdout)


def test_ask_and_punt_faces() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-x", tasks="- [ ] ASK: which store")
        write_change(root, "add-y", tasks="- [ ] PUNT: second-family advise")
        beads = write_beads(root, [])
        proc = run(
            [
                "--json",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["ready"] == [], face)
        expect([row["id"] for row in face["ask"]] == ["add-x"], face)
        expect([row["id"] for row in face["punt"]] == ["add-y"], face)


def test_pending_does_not_flip_into_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-x", banner="PENDING", tasks="- [ ] later")
        beads = write_beads(root, [])
        proc = run(
            [
                "--json",
                "--root",
                str(root / "openspec"),
                "--beads-json",
                str(beads),
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["ready"] == [], face)
        expect([row["id"] for row in face["waiting"]] == ["add-x"], face)


def main() -> int:
    tests = [
        test_openspec_ready_stays_openspec,
        test_empty_openspec_still_shows_beads,
        test_missing_openspec_still_shows_beads,
        test_parked_hides_beads,
        test_ready_flag_includes_beads,
        test_eyes_is_not_ready,
        test_ask_and_punt_faces,
        test_pending_does_not_flip_into_ready,
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
