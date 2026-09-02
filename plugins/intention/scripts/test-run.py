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
            {"ready": [], "waiting": [], "needs_advise": [], "ask": []},
        )
        proc = run(["--ready-json", str(fixture), "--json"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["stop"] == "empty", face)
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
            ["add-x", "--ready-json", str(fixture), "--json"],
            cwd=root,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["next"] is None, face)
        expect(face["stop"] == "empty", face)


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


def test_run_skill_spawns_other_family_advise() -> None:
    """Conductor prompt: same-family advise is spawn, not punt-first halt."""
    skill = HERE.parents[0] / "skills" / "run" / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    expect("spawn that reader" in text or "spawn an other-family" in text, text[:800])
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


def main() -> int:
    tests = [
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
        test_unscoped_fold_scans,
        test_roll_send_back_is_change,
        test_roll_bead_landing_is_change,
        test_roll_skips_epic,
        test_roll_intend_orphan_task,
        test_ask_stops_when_pending,
        test_ask_without_elicitation_rolls,
        test_roll_does_not_stop_on_pending,
        test_roll_needs_advise_is_not_fold,
        test_roll_skip_fold_picks_advise,
        test_roll_skip_fold_still_advises_same_id,
        test_run_skill_spawns_other_family_advise,
        test_roll_punt_skips_advise,
        test_roll_send_back_no_boxes_is_not_change,
        test_roll_send_back_with_boxes_is_change,
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
