#!/usr/bin/env python3
"""Focused verify: run.py card + stage dispatch. No worker launched."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parents[0] / "skills" / "run" / "scripts" / "run.py"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    if cwd is None and "--ready-json" in args:
        cwd = Path(args[args.index("--ready-json") + 1]).parent
    return subprocess.run(
        [sys.executable, str(RUN), *args],
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def write_ready(td: Path, payload: dict) -> Path:
    fixture = td / "ready.json"
    fixture.write_text(json.dumps(payload), encoding="utf-8")
    return fixture


def test_empty_ready_no_worker() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "eyes": [],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
        expect(face["until"] == "roll", face)
        expect(face["workers_launched"] == 0, face)
        expect(face["next"] is None, face)
        text = run(["--ready-json", str(fixture)])
        expect(text.returncode == 0, text.stderr)
        expect("RUN" in text.stdout, text.stdout)
        expect("workers 0" in text.stdout, text.stdout)


def test_missing_ready_py_is_no_ready() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "missing": "ready.py",
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "no-ready", face)
        expect(face["workers_launched"] == 0, face)
        expect(face["next"] is None, face)


def test_missing_openspec_no_scope_is_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(
            [sys.executable, str(RUN), "--json"],
            text=True,
            capture_output=True,
            cwd=td,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
        expect(face["next"] is None, face)
        expect(face.get("missing") is None or face.get("missing") != "ready.py", face)


def test_scope_missing_dir_is_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-sheaf-type", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] is None, face)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-sheaf-type", face)
        expect(face["workers_launched"] == 0, face)


def test_advise_before_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [{"id": "add-x"}],
                "ask": [],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-x", face)
        expect(face["stop"] is None, face)


def test_until_advise_runs_read() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [{"id": "add-x"}],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--until", "advise", "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["stop"] is None, face)
        expect(face["workers_launched"] == 0, face)


def test_until_advise_does_not_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--until", "advise", "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_ready_is_act() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["next"] == "act", face)
        expect(face["focus"] == "add-x", face)


def test_goal_scope_is_intend() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            [
                "we need extract-from on intend",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "intend", face)
        expect(face["stop"] is None, face)
        expect(face["workers_launched"] == 0, face)


def test_until_fold_when_legal() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-x", "--until", "fold", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "fold", face)
        expect(face["focus"] == "add-x", face)
        expect(face["workers_launched"] == 0, face)


def test_empty_does_not_fold_when_legal() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["add-x", "--until", "empty", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_default_until_is_roll() -> None:
    """Bare run (no --until) uses the roll table: unscoped fold-legal → fold."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["until"] == "roll", face)
        expect(face["next"] == "fold", face)
        expect(face["focus"] == "add-x", face)


def test_unscoped_fold_scans() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["--until", "fold", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "fold", face)
        expect(face["focus"] == "add-x", face)
        expect(face["workers_launched"] == 0, face)


def test_roll_send_back_is_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "send_back": ["add-x"],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-x", face)


def test_roll_bead_landing_is_change() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-tvm.2",
                        "title": "add-tatastu-host: kernel ADR names the host",
                        "issue_type": "decision",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-tatastu-host", face)


def test_ask_stops_when_pending() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [{"id": "add-y"}],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "ask", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "ask", face)
        expect(face["next"] is None, face)
        expect(face["focus"] == "add-y", face)


def test_ask_without_elicitation_rolls() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-tvm.2",
                        "title": "add-tatastu-host: kernel ADR names the host",
                        "issue_type": "decision",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "ask", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-tatastu-host", face)


def test_roll_does_not_stop_on_pending() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [{"id": "add-y"}],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "act", face)
        expect(face["focus"] == "add-x", face)
        expect("add-y" in face["ask"], face)


def test_roll_skips_epic() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-tvm",
                        "title": "Make Tatastu a sibling host",
                        "issue_type": "epic",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_roll_intend_orphan_task() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-ja7",
                        "title": "Information ingestion: G Brain",
                        "issue_type": "task",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "intend", face)
        expect(face["focus"] == "bazaar-ja7", face)


def test_roll_skips_node_type() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-7kb.1",
                        "title": "fileset organizer: exclusive owned, shared deferred",
                        "issue_type": "node",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_roll_skips_legacy_nod_title() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-7kb.2",
                        "title": "nod-empty-paths: [] overlaps everything",
                        "issue_type": "task",
                    }
                ],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def write_change(
    root: Path,
    name: str,
    *,
    banner: str = "ACTIVE BUILD",
    tasks: str = "- [x] done",
    rigor: str | None = None,
    review: str | None = None,
) -> Path:
    change = root / "openspec" / "changes" / name
    change.mkdir(parents=True)
    body = f"# {name}\n\n> **{banner}**\n"
    if rigor:
        body += f"\n**Rigor:** {rigor}\n"
    (change / "proposal.md").write_text(body, encoding="utf-8")
    (change / "tasks.md").write_text(f"# Tasks\n\n{tasks}\n", encoding="utf-8")
    if review:
        reviews = change / "reviews"
        reviews.mkdir()
        (reviews / "2026-08-27-advise.md").write_text(
            f"> **ADVISE:** {review}\n",
            encoding="utf-8",
        )
    return change


def test_pending_scope_does_not_flip() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [{"id": "add-x"}],
                "needs_advise": [],
                "ask": [],
            },
        )
        proc = run(["add-x", "--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "activation", face)
        expect(face["next"] is None, face)
        expect(face["focus"] == "add-x", face)


def test_roll_needs_advise_is_not_fold() -> None:
    """ACTIVE BUILD, no open boxes, in needs_advise → not fold; roll → advise."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-agent-body", rigor="architecture")
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-agent-body"}],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-agent-body", face)
        expect(face["stop"] is None, face)
        expect("add-agent-body" in face["needs_advise"], face)


def test_roll_skip_fold_picks_advise() -> None:
    """--skip the fold-legal id; roll walks to needs_advise."""
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-y"}],
                "ask": [],
                "fold_legal": ["add-x"],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(
            [
                "--until",
                "roll",
                "--skip",
                "add-x",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-y", face)
        expect("add-x" not in face["ask"], face)
        expect("add-y" in face["needs_advise"], face)


def test_roll_skip_fold_still_advises_same_id() -> None:
    """Fold refusal --skip does not drop advise on that same id."""
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-agent-body"}],
                "ask": [],
                "fold_legal": ["add-agent-body"],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(
            [
                "--until",
                "roll",
                "--skip",
                "add-agent-body",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-agent-body", face)
        expect(face["stop"] is None, face)


def test_wait_alias_interrupt() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [{"id": "add-y"}],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--interrupt", "--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "ask", face)
        expect(face["until"] == "ask", face)


def test_interrupt_stops_when_pending() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [{"id": "add-y"}],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--wait", "--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "ask", face)
        expect(face["next"] is None, face)
        expect(face["until"] == "ask", face)


def test_only_fold() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            ["--tidy", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["until"] == "fold", face)
        expect(face["next"] == "fold", face)
        expect(face["focus"] == "add-x", face)


def test_no_fold_no_beads_is_empty_walk() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = root / "openspec" / "changes" / "add-x"
        change.mkdir(parents=True)
        (change / "proposal.md").write_text(
            "# add-x\n\n> **ACTIVE BUILD**\n", encoding="utf-8"
        )
        (change / "tasks.md").write_text("# Tasks\n\n- [x] done\n", encoding="utf-8")
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(
            [
                "add-x",
                "--no-fold",
                "--no-beads",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["until"] == "empty", face)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


def test_run_skill_spawns_other_family_advise() -> None:
    """Conductor prompt: same-family advise is spawn, not punt-first halt."""
    skill = HERE.parents[0] / "skills" / "run" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    expect("spawn that reader" in text or "spawn an other-family" in text, text[:800])
    expect("spawn that reader always" in text, text)
    expect("reader writes reviews" in text, text)
    expect("Punt is last-resort only" in text or "punt only" in text.lower(), text)
    expect("Same-family advise is **not** illegal" in text, text)
    expect("stop when stuck" not in text, "stuck halt still in skill")
    expect(
        "if card.next is advise and cannot promote" not in text,
        "punt-first loop still in skill",
    )


def test_roll_punt_skips_advise() -> None:
    """Last-resort punt parks the id; roll advises a different node."""
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-sheaf-type"}, {"id": "add-y"}],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(
            [
                "--until",
                "roll",
                "--punt",
                "add-sheaf-type",
                "--ready-json",
                str(fixture),
                "--json",
            ],
            cwd=Path(td),
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-y", face)
        expect("add-sheaf-type" in face["ask"], face)
        expect("add-sheaf-type" in face["needs_advise"], face)


def test_roll_send_back_no_boxes_is_not_change() -> None:
    """Last advise send-back, no open boxes → not change; stays needs_advise."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            review="send-back",
        )
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] != "change", face)
        expect(face["next"] != "fold", face)
        expect("add-sheaf-type" in face["needs_advise"], face)
        expect(face["next"] == "advise", face)
        expect(face["focus"] == "add-sheaf-type", face)


def test_wait_eyes_is_stop_eyes() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "eyes": [
                    {
                        "id": "add-x",
                        "open": [
                            "EYES: one real two-node wave. Next: /run-wave"
                        ],
                    }
                ],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--wait", "--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "eyes", face)
        expect(face["next"] is None, face)
        expect(face["focus"] == "add-x", face)
        expect(face["next_steps"][0]["command"] == "/run-wave", face)
        text = run(["--wait", "--ready-json", str(fixture)])
        expect("YOUR EYES" in text.stdout, text.stdout)
        expect("/run-wave" in text.stdout, text.stdout)
        expect("Next:" in text.stdout, text.stdout)


def test_roll_eyes_does_not_intend_leftover() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "eyes": [
                    {
                        "id": "add-run-wave-workflow",
                        "open": ["EYES: look. Next: /run-wave"],
                    }
                ],
                "fold_legal": [],
                "send_back": [],
                "beads": [
                    {
                        "id": "bazaar-ja7",
                        "title": "Information ingestion: G Brain",
                        "issue_type": "task",
                    }
                ],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "eyes", face)
        expect(face["next"] is None, face)
        expect(face["until"] == "roll", face)


def test_roll_unrelated_ready_moves_with_eyes_listed() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-y"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "eyes": [{"id": "add-x", "open": ["EYES: look. Next: /status"]}],
                "fold_legal": [],
                "beads": [],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] is None, face)
        expect(face["next"] == "act", face)
        expect(face["focus"] == "add-y", face)
        expect("add-x" in face["eyes"], face)


def test_roll_send_back_with_boxes_is_change() -> None:
    """Last advise send-back with open boxes → change."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks="- [ ] amend the SHALL on compile",
            review="send-back",
        )
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-sheaf-type"}],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(
            ["--until", "roll", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["focus"] == "add-sheaf-type", face)
        expect("add-sheaf-type" in face["needs_advise"], face)


def test_preparation_obligation_tracks_act_candidates() -> None:
    """A wave prepares every eligible node; scoped execution prepares its pick."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-y", tasks="- [ ] implement")
        fixture = write_ready(root, {
            "ready": ["add-x", "add-y", "add-z", "add-punted", "add-eyes"],
            "waiting": [], "needs_advise": [], "ask": [],
            "eyes": ["add-eyes"], "fold_legal": [], "send_back": [], "beads": [],
        })
        for scope, until, expected in (
            ([], "roll", ["add-x", "add-y"]),
            ([], "empty", ["add-x", "add-y"]),
            (["add-y"], "roll", ["add-y"]),
        ):
            args = [*scope, "--until", until, "--skip", "add-z", "--punt", "add-punted",
                    "--ready-json", str(fixture)]
            proc = run([*args, "--json"], cwd=root)
            expect(proc.returncode == 0, proc.stderr)
            face = json.loads(proc.stdout)
            expect(face["next"] == "act", face)
            expect(face["prepare_before_act"] == expected, face)
            expect(face["workers_launched"] == 0, face)
            rendered = run(args, cwd=root)
            expect("prepare before act: " + ", ".join(expected) in rendered.stdout,
                   rendered.stdout)


def test_non_act_has_no_preparation_candidates() -> None:
    """Preparation metadata cannot make a stop or another stage actionable."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for extra, args, expected_next in (
            ({"needs_advise": ["add-x"]}, [], "advise"),
            ({"send_back": ["add-x"]}, [], "change"),
            ({"fold_legal": ["add-x"]}, [], "fold"),
            ({"waiting": ["add-y"]}, ["--wait"], None),
            ({"eyes": ["add-x"]}, [], None),
            ({}, ["--until", "advise"], None),
            ({}, ["a new goal"], "intend"),
        ):
            fixture = write_ready(root, {
                "ready": ["add-x"], "waiting": [], "needs_advise": [],
                "ask": [], "eyes": [], "fold_legal": [], "send_back": [],
                "beads": [], **extra,
            })
            proc = run([*args, "--ready-json", str(fixture), "--json"], cwd=root)
            expect(proc.returncode == 0, proc.stderr)
            face = json.loads(proc.stdout)
            expect(face["next"] == expected_next, face)
            expect(face["prepare_before_act"] == [], face)


def kat_bead(nid: str, title: str, status: str = "open", parent: str | None = None) -> dict:
    deps = []
    if parent:
        deps.append({"issue_id": nid, "depends_on_id": parent, "type": "parent-child"})
    return {"id": nid, "title": title, "status": status, "dependencies": deps}


def kat_fixture(root: Path, child_status: str, **extra) -> Path:
    write_change(root, "add-umbrella-net", tasks="Owed work lives in beads (mesh-ai0.*).")
    payload = {
        "ready": [], "waiting": [], "needs_advise": [], "ask": [], "send_back": [],
        "beads": [],
        "graph": [
            kat_bead("mesh-ai0", "add-umbrella-net: household network"),
            kat_bead("mesh-ai0.1", "add-trust-contract: trust", child_status, "mesh-ai0"),
            kat_bead("mesh-ai0.2", "inventory devices", child_status, "mesh-ai0.1"),
            kat_bead("mesh-plain", "plain epic without landing"),
        ],
    }
    payload.update(extra)
    return write_ready(root, payload)


def test_umbrella_with_open_beads_is_not_fold_legal() -> None:
    """bazaar-kat: no markdown boxes is not proof of no owed work."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = kat_fixture(root, "open")
        scoped = json.loads(run(["add-umbrella-net", "--ready-json", str(fixture), "--json"], cwd=root).stdout)
        expect(scoped["next"] != "fold", scoped)
        expect(scoped["stop"] == "owed-beads", scoped)
        expect(scoped["owed"] == ["mesh-ai0.1", "mesh-ai0.2"], scoped)
        unscoped = json.loads(run(["--ready-json", str(fixture), "--json"], cwd=root).stdout)
        expect(unscoped["next"] != "fold", unscoped)


def test_umbrella_with_closed_beads_folds() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = kat_fixture(root, "closed")
        scoped = json.loads(run(["add-umbrella-net", "--ready-json", str(fixture), "--json"], cwd=root).stdout)
        expect(scoped["next"] == "fold", scoped)
        unscoped = json.loads(run(["--ready-json", str(fixture), "--json"], cwd=root).stdout)
        expect(unscoped["next"] == "fold" and unscoped["focus"] == "add-umbrella-net", unscoped)


def test_epic_alias_resolves_to_landing() -> None:
    """bazaar-kat: `run ai0` is the epic, not a goal for a duplicate intend."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = kat_fixture(root, "open")
        for alias in ("ai0", "mesh-ai0"):
            face = json.loads(run([alias, "--ready-json", str(fixture), "--json"], cwd=root).stdout)
            expect(face["next"] != "intend", face)
            expect(face["focus"] == "add-umbrella-net", face)
        plain = json.loads(run(["plain", "--ready-json", str(fixture), "--json"], cwd=root).stdout)
        expect(plain["next"] is None and plain["stop"] == "scope-unresolved", plain)
        expect("mesh-plain" in plain["diagnostic"], plain)


def test_scoped_skip_does_not_widen() -> None:
    """bazaar-kat: --skip on the named scope never picks unrelated work."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = kat_fixture(root, "open", ready=["add-embedded-assert"])
        face = json.loads(run([
            "add-umbrella-net", "--skip", "add-umbrella-net",
            "--ready-json", str(fixture), "--json",
        ], cwd=root).stdout)
        expect(face["focus"] == "add-umbrella-net", face)
        expect(face["next"] is None and face["stop"] == "skipped", face)
        unscoped = json.loads(run([
            "--skip", "add-umbrella-net", "--ready-json", str(fixture), "--json",
        ], cwd=root).stdout)
        expect(unscoped["next"] == "act" and unscoped["focus"] == "add-embedded-assert", unscoped)


def test_stop_names_the_human_unblock() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "eyes": [],
                "fold_legal": [],
                "beads": [],
                "blocked": [
                    {
                        "id": "bazaar-spi.3",
                        "title": "campaign walks demo",
                        "status": "open",
                        "priority": 2,
                        "description": "- Spike: H9 old claim — go",
                        "blocked_by": [
                            {
                                "id": "bazaar-spi.1",
                                "status": "open",
                                "title": "demo verb",
                                "priority": 1,
                            }
                        ],
                    },
                    {
                        "id": "bazaar-ext.1",
                        "title": "waits outside",
                        "status": "open",
                        "priority": 1,
                        "blocked_by": [
                            {
                                "id": "external:tatastu:tat-9",
                                "status": "open",
                                "title": "host packet",
                                "where": "~/work/tatastu",
                            }
                        ],
                    },
                    {
                        "id": "bazaar-spike.1",
                        "title": "lands a recipe",
                        "status": "open",
                        "priority": 2,
                        "description": "- Spike: H3 canvas hash — unverified (low, inferred-from-source)",
                        "blocked_by": [{"id": "bazaar-spi.1", "status": "open"}],
                    },
                ],
                "ready_beads": [
                    {"id": "bazaar-tvm", "priority": 1, "title": "tatastu", "issue_type": "task"},
                    {"id": "bazaar-ja7", "priority": 2, "title": "ingest", "issue_type": "task"},
                ],
            },
        )
        # ja7 unblocks a chain; priority would do tvm first.
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        payload["blocked"].append(
            {
                "id": "bazaar-db8.3",
                "status": "open",
                "priority": 2,
                "blocked_by": [{"id": "bazaar-ja7", "status": "open", "priority": 2}],
            }
        )
        fixture.write_text(json.dumps(payload), encoding="utf-8")
        proc = run(["--ready-json", str(fixture), "--json"], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
        text = "\n".join(face["unblock"])
        expect("bazaar-spi.3" in text and "bazaar-spi.1" in text, text)
        expect("this repo" in text, text)
        expect("tat-9" in text and "tatastu" in text, text)
        expect("open spike" in text and "bazaar-spike.1" in text, text)
        expect("H9" not in text, text)
        expect("Order:" in text and "bazaar-ja7" in text and "bazaar-tvm" in text, text)
        shown = run(["--ready-json", str(fixture)], cwd=root)
        expect("UNBLOCK" in shown.stdout, shown.stdout)
        expect("tatastu at ~/work/tatastu" in shown.stdout, shown.stdout)


def test_continuing_card_has_no_unblock() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "beads": [],
                "blocked": [
                    {
                        "id": "bazaar-spi.3",
                        "blocked_by": [{"id": "bazaar-spi.1", "status": "open"}],
                    }
                ],
            },
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "act", face)
        expect(face["unblock"] == [], face)


def test_ask_stop_says_steer() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [{"id": "add-y"}],
                "needs_advise": [],
                "ask": [],
                "fold_legal": [],
                "send_back": [],
                "beads": [],
            },
        )
        proc = run(["--until", "ask", "--ready-json", str(fixture), "--json"], cwd=Path(td))
        face = json.loads(proc.stdout)
        expect(face["stop"] == "ask", face)
        expect(any("steer" in line for line in face["unblock"]), face["unblock"])


def _write_review(change: Path, body: str, name: str = "2026-10-29-advise.md") -> None:
    reviews = change / "reviews"
    reviews.mkdir(exist_ok=True)
    (reviews / name).write_text(body, encoding="utf-8")


def test_send_back_card_names_particulars() -> None:
    """Owed-heading boxes, not the whole task list, and not a fifth item."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks=(
                "# Tasks\n\n"
                "- [ ] implement the compiler\n\n"
                "## Owed (advise send-back)\n\n"
                "- [ ] Pin the wave write-set before take\n"
                "- [x] already done\n"
                "- [ ] Release taken nodes when launch fails\n"
                "- [ ] Land each persist on HEAD\n"
                "- [ ] Cap the wave after disjointness\n"
                "- [ ] Fifth stays off the card\n"
            ),
        )
        _write_review(
            change,
            "> **ADVISE:** send-back\n"
            "> **READER:** fable-5.1-arch-review\n\n"
            "## Verdict\n\n"
            "1. **Write-set is unknown at pick.** Packets land after take.\n",
        )
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-sheaf-type"}],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root)
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] == "change", face)
        expect(face["reason"] == "send-back", face)
        expect(face["stage_kind"] == "SEND-BACK", face)
        text = "\n".join(face["stage"])
        expect("fable-5.1-arch-review" in text, text)
        expect("Pin the wave write-set before take" in text, text)
        expect("Release taken nodes when launch fails" in text, text)
        expect("Land each persist on HEAD" in text, text)
        expect("Cap the wave after disjointness" in text, text)
        expect("Fifth stays off the card" not in text, text)
        expect("implement the compiler" not in text, text)
        expect("Write-set is unknown" not in text, text)
        expect("Next is change: amend those." in text, text)
        rendered = run(["--until", "roll", "--ready-json", str(fixture)], cwd=root)
        expect("\nSEND-BACK\n" in rendered.stdout, rendered.stdout)
        expect("Pin the wave write-set before take" in rendered.stdout, rendered.stdout)


def test_send_back_uses_review_when_boxes_are_not_owed() -> None:
    """An open task box is not the send-back. Numbered review items are."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks="- [ ] implement the compiler",
        )
        _write_review(
            change,
            "> **ADVISE:** send-back\n"
            "> **READER:** opus-arch\n\n"
            "## Owed corrections\n\n"
            "1. **Stamp the living base** before the union paste.\n"
            "2. **Refuse a stale SHALL** when the blob moved.\n",
        )
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": [], "beads": []},
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root).stdout
        )
        text = "\n".join(face["stage"])
        expect(face["stage_kind"] == "SEND-BACK", face)
        expect("Stamp the living base" in text, text)
        expect("Refuse a stale SHALL" in text, text)
        expect("implement the compiler" not in text, text)


def test_send_back_names_file_when_body_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks="- [ ] amend the SHALL on compile",
            review="send-back",
        )
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": [], "beads": []},
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root).stdout
        )
        text = "\n".join(face["stage"])
        expect("2026-08-27-advise.md" in text, text)
        expect("has no particulars" in text, text)


def test_send_back_stuck_says_reread() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = write_change(root, "add-sheaf-type", rigor="architecture", tasks="- [x] done")
        _write_review(
            change,
            "> **ADVISE:** send-back\n"
            "> **READER:** fable-5.1-arch-review\n\n"
            "## Verdict\n\n"
            "1. **Nothing lands the wave.** N branches and no merge.\n",
        )
        fixture = write_ready(
            root,
            {"ready": [], "waiting": [], "needs_advise": [], "ask": [], "beads": []},
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root).stdout
        )
        expect(face["next"] == "advise", face)
        expect(face["stage_kind"] == "SEND-BACK", face)
        text = "\n".join(face["stage"])
        expect("Nothing lands the wave" in text, text)
        expect("another read, not an amend" in text, text)
        expect("Next is change" not in text, text)


def test_send_back_without_dir_says_so() -> None:
    with tempfile.TemporaryDirectory() as td:
        fixture = write_ready(
            Path(td),
            {
                "ready": [{"id": "add-x"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "send_back": ["add-x"],
                "fold_legal": [],
                "beads": [],
            },
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=Path(td)).stdout
        )
        expect(face["stage_kind"] == "SEND-BACK", face)
        expect("No change directory to read." in "\n".join(face["stage"]), face["stage"])


def test_accept_card_is_one_line() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks="- [ ] implement the compiler",
        )
        _write_review(
            change,
            "> **ADVISE:** accept\n> **READER:** fable-5.1-arch-review\n\nLooks sound.\n",
        )
        fixture = write_ready(
            root,
            {
                "ready": [{"id": "add-sheaf-type"}],
                "waiting": [],
                "needs_advise": [],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root)
        face = json.loads(proc.stdout)
        expect(face["next"] == "act", face)
        expect(face["stage_kind"] == "ACCEPTED", face)
        expect(
            face["stage"] == ["`add-sheaf-type` accepted by fable-5.1-arch-review."],
            face["stage"],
        )
        rendered = run(["--until", "roll", "--ready-json", str(fixture)], cwd=root)
        expect("\nACCEPTED\n" in rendered.stdout, rendered.stdout)


def test_accept_with_nits_names_nits() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        change = write_change(root, "add-sheaf-type", tasks="- [ ] implement")
        _write_review(
            change,
            "> **ADVISE:** accept-with-nits\n> **READER:** opus-arch\n",
        )
        fixture = write_ready(
            root,
            {"ready": ["add-sheaf-type"], "waiting": [], "needs_advise": [], "ask": [], "beads": []},
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root).stdout
        )
        expect(face["next"] == "act", face)
        expect("accepted with nits by opus-arch" in "\n".join(face["stage"]), face)


def test_accept_without_reader_is_quiet() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(
            root,
            "add-sheaf-type",
            rigor="architecture",
            tasks="- [ ] implement the compiler",
            review="accept",
        )
        fixture = write_ready(
            root,
            {"ready": ["add-sheaf-type"], "waiting": [], "needs_advise": [], "ask": [], "beads": []},
        )
        face = json.loads(
            run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root).stdout
        )
        expect(face["next"] == "act", face)
        expect("stage" not in face, face)


def test_unread_advise_has_no_stage_summary() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        write_change(root, "add-agent-body", rigor="architecture")
        fixture = write_ready(
            root,
            {
                "ready": [],
                "waiting": [],
                "needs_advise": [{"id": "add-agent-body"}],
                "ask": [],
                "beads": [],
            },
        )
        proc = run(["--until", "roll", "--ready-json", str(fixture), "--json"], cwd=root)
        face = json.loads(proc.stdout)
        expect(face["next"] == "advise", face)
        expect("stage" not in face, face)
        rendered = run(["--until", "roll", "--ready-json", str(fixture)], cwd=root)
        expect("SEND-BACK" not in rendered.stdout, rendered.stdout)
        expect("ACCEPTED" not in rendered.stdout, rendered.stdout)


def test_scoped_skip_still_advises_same_id() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fixture = kat_fixture(root, "open", needs_advise=["add-umbrella-net"], ready=["add-other"])
        face = json.loads(run([
            "add-umbrella-net", "--skip", "add-umbrella-net",
            "--ready-json", str(fixture), "--json",
        ], cwd=root).stdout)
        expect(face["next"] == "advise" and face["focus"] == "add-umbrella-net", face)


def main() -> int:
    tests = [
        test_umbrella_with_open_beads_is_not_fold_legal,
        test_umbrella_with_closed_beads_folds,
        test_epic_alias_resolves_to_landing,
        test_scoped_skip_does_not_widen,
        test_scoped_skip_still_advises_same_id,
        test_stop_names_the_human_unblock,
        test_continuing_card_has_no_unblock,
        test_ask_stop_says_steer,
        test_preparation_obligation_tracks_act_candidates,
        test_non_act_has_no_preparation_candidates,
        test_empty_ready_no_worker,
        test_until_advise_runs_read,
        test_until_advise_does_not_act,
        test_missing_ready_py_is_no_ready,
        test_missing_openspec_no_scope_is_empty,
        test_scope_missing_dir_is_change,
        test_advise_before_act,
        test_ready_is_act,
        test_pending_scope_does_not_flip,
        test_goal_scope_is_intend,
        test_until_fold_when_legal,
        test_empty_does_not_fold_when_legal,
        test_default_until_is_roll,
        test_unscoped_fold_scans,
        test_roll_send_back_is_change,
        test_roll_bead_landing_is_change,
        test_roll_skips_epic,
        test_roll_intend_orphan_task,
        test_roll_skips_node_type,
        test_roll_skips_legacy_nod_title,
        test_ask_stops_when_pending,
        test_ask_without_elicitation_rolls,
        test_roll_does_not_stop_on_pending,
        test_roll_needs_advise_is_not_fold,
        test_roll_skip_fold_picks_advise,
        test_roll_skip_fold_still_advises_same_id,
        test_wait_alias_interrupt,
        test_interrupt_stops_when_pending,
        test_only_fold,
        test_no_fold_no_beads_is_empty_walk,
        test_run_skill_spawns_other_family_advise,
        test_roll_punt_skips_advise,
        test_roll_send_back_no_boxes_is_not_change,
        test_roll_send_back_with_boxes_is_change,
        test_send_back_card_names_particulars,
        test_send_back_uses_review_when_boxes_are_not_owed,
        test_send_back_names_file_when_body_empty,
        test_send_back_stuck_says_reread,
        test_send_back_without_dir_says_so,
        test_accept_card_is_one_line,
        test_accept_with_nits_names_nits,
        test_accept_without_reader_is_quiet,
        test_unread_advise_has_no_stage_summary,
        test_wait_eyes_is_stop_eyes,
        test_roll_eyes_does_not_intend_leftover,
        test_roll_unrelated_ready_moves_with_eyes_listed,
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
