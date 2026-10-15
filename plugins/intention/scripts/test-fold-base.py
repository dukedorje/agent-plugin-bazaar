#!/usr/bin/env python3
"""Focused verify: fold base blobs. A stale paste refuses. A missing one does not."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLD_BASE = HERE.parents[0] / "skills" / "fold" / "scripts" / "fold_base.py"
RUN = HERE.parents[0] / "skills" / "run" / "scripts" / "run.py"


def load():
    spec = importlib.util.spec_from_file_location("fold_base", FOLD_BASE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout.strip()


def init_repo(root: Path, living: str) -> None:
    git(root, "init")
    git(root, "config", "user.email", "fold-base@example.com")
    git(root, "config", "user.name", "fold-base")
    spec = root / "openspec" / "specs" / "verbs" / "spec.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(living, encoding="utf-8")


LIVING = """# verbs

### Requirement: One
The system SHALL keep the first clause.

#### Scenario: First
- GIVEN one
- WHEN read
- THEN the first clause is there

### Requirement: Two
The system SHALL keep the second clause.
"""

DELTA = """## MODIFIED Requirements

### Requirement: One
The system SHALL keep the first clause.
The system SHALL add a second sentence.

#### Scenario: First
- GIVEN one
- WHEN read
- THEN the first clause is there

#### Scenario: Added
- GIVEN the edit
- WHEN folded
- THEN both sentences are there
"""


def write_delta(root: Path, text: str) -> Path:
    change = root / "openspec" / "changes" / "update-sample"
    spec = change / "specs" / "verbs" / "spec.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(text, encoding="utf-8")
    proposal = change / "proposal.md"
    proposal.write_text("# update-sample\n\n> **ACTIVE BUILD**\n", encoding="utf-8")
    (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
    return change


def test_stamp_then_match_is_not_stale() -> None:
    module = load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        init_repo(root, LIVING)
        change = write_delta(root, DELTA)
        stamped = module.stamp(change)
        expect(stamped["stamped"] == ["verbs:One"], stamped)
        report = module.classify(change)
        expect(report["stale"] == [], report)
        expect(report["unstamped"] == [], report)
        text = (change / "specs" / "verbs" / "spec.md").read_text(encoding="utf-8")
        expect("<!-- base: " in text, text)
        expect("openspec/specs/verbs/spec.md" in text, text)


def test_living_edit_is_stale() -> None:
    module = load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        init_repo(root, LIVING)
        change = write_delta(root, DELTA)
        module.stamp(change)
        spec = root / "openspec" / "specs" / "verbs" / "spec.md"
        spec.write_text(LIVING.replace("first clause", "first clause plus upstream"), encoding="utf-8")
        report = module.classify(change)
        expect(len(report["stale"]) == 1, report)
        expect(report["stale"][0]["why"] == "living-requirement-changed", report)
        expect(report["stale"][0]["requirement"] == "One", report)


def test_unstamped_does_not_refuse() -> None:
    module = load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        init_repo(root, LIVING)
        change = write_delta(root, DELTA)
        report = module.classify(change)
        expect(report["stale"] == [], report)
        expect(report["unstamped"][0]["requirement"] == "One", report)


def test_removed_already_gone_is_not_stale() -> None:
    module = load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        init_repo(root, LIVING)
        change = write_delta(
            root,
            "## REMOVED Requirements\n\n### Requirement: Two\n",
        )
        module.stamp(change)
        spec = root / "openspec" / "specs" / "verbs" / "spec.md"
        spec.write_text(LIVING.split("### Requirement: Two")[0], encoding="utf-8")
        report = module.classify(change)
        expect(report["stale"] == [], report)


def test_run_routes_stale_to_change_and_keeps_a_clean_fold() -> None:
    module = load()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        init_repo(root, LIVING)
        stale = write_delta(root, DELTA)
        module.stamp(stale)
        (root / "openspec" / "specs" / "verbs" / "spec.md").write_text(
            LIVING.replace("first clause", "first clause plus upstream"),
            encoding="utf-8",
        )
        clean = root / "openspec" / "changes" / "add-clean"
        clean.mkdir(parents=True)
        (clean / "proposal.md").write_text(
            "# add-clean\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (clean / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = root / "ready.json"
        fixture.write_text(json.dumps({
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
            "eyes": [],
            "fold_legal": ["update-sample", "add-clean"],
            "send_back": [],
            "beads": [],
        }), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(RUN), "--ready-json", str(fixture), "--json"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "fold" and face["focus"] == "add-clean", face)
        fixture.write_text(json.dumps({
            "ready": [],
            "waiting": [],
            "needs_advise": [],
            "ask": [],
            "eyes": [],
            "fold_legal": ["update-sample"],
            "send_back": [],
            "beads": [],
        }), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(RUN), "--ready-json", str(fixture), "--json"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["reason"] == "stale-base", face)
        expect(face["focus"] == "update-sample", face)
        expect(face["stop"] is None, face)


def main() -> int:
    tests = [
        test_stamp_then_match_is_not_stale,
        test_living_edit_is_stale,
        test_unstamped_does_not_refuse,
        test_removed_already_gone_is_not_stale,
        test_run_routes_stale_to_change_and_keeps_a_clean_fold,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
