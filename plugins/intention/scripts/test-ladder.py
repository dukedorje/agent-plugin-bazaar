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
DROP_OPENAI = ("OPENAI_API_KEY",)


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


def env_without_openai() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if k not in DROP_OPENAI}


def env_with_openai(key: str = "sk-test-not-used") -> dict[str, str]:
    out = env_without_openai()
    out["OPENAI_API_KEY"] = key
    return out


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def assign(shape: str, extra: list[str] | None = None) -> dict:
    proc = run(["assign", "--shape", shape, *(extra or [])])
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
        ("plan", "fable-5-plan", "lean"),
        ("intend-consult", "fable-5-plan", "lean"),
        ("architecture-review", "opus-4.8-arch-review", "lean"),
        ("fold", "opus-5-fold", "standard"),
    ]
    for shape, route_id, density in cases:
        try:
            got = assign(shape)
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
        expect(got["id"] == "opus-4.8-arch-review", got)
        expect(got["harness"] == "claude", got)
        expect(got["interface"] == "opus-4.8", got)
        alt = run(["assign", "--shape", "architecture-review", "--include-unavailable"])
        expect(alt.returncode == 0, alt.stderr)
        expect(json.loads(alt.stdout)["id"] == "opus-4.8-arch-review", alt.stdout)
        show = json.loads(run(["show"], env=env_without_openai()).stdout)
        grok = next(r for r in show["routes"] if r["id"] == "grok-arch-review")
        expect(grok["available"] is True, grok)
        sol = next(r for r in show["routes"] if r["id"] == "sol-arch-review")
        expect(sol["available"] is False, sol)
        print("pass arch-review default is opus-4.8; grok on; sol off without key")
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
        off = json.loads(run(["show"], env=env_without_openai()).stdout)
        sol_off = next(r for r in off["routes"] if r["id"] == "sol-arch-review")
        expect(sol_off["available"] is False, sol_off)
        on = json.loads(run(["show"], env=env_with_openai()).stdout)
        sol_on = next(r for r in on["routes"] if r["id"] == "sol-arch-review")
        expect(sol_on["available"] is True, sol_on)
        picked = json.loads(
            run(
                ["assign", "--shape", "architecture-review", "--id", "sol-arch-review"],
                env=env_with_openai(),
            ).stdout
        )
        expect(picked["id"] == "sol-arch-review", picked)
        expect(picked["interface"] == "gpt-5.6-sol", picked)
        default = json.loads(
            run(["assign", "--shape", "architecture-review"], env=env_with_openai()).stdout
        )
        expect(default["id"] == "opus-4.8-arch-review", default)
        print("pass sol available iff OPENAI_API_KEY; still not default")
    except Exception as exc:  # noqa: BLE001
        failed += 1
        print(f"FAIL sol env: {exc}")

    if failed:
        print(f"FAIL {failed}")
        return 1
    print("pass ladder")
    return 0


if __name__ == "__main__":
    sys.exit(main())
