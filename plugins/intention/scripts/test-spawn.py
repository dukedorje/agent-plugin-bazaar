#!/usr/bin/env python3
"""Focused verify for spawn.py. No live harness required."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPAWN = HERE / "spawn.py"
PACKET = HERE.parents[2] / "docs" / "contracts" / "examples" / "density-explicit.packet.json"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SPAWN), *args],
        text=True,
        capture_output=True,
    )


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_unique_stage() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        a = run(["stage", "--packet", str(PACKET), "--root", str(root)])
        b = run(["stage", "--packet", str(PACKET), "--root", str(root)])
        expect(a.returncode == 0, a.stderr)
        expect(b.returncode == 0, b.stderr)
        sa, sb = json.loads(a.stdout), json.loads(b.stdout)
        expect(sa["prompt_file"] != sb["prompt_file"], (sa["prompt_file"], sb["prompt_file"]))
        pa, pb = Path(sa["prompt_file"]), Path(sb["prompt_file"])
        expect(pa.is_file() and pa.stat().st_size > 0, pa)
        expect(pb.is_file() and pb.stat().st_size > 0, pb)
        expect(sa["surface"] == "packet-only", sa)
        expect(sa["interface"] == "deepseek-flash", sa)
        text = pa.read_text(encoding="utf-8")
        expect("/act" not in text, text)
        expect("/intend" not in text, text)
        expect("/meta-execute" not in text, text)
        expect("/run" not in text, text)
        expect("pkt-density-explicit" in text, text)
        expect(str(Path(sa["packet_file"])) in text, text)


def test_empty_prompt_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        staged = run(["stage", "--packet", str(PACKET), "--root", str(root)])
        expect(staged.returncode == 0, staged.stderr)
        spec = json.loads(staged.stdout)
        Path(spec["prompt_file"]).write_text("", encoding="utf-8")
        sentinel = root / "started"
        hanging = [
            "run",
            "--spec",
            spec["spec_file"],
            "--adapter",
            "exec",
            "--argv",
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(sentinel)!r}).write_text('x'); import time; time.sleep(30)",
        ]
        proc = run(hanging)
        expect(proc.returncode == 2, proc.stdout + proc.stderr)
        expect("empty prompt" in proc.stderr, proc.stderr)
        expect(not sentinel.exists(), "adapter started despite empty prompt")


def test_missing_prompt_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        spec = Path(td) / "spec.json"
        spec.write_text(
            json.dumps({"prompt_file": str(Path(td) / "nope.md"), "timeout_sec": 1}),
            encoding="utf-8",
        )
        proc = run(["run", "--spec", str(spec)])
        expect(proc.returncode == 2, proc.stdout + proc.stderr)
        expect("missing prompt" in proc.stderr, proc.stderr)


def test_stall_infra_red() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        staged = run(
            ["stage", "--packet", str(PACKET), "--root", str(root), "--timeout", "0.3"]
        )
        expect(staged.returncode == 0, staged.stderr)
        spec_path = json.loads(staged.stdout)["spec_file"]
        spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
        spec["timeout_sec"] = 0.3
        Path(spec_path).write_text(json.dumps(spec), encoding="utf-8")
        proc = run(
            [
                "run",
                "--spec",
                spec_path,
                "--adapter",
                "exec",
                "--argv",
                sys.executable,
                "-c",
                "import time; time.sleep(10)",
            ]
        )
        expect(proc.returncode == 0, proc.stderr)
        face = json.loads(proc.stdout)
        expect(face["disposition"] == "infra-red", face)
        expect("stall" in face["blockers"], face)


def test_claude_adapter_argv() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        staged = run(["stage", "--packet", str(PACKET), "--root", str(root)])
        expect(staged.returncode == 0, staged.stderr)
        spec_path = json.loads(staged.stdout)["spec_file"]
        spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
        spec["interface"] = "sonnet-5"
        spec["surface"] = "packet-only"
        Path(spec_path).write_text(json.dumps(spec), encoding="utf-8")
        fake = root / "fake-claude"
        argv_log = root / "argv.json"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json,sys\n"
            f"json.dump({{'argv': sys.argv, 'stdin': sys.stdin.read()}}, open({str(argv_log)!r},'w'))\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        env_run = subprocess.run(
            [sys.executable, str(SPAWN), "run", "--spec", spec_path, "--adapter", "claude"],
            text=True,
            capture_output=True,
            env={**dict(**subprocess.os.environ), "CLAUDE_BIN": str(fake)},
        )
        expect(env_run.returncode == 0, env_run.stderr + env_run.stdout)
        logged = json.loads(argv_log.read_text(encoding="utf-8"))
        argv, stdin = logged["argv"], logged["stdin"]
        expect("-p" in argv, argv)
        expect("--model" in argv and "claude-sonnet-5" in argv, argv)
        expect("--effort" in argv and "low" in argv, argv)
        expect("--disable-slash-commands" in argv, argv)
        expect(not any("You are executing ONE work node" in a for a in argv), argv)
        expect("You are executing ONE work node" in stdin, stdin[:200])
        expect("pkt-density-explicit" in stdin, stdin[:400])
        face = json.loads(env_run.stdout)
        expect(face["disposition"] == "pass", face)


def test_codex_adapter_argv() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-codex",
            "node_id": "nod-codex",
            "goal": "Reply with the single word pong.",
            "assignee": {
                "id": "agt-sol",
                "kind": "model",
                "harness": "codex",
                "interface": "gpt-5.6-sol",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-sol"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {"permission": "read", "paths": [], "do_not": ["deploy"]},
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        fake = root / "fake-codex"
        argv_log = root / "argv.json"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json,sys\n"
            f"json.dump({{'argv': sys.argv, 'stdin': sys.stdin.read()}}, open({str(argv_log)!r},'w'))\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        env = {**os.environ, "CODEX_BIN": str(fake)}
        staged = subprocess.run(
            [sys.executable, str(SPAWN), "stage", "--packet", str(pkt), "--root", str(root)],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        spec = json.loads(staged.stdout)
        expect(spec["adapter"] == "codex", spec)
        env_run = subprocess.run(
            [sys.executable, str(SPAWN), "run", "--spec", spec["spec_file"], "--adapter", "codex"],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(env_run.returncode == 0, env_run.stderr + env_run.stdout)
        logged = json.loads(argv_log.read_text(encoding="utf-8"))
        argv, stdin = logged["argv"], logged["stdin"]
        expect("exec" in argv, argv)
        expect(argv[-1] == "-", argv)
        expect("-m" in argv and "gpt-5.6-sol" in argv, argv)
        expect("--sandbox" in argv and "read-only" in argv, argv)
        expect("--skip-git-repo-check" in argv, argv)
        expect("--ephemeral" in argv, argv)
        expect("-c" in argv, argv)
        expect(any("model_reasoning_effort=" in a and "high" in a for a in argv), argv)
        expect(not any("You are executing ONE work node" in a for a in argv), argv)
        expect("You are executing ONE work node" in stdin, stdin[:200])
        expect("pkt-codex" in stdin, stdin[:400])
        face = json.loads(env_run.stdout)
        expect(face["disposition"] == "pass", face)


def test_openai_adapter_missing_key() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-sol",
            "node_id": "nod-sol",
            "goal": "Reply with the single word pong.",
            "assignee": {
                "id": "agt-sol",
                "kind": "model",
                "harness": "codex",
                "interface": "gpt-5.6-sol",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-sol"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {"permission": "read", "paths": [], "do_not": ["deploy"]},
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if k not in {"OPENAI_API_KEY", "CODEX_BIN"}}
        env["CODEX_BIN"] = "/nonexistent/codex-not-installed"
        staged = subprocess.run(
            [sys.executable, str(SPAWN), "stage", "--packet", str(pkt), "--root", str(root)],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        spec = json.loads(staged.stdout)
        expect(spec["adapter"] == "none", spec)
        proc = subprocess.run(
            [sys.executable, str(SPAWN), "run", "--spec", spec["spec_file"], "--adapter", "openai"],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["disposition"] == "infra-red", face)
        expect("openai-key-missing" in face["blockers"], face)


def test_openai_adapter_sol_live() -> None:
    key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not key:
        print("skip test_openai_adapter_sol_live (no OPENAI_API_KEY)")
        return
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-sol-live",
            "node_id": "nod-sol-live",
            "goal": "Reply with the single word pong.",
            "assignee": {
                "id": "agt-sol",
                "kind": "model",
                "harness": "codex",
                "interface": "gpt-5.6-sol",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-sol"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {"permission": "write", "paths": [], "do_not": ["deploy"]},
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        env = {**os.environ, "CODEX_BIN": "/nonexistent/codex-not-installed"}
        staged = subprocess.run(
            [sys.executable, str(SPAWN), "stage", "--packet", str(pkt), "--root", str(root)],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        spec = json.loads(staged.stdout)
        expect(spec["adapter"] == "openai", spec)
        expect(spec["interface"] == "gpt-5.6-sol", spec)
        proc = run(["run", "--spec", spec["spec_file"], "--adapter", "openai"])
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        face = json.loads(proc.stdout)
        expect(face["disposition"] == "pass", face)
        expect("pong" in (face.get("summary") or "").lower(), face)


def test_read_permission_prompt_is_reader_brief() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-advise",
            "node_id": "nod-advise",
            "goal": "Read add-x. Verdict accept or send-back.",
            "assignee": {
                "id": "agt-fable",
                "kind": "model",
                "harness": "claude",
                "interface": "fable-5.1",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-fable"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {
                "permission": "read",
                "paths": ["openspec/changes/add-x/reviews/"],
                "do_not": ["fold", "act", "deploy"],
            },
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        staged = run(["stage", "--packet", str(pkt), "--root", str(root)])
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        spec = json.loads(staged.stdout)
        prompt = Path(spec["prompt_file"]).read_text(encoding="utf-8")
        expect("Write your own review file" in prompt, prompt)
        expect("**ADVISE:** accept" in prompt, prompt)
        expect("**READER:**" in prompt, prompt)
        expect("Edit and stop" not in prompt, prompt)
        expect("Do not implement product code" in prompt, prompt)
        expect(spec.get("permission") == "read", spec)
        expect(any("reviews" in p for p in spec.get("paths") or []), spec)


def test_codex_advise_sandbox_is_writable() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-advise-sol",
            "node_id": "nod-advise",
            "change_id": "add-x",
            "goal": "Write the advise review for add-x.",
            "assignee": {
                "id": "agt-sol",
                "kind": "model",
                "harness": "codex",
                "interface": "gpt-5.6-sol",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-sol"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {
                "permission": "write",
                "paths": ["openspec/changes/add-x/reviews/"],
                "do_not": ["fold", "act", "deploy", "implement"],
            },
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        fake = root / "fake-codex"
        argv_log = root / "argv.json"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json,sys\n"
            f"json.dump({{'argv': sys.argv, 'stdin': sys.stdin.read()}}, open({str(argv_log)!r},'w'))\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        env = {**os.environ, "CODEX_BIN": str(fake)}
        staged = subprocess.run(
            [sys.executable, str(SPAWN), "stage", "--packet", str(pkt), "--root", str(root)],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        spec = json.loads(staged.stdout)
        env_run = subprocess.run(
            [sys.executable, str(SPAWN), "run", "--spec", spec["spec_file"], "--adapter", "codex"],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(env_run.returncode == 0, env_run.stderr + env_run.stdout)
        logged = json.loads(argv_log.read_text(encoding="utf-8"))
        argv, stdin = logged["argv"], logged["stdin"]
        expect("--sandbox" in argv and "workspace-write" in argv, argv)
        expect("read-only" not in argv, argv)
        expect("Write your own review file" in stdin, stdin[:500])


def test_consult_prompt_is_not_advise() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        packet = {
            "id": "pkt-consult-x",
            "node_id": "consult",
            "goal": "Second-opinion this architecture: keep spawn cwd as workspace.",
            "role": "consultant",
            "assignee": {
                "id": "agt-fable-5-1-arch-review",
                "kind": "model",
                "harness": "claude",
                "interface": "fable-5.1",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-fable-5-1-arch-review"},
            },
            "requester": {
                "id": "agt-conductor",
                "kind": "group",
                "harness": "none",
                "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
            },
            "constraints": {
                "permission": "read",
                "paths": ["ARCHITECTURE.md"],
                "do_not": ["fold", "act", "deploy", "implement", "advise"],
            },
            "acceptance": {"kind": "none"},
            "load_class": "structure-clear",
            "rigor": "architecture",
            "density": "lean",
            "surface": "packet-only",
        }
        pkt = root / "packet.json"
        pkt.write_text(json.dumps(packet), encoding="utf-8")
        staged = run(["stage", "--packet", str(pkt), "--root", str(root)])
        expect(staged.returncode == 0, staged.stderr + staged.stdout)
        prompt = Path(json.loads(staged.stdout)["prompt_file"]).read_text(encoding="utf-8")
        expect("SECOND OPINION" in prompt, prompt)
        expect("**CONSULT:** agree" in prompt, prompt)
        expect("**ADVISE:** accept" not in prompt, prompt)
        expect("does not unblock act" in prompt, prompt)


def test_consult_cli_fake_claude() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fake = root / "fake-claude"
        argv_log = root / "argv.json"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json,os,sys\n"
            f"json.dump({{'argv': sys.argv, 'stdin': sys.stdin.read(), 'cwd': os.getcwd()}}, open({str(argv_log)!r},'w'))\n"
            "sys.stdout.write('> **CONSULT:** caution\\n\\nKeep spawn cwd as the workspace.\\n')\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in {"OPENAI_API_KEY", "CODEX_BIN", "CLAUDE_BIN"}
        }
        env["CLAUDE_BIN"] = str(fake)
        env["CODEX_BIN"] = "/nonexistent/codex-not-installed"
        proc = subprocess.run(
            [
                sys.executable,
                str(SPAWN),
                "consult",
                "--shape",
                "architecture-review",
                "--id",
                "fable-5.1-arch-review",
                "--goal",
                "Should spawn cwd be the workspace?",
                "--paths",
                "ARCHITECTURE.md",
                "--root",
                str(root),
            ],
            text=True,
            capture_output=True,
            env=env,
        )
        expect(proc.returncode == 0, proc.stderr + proc.stdout)
        out = json.loads(proc.stdout)
        expect(out["shape"] == "architecture-review", out)
        expect(len(out["opinions"]) == 1, out)
        op = out["opinions"][0]
        expect(op["verdict"] == "caution", op)
        expect("workspace" in (op.get("body") or "").lower(), op)
        logged = json.loads(argv_log.read_text(encoding="utf-8"))
        expect("-p" in logged["argv"], logged["argv"])
        expect(not any("SECOND OPINION" in a for a in logged["argv"]), logged["argv"])
        expect("SECOND OPINION" in logged["stdin"], logged["stdin"][:300])
        expect("**ADVISE:** accept" not in logged["stdin"], logged["stdin"])
        expect(Path(logged["cwd"]).resolve() == root.resolve(), logged["cwd"])


def test_consult_who_exclusive() -> None:
    proc = run(
        [
            "consult",
            "--panel",
            "--who",
            "fable",
            "--goal",
            "x",
        ]
    )
    expect(proc.returncode == 2, proc.stdout + proc.stderr)
    expect("mutually exclusive" in proc.stderr, proc.stderr)
    grok = run(
        [
            "consult",
            "--shape",
            "architecture-review",
            "--who",
            "grok",
            "--goal",
            "x",
        ]
    )
    expect(grok.returncode == 2, grok.stdout + grok.stderr)
    expect("no adapter" in grok.stderr, grok.stderr)


def test_consult_empty_fails() -> None:
    proc = subprocess.run(
        [sys.executable, str(SPAWN), "consult", "--goal", ""],
        text=True,
        capture_output=True,
        input="",
    )
    expect(proc.returncode == 2, proc.stdout + proc.stderr)
    expect("empty consult brief" in proc.stderr, proc.stderr)


def test_empty_packet_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        empty = Path(td) / "empty.json"
        empty.write_text("", encoding="utf-8")
        proc = run(["stage", "--packet", str(empty), "--root", str(td)])
        expect(proc.returncode == 2, proc.stdout + proc.stderr)


def main() -> int:
    tests = [
        test_unique_stage,
        test_empty_prompt_fails,
        test_missing_prompt_fails,
        test_stall_infra_red,
        test_claude_adapter_argv,
        test_codex_adapter_argv,
        test_openai_adapter_missing_key,
        test_openai_adapter_sol_live,
        test_read_permission_prompt_is_reader_brief,
        test_codex_advise_sandbox_is_writable,
        test_consult_prompt_is_not_advise,
        test_consult_cli_fake_claude,
        test_consult_who_exclusive,
        test_consult_empty_fails,
        test_empty_packet_fails,
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
