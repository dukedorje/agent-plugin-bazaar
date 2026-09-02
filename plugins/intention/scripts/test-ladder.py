#!/usr/bin/env python3
"""Focused verify for ladder.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LADDER = HERE / "ladder.py"
DROP_SOL = ("OPENAI_API_KEY", "CODEX_BIN")
MISSING_CODEX = "/nonexistent/codex-not-installed"


def run(
    args: list[str],
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LADDER), *args],
        text=True,
        capture_output=True,
        env=env,
    )


def env_without_sol() -> dict[str, str]:
    out = {k: v for k, v in os.environ.items() if k not in DROP_SOL}
    out["CODEX_BIN"] = MISSING_CODEX
    return out


def env_with_openai(key: str = "sk-test-not-used") -> dict[str, str]:
    out = env_without_sol()
    out["OPENAI_API_KEY"] = key
    return out


def env_with_codex() -> dict[str, str]:
    out = env_without_sol()
    out["CODEX_BIN"] = sys.executable
    return out


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def assign(
    shape: str,
    extra: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> dict:
    proc = run(["assign", "--shape", shape, *(extra or [])], env=env)
    expect(proc.returncode == 0, proc.stderr or proc.stdout)
    return json.loads(proc.stdout)


def main() -> int:
    failed = 0
    cases = [
        ("known", "sonnet-5", "explicit"),
        ("mechanical", "sonnet-5", "explicit"),
        ("thinking", "opus-5", "standard"),
        ("implementation", "opus-5", "standard"),
        ("design", "opus-5-design", "standard"),
        ("plan", "fable-5.1-plan", "lean"),
        ("intend-consult", "fable-5.1-plan", "lean"),
        ("architecture-review", "fable-5.1-arch-review", "lean"),
        ("fold", "opus-5-fold", "standard"),
    ]
    for shape, route_id, density in cases:
        try:
            got = assign(shape, env=env_without_sol())
            expect(got["id"] == route_id, f"{shape} -> {got.get('id')} want {route_id}")
            expect(got["density"] == density, f"{shape} density {got.get('density')}")
            expect(got.get("available") is True, f"{shape} not available")
            print(f"pass {shape} -> {route_id}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {shape}: {exc}")

    try:
        design = assign("design")
        expect("designer" in design.get("skills", []), design)
        expect(design["effort"] in {"low", "medium"}, design)
        print("pass design uses designer skills")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL design skills: {exc}")

    try:
        proc = run(["assign", "--shape", "architecture-review"])
        got = json.loads(proc.stdout)
        expect(got["id"] == "fable-5.1-arch-review", got)
        expect(got["harness"] == "claude", got)
        expect(got["interface"] == "fable-5.1", got)
        alt = run(["assign", "--shape", "architecture-review", "--include-unavailable"])
        expect(alt.returncode == 0, alt.stderr)
        expect(json.loads(alt.stdout)["id"] == "fable-5.1-arch-review", alt.stdout)
        show = json.loads(run(["show"], env=env_without_sol()).stdout)
        grok = next(r for r in show["routes"] if r["id"] == "grok-arch-review")
        expect(grok["available"] is True, grok)
        sol = next(r for r in show["routes"] if r["id"] == "sol-arch-review")
        expect(sol["available"] is False, sol)
        print("pass arch-review default is fable-5.1; grok on; sol off without key")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL sol optional: {exc}")

    try:
        got = assign("fold")
        expect(got["id"] == "opus-5-fold", got)
        expect(got["role"] == "folder", got)
        expect(got["interface"] == "opus-5", got)
        show = json.loads(run(["show"]).stdout)
        grok_fold = next(r for r in show["routes"] if r["id"] == "grok-fold")
        expect(grok_fold["available"] is False, grok_fold)
        print("pass fold is opus-5; grok-fold optional")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL fold route: {exc}")

    try:
        proc = run(["assign", "--shape", "not-a-shape"])
        expect(proc.returncode != 0, "unknown shape should fail")
        print("pass unknown shape fails")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL unknown: {exc}")

    try:
        off = json.loads(run(["show"], env=env_without_sol()).stdout)
        sol_off = next(r for r in off["routes"] if r["id"] == "sol-arch-review")
        expect(sol_off["available"] is False, sol_off)
        on_key = json.loads(run(["show"], env=env_with_openai()).stdout)
        expect(
            next(r for r in on_key["routes"] if r["id"] == "sol-arch-review")["available"]
            is True,
            on_key,
        )
        on_cli = json.loads(run(["show"], env=env_with_codex()).stdout)
        expect(
            next(r for r in on_cli["routes"] if r["id"] == "sol-arch-review")["available"]
            is True,
            on_cli,
        )
        picked = json.loads(
            run(
                ["assign", "--shape", "architecture-review", "--id", "sol-arch-review"],
                env=env_with_codex(),
            ).stdout
        )
        expect(picked["id"] == "sol-arch-review", picked)
        expect(picked["interface"] == "gpt-5.6-sol", picked)
        default = json.loads(
            run(["assign", "--shape", "architecture-review"], env=env_with_codex()).stdout
        )
        expect(default["id"] == "fable-5.1-arch-review", default)
        print("pass sol available iff codex CLI or OPENAI_API_KEY; still not default")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL sol env: {exc}")

    try:
        grok_author = json.loads(
            run(
                [
                    "assign",
                    "--shape",
                    "architecture-review",
                    "--not-harness",
                    "grok",
                ],
                env=env_without_sol(),
            ).stdout
        )
        expect(grok_author["id"] == "fable-5.1-arch-review", grok_author)
        expect(grok_author["harness"] == "claude", grok_author)
        claude_author = json.loads(
            run(
                [
                    "assign",
                    "--shape",
                    "architecture-review",
                    "--not-harness",
                    "claude",
                ],
                env=env_without_sol(),
            ).stdout
        )
        expect(claude_author["id"] == "grok-arch-review", claude_author)
        expect(claude_author["harness"] == "grok", claude_author)
        print("pass --not-harness skips author family")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL not-harness: {exc}")

    try:
        got = assign("known", env=env_with_codex())
        expect(got["id"] == "terra-known", got)
        expect(got["interface"] == "gpt-5.6-terra", got)
        nxt = assign("known", extra=["--after", "terra-known"], env=env_with_codex())
        expect(nxt["id"] == "sonnet-5", nxt)
        think = assign("thinking", env=env_with_codex())
        expect(think["id"] == "sol-implement", think)
        think_fb = assign("thinking", extra=["--after", "sol-implement"], env=env_with_codex())
        expect(think_fb["id"] == "opus-5", think_fb)
        plan = assign("plan", env=env_with_codex())
        expect(plan["id"] == "fable-5.1-plan", plan)
        plan_fb = assign("plan", extra=["--after", "fable-5.1-plan"], env=env_with_codex())
        expect(plan_fb["id"] == "sol-plan", plan_fb)
        print("pass terra/sol primaries and --after handoff")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL priority handoff: {exc}")

    try:
        proc = run(
            ["panel", "--shape", "architecture-review"],
            env=env_with_codex(),
        )
        expect(proc.returncode == 0, proc.stderr)
        panel = json.loads(proc.stdout)
        ids = [r["id"] for r in panel]
        expect(ids[:4] == [
            "fable-5.1-arch-review",
            "sol-arch-review",
            "opus-4.8-arch-review",
            "grok-arch-review",
        ], ids)
        print("pass architecture panel order Fable, Sol, 4.8, Grok")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL panel: {exc}")

    try:
        # Terra down: --after terra-known still reaches Sonnet.
        nxt = assign("known", extra=["--after", "terra-known"], env=env_without_sol())
        expect(nxt["id"] == "sonnet-5", nxt)
        print("pass --after skips unavailable rungs")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL after skip-forward: {exc}")

    try:
        fable = json.loads(
            run(["assign", "--shape", "architecture-review", "--who", "fable"]).stdout
        )
        expect(fable["id"] == "fable-5.1-arch-review", fable)
        four = json.loads(
            run(["assign", "--shape", "architecture-review", "--who", "4.8"]).stdout
        )
        expect(four["id"] == "opus-4.8-arch-review", four)
        several = json.loads(
            run(
                ["assign", "--shape", "architecture-review", "--who", "sol,fable"],
                env=env_with_codex(),
            ).stdout
        )
        ids = [r["id"] for r in several]
        expect(ids == ["fable-5.1-arch-review", "sol-arch-review"], ids)
        terra_think = run(["assign", "--shape", "thinking", "--who", "terra"])
        expect(terra_think.returncode != 0, terra_think.stdout)
        expect("unknown who" in terra_think.stderr, terra_think.stderr)
        four_think = run(["assign", "--shape", "thinking", "--who", "4.8"])
        expect(four_think.returncode != 0, four_think.stderr)
        mixed = run(
            ["assign", "--shape", "architecture-review", "--who", "fable", "--id", "sol-arch-review"]
        )
        expect(mixed.returncode != 0, mixed.stdout + mixed.stderr)
        print("pass --who nicknames are shape-scoped")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL who: {exc}")

    if failed:
        print(f"FAIL {failed}")
        return 1
    print("pass ladder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
