#!/usr/bin/env python3
"""Refresh harness plugin copies from this clone's plugins/ tree.

Claude, Grok, and Codex cache plugins by version or git SHA. Pushing
main does not recopy those dirs. After a commit/merge/checkout of
main, this script mirrors plugins/<name> into every bazaar cache it
finds under $HOME. Missing harnesses are skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

MARKETPLACE_ID = "agent-plugin-bazaar"
PROTECTED = {".in_use", ".git", ".omc", ".spawns"}
IGNORE = {"__pycache__", ".git", ".omc", ".spawns", ".dolt", "node_modules"}


def repo_root_from(start: Path) -> Path:
    here = start.resolve()
    if (here / ".claude-plugin" / "marketplace.json").is_file():
        return here
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=here,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return Path(proc.stdout.strip())
    raise SystemExit("not in agent-plugin-bazaar")


def plugin_names(repo: Path) -> list[str]:
    data = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text())
    names = [str(p["name"]) for p in data.get("plugins") or [] if p.get("name")]
    grok = repo / ".grok-plugin" / "marketplace.json"
    if grok.is_file():
        gdata = json.loads(grok.read_text())
        for p in gdata.get("plugins") or []:
            name = p.get("name")
            if name and name not in names:
                names.append(str(name))
    return names


def looks_like_plugin_root(path: Path, name: str) -> bool:
    if not path.is_dir():
        return False
    for manifest in (
        path / ".claude-plugin" / "plugin.json",
        path / ".codex-plugin" / "plugin.json",
        path / ".grok-plugin" / "plugin.json",
        path / "plugin.json",
    ):
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text())
        except json.JSONDecodeError:
            continue
        if data.get("name") == name:
            return True
    return (path / "skills").is_dir() and path.name == name


def looks_like_marketplace_root(path: Path) -> bool:
    return (path / "plugins").is_dir() and (
        (path / ".claude-plugin" / "marketplace.json").is_file()
        or (path / ".grok-plugin" / "marketplace.json").is_file()
        or (path / ".agents" / "plugins" / "marketplace.json").is_file()
    )


def mirror_tree(src: Path, dest: Path) -> bool:
    """Copy src onto dest. Keep PROTECTED names on dest. Return True if dest existed or was created."""
    if not src.is_dir():
        return False
    dest.mkdir(parents=True, exist_ok=True)
    for child in list(dest.iterdir()):
        if child.name in PROTECTED or child.name in IGNORE:
            continue
        if not (src / child.name).exists():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    for child in src.iterdir():
        if child.name in IGNORE or child.name in PROTECTED:
            continue
        target = dest / child.name
        if child.is_dir():
            mirror_tree(child, target)
        else:
            shutil.copy2(child, target)
    return True


def git_ff_main(path: Path, source_repo: Path) -> str | None:
    git_dir = path / ".git"
    if not git_dir.exists():
        return None
    if path.resolve() == source_repo.resolve():
        return None
    ident = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    url = (ident.stdout or "").strip().lower()
    if MARKETPLACE_ID not in url and "agent-plugin-bazaar" not in url:
        return None
    fetch = subprocess.run(
        ["git", "fetch", "--quiet", "origin"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        return f"fetch-fail {path}"
    subprocess.run(
        ["git", "checkout", "--quiet", "main"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    pull = subprocess.run(
        ["git", "merge", "--ff-only", "--quiet", "origin/main"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    if pull.returncode != 0:
        return f"ff-fail {path}"
    return f"ff {path}"


def grok_registry_roots(home: Path) -> list[Path]:
    registry = home / ".grok" / "installed-plugins" / "registry.json"
    if not registry.is_file():
        return []
    try:
        data = json.loads(registry.read_text())
    except json.JSONDecodeError:
        return []
    out: list[Path] = []
    for rec in (data.get("repos") or {}).values():
        if not isinstance(rec, dict):
            continue
        path = rec.get("path")
        if path:
            out.append(Path(path))
        kind = rec.get("kind") or {}
        src = kind.get("source_path") or kind.get("url") or ""
        if MARKETPLACE_ID in str(src).lower() or "agent-plugin-bazaar" in str(src).lower():
            if path:
                out.append(Path(path))
        mp = rec.get("marketplace") or {}
        url = str(mp.get("source_url_or_path") or "")
        if MARKETPLACE_ID in url.lower() and path:
            out.append(Path(path))
    # unique, keep order
    seen: set[Path] = set()
    uniq: list[Path] = []
    for p in out:
        r = p.resolve() if p.exists() else p
        if r not in seen:
            seen.add(r)
            uniq.append(p)
    return uniq


def cache_roots(home: Path) -> list[Path]:
    roots = [
        home / ".claude" / "plugins" / "cache" / MARKETPLACE_ID,
        home / ".claude" / "plugins" / "marketplaces" / MARKETPLACE_ID,
        home / ".codex" / "plugins" / "cache" / MARKETPLACE_ID,
        home / ".codex" / ".tmp" / "marketplaces" / MARKETPLACE_ID,
    ]
    mp_cache = home / ".grok" / "marketplace-cache"
    if mp_cache.is_dir():
        roots.extend(p for p in mp_cache.iterdir() if p.is_dir())
    installed = home / ".grok" / "installed-plugins"
    if installed.is_dir():
        roots.extend(p for p in installed.iterdir() if p.is_dir())
    roots.extend(grok_registry_roots(home))
    seen: set[Path] = set()
    out: list[Path] = []
    for p in roots:
        if not p.exists():
            continue
        r = p.resolve()
        if r in seen:
            continue
        seen.add(r)
        out.append(p)
    return out


def destinations_for(name: str, src: Path, roots: list[Path]) -> list[Path]:
    dests: list[Path] = []
    for root in roots:
        if looks_like_plugin_root(root, name):
            dests.append(root)
            continue
        if looks_like_marketplace_root(root):
            dests.append(root / "plugins" / name)
            continue
        plugin_dir = root / name
        if plugin_dir.is_dir():
            # versioned cache: cache/<marketplace>/<name>/<version>/
            versions = [
                p
                for p in plugin_dir.iterdir()
                if p.is_dir() and not p.name.startswith(".")
            ]
            if versions and any(looks_like_plugin_root(p, name) for p in versions):
                dests.extend(p for p in versions if looks_like_plugin_root(p, name) or (p / "skills").is_dir())
            elif looks_like_plugin_root(plugin_dir, name):
                dests.append(plugin_dir)
            else:
                dests.extend(versions or [plugin_dir])
            continue
        nested = root / "plugins" / name
        if nested.is_dir() or (root / "plugins").is_dir():
            dests.append(nested)
    seen: set[Path] = set()
    uniq: list[Path] = []
    for d in dests:
        key = d.resolve() if d.exists() else d
        if key in seen:
            continue
        seen.add(key)
        uniq.append(d)
    return uniq


def run_cli(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return f"skip {' '.join(cmd)}: {(proc.stderr or proc.stdout or '').strip()[:200]}"
    return f"ok {' '.join(cmd)}"


def sync(
    repo: Path,
    home: Path,
    *,
    dry_run: bool = False,
    cli: bool = False,
) -> list[str]:
    names = plugin_names(repo)
    notes: list[str] = []
    roots = cache_roots(home)
    if not dry_run:
        for root in roots:
            ff = git_ff_main(root, repo)
            if ff:
                notes.append(ff)
    for name in names:
        src = repo / "plugins" / name
        if not src.is_dir():
            notes.append(f"skip missing {src}")
            continue
        dests = destinations_for(name, src, roots)
        if not dests:
            notes.append(f"no-cache {name}")
            continue
        for dest in dests:
            if dest.resolve() == src.resolve():
                continue
            if dry_run:
                notes.append(f"would-mirror {name} -> {dest}")
                continue
            mirror_tree(src, dest)
            notes.append(f"mirror {name} -> {dest}")
    if cli and not dry_run:
        for cmd in (
            ["grok", "plugin", "marketplace", "update", MARKETPLACE_ID],
            ["grok", "plugin", "update"],
            ["codex", "plugin", "marketplace", "upgrade"],
        ):
            try:
                notes.append(run_cli(cmd))
            except FileNotFoundError:
                notes.append(f"skip {cmd[0]}: not installed")
    return notes


def install_hooks(repo: Path) -> str:
    subprocess.run(
        ["git", "config", "core.hooksPath", ".githooks"],
        cwd=repo,
        check=True,
    )
    return "core.hooksPath=.githooks"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--home", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cli", action="store_true", help="also call grok/codex update CLIs")
    parser.add_argument("--install-hooks", action="store_true")
    args = parser.parse_args()
    start = Path(args.repo) if args.repo else Path(__file__).resolve().parent.parent
    repo = repo_root_from(start)
    if args.install_hooks:
        print(install_hooks(repo))
    home = Path(args.home) if args.home else Path(os.environ.get("HOME", str(Path.home())))
    if os.environ.get("SYNC_HARNESS_PLUGINS") == "0":
        print("skip SYNC_HARNESS_PLUGINS=0")
        return 0
    notes = sync(repo, home, dry_run=args.dry_run, cli=args.cli)
    for line in notes:
        print(line)
    if not notes:
        print("no harness caches found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
