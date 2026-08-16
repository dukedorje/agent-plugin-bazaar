#!/usr/bin/env python3
"""Focused verify for spawn.py. No live harness required."""

from __future__ import annotations

import json
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
            f"json.dump(sys.argv, open({str(argv_log)!r},'w'))\n",
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
        argv = json.loads(argv_log.read_text(encoding="utf-8"))
        expect("-p" in argv, argv)
        expect("--model" in argv and "claude-sonnet-5" in argv, argv)
        expect("--effort" in argv and "low" in argv, argv)
        expect("--disable-slash-commands" in argv, argv)
        face = json.loads(env_run.stdout)
        expect(face["disposition"] == "pass", face)


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
