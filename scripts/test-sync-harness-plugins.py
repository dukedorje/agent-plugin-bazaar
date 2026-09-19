#!/usr/bin/env python3
"""Fixtures for scripts/sync-harness-plugins.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import importlib.util

ROOT = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location(
    "sync_harness_plugins", ROOT / "sync-harness-plugins.py"
)
assert _SPEC and _SPEC.loader
sync = importlib.util.module_from_spec(_SPEC)
sys.modules["sync_harness_plugins"] = sync
_SPEC.loader.exec_module(sync)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def plugin_tree(root: Path, name: str, version: str, marker: str) -> Path:
    dest = root / name
    write(
        dest / ".claude-plugin" / "plugin.json",
        json.dumps({"name": name, "version": version}),
    )
    write(dest / "skills" / "x" / "SKILL.md", marker)
    write(dest / "references" / "ladder.json", marker)
    return dest


def bazaar_repo(tmp: Path) -> Path:
    repo = tmp / "bazaar"
    write(
        repo / ".claude-plugin" / "marketplace.json",
        json.dumps(
            {
                "name": "agent-plugin-bazaar",
                "plugins": [
                    {"name": "intention", "version": "0.5.0", "source": "./plugins/intention"},
                    {"name": "metacoding", "version": "0.1.1", "source": "./plugins/metacoding"},
                ],
            }
        ),
    )
    write(
        repo / ".grok-plugin" / "marketplace.json",
        json.dumps(
            {
                "name": "agent-plugin-bazaar",
                "plugins": [
                    {
                        "name": "intention",
                        "version": "0.5.0",
                        "source": {"type": "local", "path": "./plugins/intention"},
                    }
                ],
            }
        ),
    )
    plugin_tree(repo / "plugins", "intention", "0.5.0", "NEW")
    plugin_tree(repo / "plugins", "metacoding", "0.1.1", "META")
    return repo


def expect(cond: bool, msg: object) -> None:
    if not cond:
        raise AssertionError(msg)


def test_mirrors_versioned_claude_and_codex(tmp: Path) -> None:
    repo = bazaar_repo(tmp)
    home = tmp / "home"
    claude_old = (
        home
        / ".claude"
        / "plugins"
        / "cache"
        / "agent-plugin-bazaar"
        / "intention"
        / "0.5.0"
    )
    write(claude_old / ".claude-plugin" / "plugin.json", json.dumps({"name": "intention", "version": "0.5.0"}))
    write(claude_old / "skills" / "x" / "SKILL.md", "OLD")
    write(claude_old / ".in_use", "1")
    write(claude_old / "stale.txt", "gone")
    codex = (
        home
        / ".codex"
        / "plugins"
        / "cache"
        / "agent-plugin-bazaar"
        / "intention"
        / "0.5.0+codex.stamp"
    )
    write(codex / ".codex-plugin" / "plugin.json", json.dumps({"name": "intention", "version": "0.5.0+codex.stamp"}))
    write(codex / "skills" / "x" / "SKILL.md", "OLD")
    notes = sync.sync(repo, home, dry_run=False, cli=False)
    expect((claude_old / "skills" / "x" / "SKILL.md").read_text() == "NEW", notes)
    expect((claude_old / ".in_use").read_text() == "1", "protected .in_use")
    expect(not (claude_old / "stale.txt").exists(), "stale deleted")
    expect((codex / "skills" / "x" / "SKILL.md").read_text() == "NEW", notes)
    expect((codex / "references" / "ladder.json").read_text() == "NEW", notes)


def test_mirrors_marketplace_clone_and_grok_install(tmp: Path) -> None:
    repo = bazaar_repo(tmp)
    home = tmp / "home"
    mp = home / ".claude" / "plugins" / "marketplaces" / "agent-plugin-bazaar"
    write(mp / ".claude-plugin" / "marketplace.json", json.dumps({"plugins": []}))
    write(mp / "plugins" / "intention" / "skills" / "x" / "SKILL.md", "OLD")
    grok = home / ".grok" / "installed-plugins" / "intention-abc"
    write(grok / ".claude-plugin" / "plugin.json", json.dumps({"name": "intention", "version": "0.4.0"}))
    write(grok / "skills" / "x" / "SKILL.md", "OLD")
    write(
        home / ".grok" / "installed-plugins" / "registry.json",
        json.dumps(
            {
                "repos": {
                    "intention-abc": {
                        "path": str(grok),
                        "marketplace": {
                            "source_url_or_path": "https://github.com/dukedorje/agent-plugin-bazaar.git"
                        },
                    }
                }
            }
        ),
    )
    notes = sync.sync(repo, home, dry_run=False, cli=False)
    expect((mp / "plugins" / "intention" / "skills" / "x" / "SKILL.md").read_text() == "NEW", notes)
    expect((grok / "skills" / "x" / "SKILL.md").read_text() == "NEW", notes)
    expect((grok / ".claude-plugin" / "plugin.json").read_text().find("0.5.0") > 0, "manifest copied")


def test_dry_run_does_not_write(tmp: Path) -> None:
    repo = bazaar_repo(tmp)
    home = tmp / "home"
    dest = home / ".claude" / "plugins" / "cache" / "agent-plugin-bazaar" / "intention" / "0.5.0"
    write(dest / ".claude-plugin" / "plugin.json", json.dumps({"name": "intention"}))
    write(dest / "skills" / "x" / "SKILL.md", "OLD")
    notes = sync.sync(repo, home, dry_run=True, cli=False)
    expect((dest / "skills" / "x" / "SKILL.md").read_text() == "OLD", notes)
    expect(any(n.startswith("would-mirror") for n in notes), notes)


def test_skips_this_clone(tmp: Path) -> None:
    repo = bazaar_repo(tmp)
    notes = sync.sync(repo, tmp / "empty-home", dry_run=False, cli=False)
    expect(any("no-cache" in n for n in notes), notes)
    expect((repo / "plugins" / "intention" / "skills" / "x" / "SKILL.md").read_text() == "NEW", "source intact")


def git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True)


def commit_all(cwd: Path, message: str) -> None:
    git(cwd, "add", ".")
    subprocess.run(
        [
            "git",
            "-C",
            str(cwd),
            "-c",
            "user.email=t@t",
            "-c",
            "user.name=t",
            "commit",
            "-m",
            message,
        ],
        check=True,
        capture_output=True,
    )


def test_ff_marketplace_clone(tmp: Path) -> None:
    remote = tmp / "agent-plugin-bazaar.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    work = tmp / "work"
    subprocess.run(
        ["git", "init", "-b", "main", str(work)],
        check=True,
        capture_output=True,
    )
    write(work / "README.md", "one")
    commit_all(work, "one")
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-u", "origin", "main")
    cache = tmp / "home" / ".claude" / "plugins" / "marketplaces" / "agent-plugin-bazaar"
    subprocess.run(["git", "clone", str(remote), str(cache)], check=True, capture_output=True)
    other = tmp / "unrelated.git"
    subprocess.run(["git", "init", "--bare", str(other)], check=True, capture_output=True)
    git(cache, "remote", "set-url", "origin", str(other))
    skipped = sync.git_ff_main(cache, tmp / "bazaar")
    expect(skipped is None, skipped)
    git(cache, "remote", "set-url", "origin", str(remote))
    write(work / "README.md", "two")
    commit_all(work, "two")
    git(work, "push")
    result = sync.git_ff_main(cache, tmp / "bazaar")
    expect(result is not None and result.startswith("ff "), result)
    expect((cache / "README.md").read_text() == "two", (cache / "README.md").read_text())


def main() -> int:
    import tempfile

    tests = [
        test_mirrors_versioned_claude_and_codex,
        test_mirrors_marketplace_clone_and_grok_install,
        test_dry_run_does_not_write,
        test_skips_this_clone,
        test_ff_marketplace_clone,
    ]
    failed = 0
    for fn in tests:
        try:
            with tempfile.TemporaryDirectory() as tmp:
                fn(Path(tmp))
            print(f"pass {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    print(f"pass {len(tests) - failed} tests" if not failed else f"{failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
