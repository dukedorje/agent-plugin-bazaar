#!/usr/bin/env python3
"""Stage and run a worker without colliding scratchpads.

Unique prompt file per spawn. Empty/missing prompt hard-fails.
Stall (timeout) is infra-red. Packet-only gets the packet, never a slash.
Claude/Codex CLIs take the prompt on stdin and write the result on stdout.

  python3 plugins/intention/scripts/spawn.py stage --packet FILE [--node ID]
  python3 plugins/intention/scripts/spawn.py run --spec FILE
  python3 plugins/intention/scripts/spawn.py consult [--panel] [--shape architecture-review]
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import shutil
import signal
import sys
import time
import uuid
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

OPENAI_KEY_VARS = ("OPENAI_API_KEY",)

SLASH = ("/act", "/intend", "/meta-execute", "/run")

CLAUDE_MODELS = {
    "sonnet-5": "claude-sonnet-5",
    "opus-5": "claude-opus-5",
    "opus-4.8": "claude-opus-4-8",
    "fable-5": "claude-fable-5",
    "fable-5.1": "claude-fable-5-1",
    "claude-sonnet-5": "claude-sonnet-5",
    "claude-opus-5": "claude-opus-5",
    "claude-opus-4-8": "claude-opus-4-8",
    "claude-fable-5": "claude-fable-5",
    "claude-fable-5-1": "claude-fable-5-1",
}

# Shared ladder language: low | medium | high.
# Claude → --effort. Codex → -c model_reasoning_effort="…".
EFFORT = {
    "sonnet-5": "low",
    "opus-5": "medium",
    "opus-4.8": "high",
    "fable-5": "high",
    "fable-5.1": "high",
    "gpt-5.6-sol": "high",
    "gpt-5.6-terra": "low",
}


def atomic_write(path: Path, text: str, allow_empty: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)
    if not path.is_file():
        raise SystemExit(f"write failed: {path}")
    if not allow_empty and path.stat().st_size == 0:
        raise SystemExit(f"prompt write failed or empty: {path}")


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} is not a JSON object")
    return data


def surface_of(packet: dict, override: str | None) -> str:
    if override:
        return override
    raw = packet.get("surface")
    if raw in {"skill-host", "packet-only"}:
        return raw
    return "packet-only"


def interface_of(packet: dict) -> str | None:
    assignee = packet.get("assignee") if isinstance(packet.get("assignee"), dict) else {}
    iface = assignee.get("interface")
    return str(iface) if isinstance(iface, str) and iface else None


def harness_of(packet: dict) -> str:
    assignee = packet.get("assignee") if isinstance(packet.get("assignee"), dict) else {}
    harness = assignee.get("harness")
    return str(harness) if isinstance(harness, str) and harness else "none"


def node_of(packet: dict, override: str | None) -> str:
    if override:
        return override
    return str(packet.get("node_id") or packet.get("id") or "node")


def permission_of(packet: dict) -> str:
    cons = packet.get("constraints") if isinstance(packet.get("constraints"), dict) else {}
    perm = cons.get("permission")
    return str(perm) if isinstance(perm, str) and perm else "write"


def is_consult(packet: dict) -> bool:
    if packet.get("change_id"):
        return False
    if str(packet.get("node_id") or "").startswith("consult"):
        return True
    return str(packet.get("role") or "") == "consultant"


def prompt_body(packet: dict, packet_path: Path, surface: str) -> str:
    blob = json.dumps(packet, indent=2, ensure_ascii=False)
    if is_consult(packet):
        header = (
            "You are giving a SECOND OPINION. This brief is the whole input.\n"
            "Do not look for a plan file. Do not run a host slash command.\n"
            f"Surface: {surface}. Packet file: {packet_path}\n\n"
            "Packet:\n\n"
            f"{blob}\n\n"
        )
        closer = (
            "You are a second-opinion reader. Permission: read.\n"
            "Do not implement. Do not fold. Do not flip any change banner.\n"
            "Do not write openspec/changes/ or reviews that gate act.\n"
            "This is not advise. An opinion does not unblock act.\n"
            "Read constraints.paths if any; otherwise follow the goal.\n"
            "First banner line MUST be exactly one of:\n"
            "> **CONSULT:** agree\n"
            "> **CONSULT:** caution\n"
            "> **CONSULT:** dissent\n"
            "Body: steelman against, one real tradeoff, findings, what is solid.\n"
            "Cite file:line for code claims. Notes in the body, not the verdict.\n"
        )
        return header + closer
    header = (
        "You are executing ONE work node. This file is the whole brief.\n"
        "Do not look for a plan file. Do not run a host slash command.\n"
        f"Surface: {surface}. Packet file: {packet_path}\n\n"
        "Packet:\n\n"
        f"{blob}\n\n"
    )
    if permission_of(packet) == "read":
        closer = (
            "You are a read-only reader. Permission: read.\n"
            "Do not implement. Do not fold. Do not flip the change banner.\n"
            "Work only on constraints.paths (the review file).\n"
            "First banner line after the title MUST be exactly one of:\n"
            "> **ADVISE:** accept\n"
            "> **ADVISE:** send-back\n"
            "Notes belong in the body, not in the verdict.\n"
            "Return a signed result JSON if you can.\n"
        )
    else:
        closer = (
            "Work only on constraints.paths. Edit and stop. The conductor persists.\n"
            "Return a signed result JSON if you can.\n"
        )
    return header + closer


def assert_prompt_ok(text: str, surface: str) -> None:
    if not text.strip():
        raise SystemExit("empty prompt")
    if surface != "skill-host":
        for token in SLASH:
            if token in text:
                raise SystemExit(f"packet-only prompt contains {token}")


def infra_face(summary: str, blocker: str, raw_ref: str) -> dict[str, Any]:
    return {
        "disposition": "infra-red",
        "summary": summary,
        "verify_command": None,
        "verify_exit": None,
        "commit_sha": None,
        "changed_files": [],
        "blockers": [blocker],
        "raw_ref": raw_ref,
    }


def cmd_stage(args: argparse.Namespace) -> int:
    packet_src = args.packet.resolve()
    if not packet_src.is_file() or packet_src.stat().st_size == 0:
        print("packet missing or empty", file=sys.stderr)
        return 2
    packet = load_json(packet_src)
    if not str(packet.get("goal") or "").strip():
        print("packet goal empty", file=sys.stderr)
        return 2
    surface = surface_of(packet, args.surface)
    node = node_of(packet, args.node)
    stamp = f"{int(time.time())}-{os.getpid()}-{uuid.uuid4().hex[:8]}"
    dest = args.root.resolve() / ".spawns" / f"{node}-{stamp}"
    if dest.exists():
        print(f"spawn dir already exists: {dest}", file=sys.stderr)
        return 2
    dest.mkdir(parents=True)
    packet_copy = dest / "packet.json"
    atomic_write(packet_copy, json.dumps(packet, indent=2) + "\n")
    prompt = dest / "prompt.md"
    body = prompt_body(packet, packet_copy, surface)
    assert_prompt_ok(body, surface)
    atomic_write(prompt, body)
    harness = harness_of(packet)
    if harness == "claude":
        adapter = "claude"
    elif harness in {"codex", "openai"}:
        if codex_cli_present():
            adapter = "codex"
        elif openai_api_key():
            adapter = "openai"
        else:
            adapter = "none"
    else:
        adapter = "none"
    spec = {
        "node_id": node,
        "surface": surface,
        "interface": interface_of(packet),
        "harness": harness,
        "packet_file": str(packet_copy),
        "prompt_file": str(prompt),
        "timeout_sec": args.timeout,
        "adapter": adapter,
        "workspace": str(args.root.resolve()),
        "argv": [],
    }
    assignee = packet.get("assignee") if isinstance(packet.get("assignee"), dict) else {}
    if assignee.get("effort"):
        spec["effort"] = assignee["effort"]
    spec_path = dest / "spec.json"
    atomic_write(spec_path, json.dumps(spec, indent=2) + "\n")
    print(json.dumps({**spec, "dir": str(dest), "spec_file": str(spec_path)}, indent=2))
    return 0


def effort_of(spec: dict) -> str:
    interface = str(spec.get("interface") or "")
    raw = spec.get("effort") or EFFORT.get(interface) or "medium"
    return str(raw)


def claude_argv(spec: dict, prompt_file: Path) -> list[str]:
    """claude -p. Prompt is stdin, not argv (ARG_MAX)."""
    del prompt_file  # consumed by cmd_run via stdin
    interface = str(spec.get("interface") or "sonnet-5")
    model = CLAUDE_MODELS.get(interface, interface)
    effort = effort_of(spec)
    binary = os.environ.get("CLAUDE_BIN", "claude")
    argv = [
        binary,
        "-p",
        "--model",
        model,
        "--effort",
        effort,
        "--output-format",
        "json",
        "--permission-mode",
        "bypassPermissions",
        "--allowedTools",
        "Read,Write,Edit,Bash,Grep,Glob",
        "--no-session-persistence",
    ]
    if spec.get("surface") != "skill-host":
        argv.append("--disable-slash-commands")
    return argv


def codex_bin() -> str:
    return os.environ.get("CODEX_BIN", "codex")


def codex_cli_present() -> bool:
    return shutil.which(codex_bin()) is not None


def codex_argv(spec: dict, prompt_file: Path) -> list[str]:
    """codex exec -. Prompt is stdin (`-`), not argv (ARG_MAX)."""
    interface = str(spec.get("interface") or "gpt-5.6-sol")
    workspace = str(spec.get("workspace") or Path.cwd())
    sandbox = "read-only" if spec.get("surface") == "packet-only" else "workspace-write"
    last = prompt_file.parent / "last.md"
    effort = effort_of(spec)
    return [
        codex_bin(),
        "exec",
        "--skip-git-repo-check",
        "--ephemeral",
        "--color",
        "never",
        "--sandbox",
        sandbox,
        "-C",
        workspace,
        "-m",
        interface,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "--output-last-message",
        str(last),
        "-",
    ]


def openai_api_key() -> str | None:
    for name in OPENAI_KEY_VARS:
        val = (os.environ.get(name) or "").strip()
        if val:
            return val
    return None


def openai_headers(key: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    org = (os.environ.get("OPENAI_ORG") or os.environ.get("OPENAI_ORGANIZATION") or "").strip()
    if org:
        headers["OpenAI-Organization"] = org
    return headers


def openai_chat(model: str, prompt: str, timeout_sec: float | None) -> tuple[int, str]:
    """POST /v1/chat/completions. Returns (http_status, body_text). Never logs the key."""
    key = openai_api_key()
    if not key:
        return 0, "OPENAI_API_KEY not set"
    base = (os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com").rstrip("/")
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a read-only architecture reader. Permission: read. "
                        "Do not implement. Do not fold. Put the ADVISE verdict first."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        base + "/v1/chat/completions",
        data=body,
        method="POST",
        headers=openai_headers(key),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec or 120) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")
    except OSError as exc:
        return 0, str(exc)


def run_openai(spec: dict, prompt_file: Path, raw_path: Path, face_path: Path) -> int:
    prompt = read_prompt(prompt_file)
    model = str(spec.get("interface") or "gpt-5.6-sol")
    timeout = spec.get("timeout_sec")
    try:
        timeout_sec = float(timeout) if timeout is not None else 120.0
    except (TypeError, ValueError):
        timeout_sec = 120.0
    status, raw = openai_chat(model, prompt, timeout_sec)
    atomic_write(raw_path, raw, allow_empty=True)
    content = ""
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            choices = parsed.get("choices") or []
            if choices and isinstance(choices[0], dict):
                msg = choices[0].get("message") or {}
                if isinstance(msg, dict):
                    content = str(msg.get("content") or "")
    except json.JSONDecodeError:
        parsed = None
    if status == 200 and content.strip():
        face = {
            "disposition": "pass",
            "summary": content.strip()[:500],
            "verify_command": f"openai:{model}",
            "verify_exit": 0,
            "commit_sha": None,
            "changed_files": [],
            "blockers": [],
            "raw_ref": str(raw_path),
        }
    else:
        blocker = "openai-key-missing" if status == 0 and "not set" in raw else f"openai-http-{status}"
        face = infra_face(
            f"OpenAI API {model} failed (status {status}).",
            blocker,
            str(raw_path),
        )
    atomic_write(face_path, json.dumps(face, indent=2) + "\n")
    print(json.dumps(face, indent=2))
    return 0


def read_prompt(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"missing prompt file: {path}")
    if path.stat().st_size == 0:
        raise SystemExit(f"empty prompt file: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise SystemExit(f"empty prompt file: {path}")
    return text


def _json_result_text(parsed: Any) -> str:
    if isinstance(parsed, str) and parsed.strip():
        return parsed.strip()
    if isinstance(parsed, dict):
        for key in ("result", "content", "text", "message"):
            val = parsed.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
            if isinstance(val, dict):
                inner = val.get("content") or val.get("text")
                if isinstance(inner, str) and inner.strip():
                    return inner.strip()
        choices = parsed.get("choices")
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            msg = choices[0].get("message") or {}
            if isinstance(msg, dict):
                content = msg.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()
    if isinstance(parsed, list):
        for item in reversed(parsed):
            text = _json_result_text(item)
            if text:
                return text
    return ""


def harvest_text(dest: Path, raw: str) -> str:
    last = dest / "last.md"
    if last.is_file() and last.stat().st_size > 0:
        text = last.read_text(encoding="utf-8").strip()
        if text:
            return text
    raw = (raw or "").strip()
    if not raw:
        return ""
    blobs = [raw]
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    if lines and lines[-1] != raw:
        blobs.append(lines[-1])
    for blob in blobs:
        try:
            parsed = json.loads(blob)
        except json.JSONDecodeError:
            continue
        text = _json_result_text(parsed)
        if text:
            return text
    return raw


CONSULT_VERDICTS = ("agree", "caution", "dissent")


def parse_consult_verdict(text: str) -> str:
    for line in (text or "").splitlines():
        low = line.lower()
        if "consult:" not in low:
            continue
        for verdict in CONSULT_VERDICTS:
            if verdict in low:
                return verdict
    return "unknown"


def adapter_for_harness(harness: str) -> str:
    if harness == "claude":
        return "claude"
    if harness in {"codex", "openai"}:
        if codex_cli_present():
            return "codex"
        if openai_api_key():
            return "openai"
        return "none"
    return "none"


def consult_agent_id(route: dict) -> str:
    raw = str(route.get("id") or route.get("interface") or "reader")
    slug = []
    prev_dash = False
    for ch in raw.lower():
        if ch.isalnum():
            slug.append(ch)
            prev_dash = False
        elif not prev_dash:
            slug.append("-")
            prev_dash = True
    cleaned = "".join(slug).strip("-") or "reader"
    return "agt-" + cleaned[:80]


def consult_packet(goal: str, route: dict, paths: list[str]) -> dict[str, Any]:
    harness = str(route.get("harness") or "none")
    interface = str(route.get("interface") or "")
    aid = consult_agent_id(route)
    shapes = route.get("shapes") or []
    rigor = "architecture" if "architecture-review" in shapes else "brief"
    packet: dict[str, Any] = {
        "id": f"pkt-consult-{uuid.uuid4().hex[:8]}",
        "node_id": "consult",
        "goal": goal.strip(),
        "assignee": {
            "id": aid,
            "kind": "model",
            "harness": harness,
            "interface": interface,
            "signing": {"mode": "stand-in", "stand_in_id": aid},
        },
        "requester": {
            "id": "agt-conductor",
            "kind": "group",
            "harness": "none",
            "signing": {"mode": "stand-in", "stand_in_id": "agt-conductor"},
        },
        "constraints": {
            "permission": "read",
            "paths": list(paths),
            "do_not": ["fold", "act", "deploy", "implement", "advise"],
        },
        "acceptance": {"kind": "none"},
        "load_class": "structure-clear",
        "rigor": rigor,
        "density": str(route.get("density") or "lean"),
        "surface": "packet-only",
        "role": "consultant",
    }
    if route.get("effort"):
        packet["assignee"]["effort"] = route["effort"]
    return packet


def cmd_run(args: argparse.Namespace) -> int:
    spec = load_json(args.spec.resolve())
    prompt_file = Path(str(spec.get("prompt_file") or ""))
    try:
        read_prompt(prompt_file)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2

    dest = prompt_file.parent
    raw_path = dest / "raw.txt"
    face_path = dest / "face.json"
    timeout = spec.get("timeout_sec")
    try:
        timeout_sec = float(timeout) if timeout is not None else None
    except (TypeError, ValueError):
        timeout_sec = None

    adapter = args.adapter or spec.get("adapter") or "none"
    argv = list(args.argv or spec.get("argv") or [])
    stdin_text: str | None = None
    if adapter == "claude":
        argv = claude_argv(spec, prompt_file)
        stdin_text = read_prompt(prompt_file)
    if adapter == "codex":
        argv = codex_argv(spec, prompt_file)
        stdin_text = read_prompt(prompt_file)
    if adapter == "openai":
        return run_openai(spec, prompt_file, raw_path, face_path)
    if adapter == "none" and not argv:
        face = infra_face(
            "No adapter configured. Spec is ready for a packet-only host.",
            "adapter-none",
            str(raw_path),
        )
        atomic_write(raw_path, "not launched\n", allow_empty=True)
        atomic_write(face_path, json.dumps(face, indent=2) + "\n")
        print(json.dumps(face, indent=2))
        return 0

    if adapter not in {"exec", "claude", "codex", "openai", "none"}:
        print(f"unknown adapter: {adapter}", file=sys.stderr)
        return 2
    if not argv:
        print("adapter requires argv", file=sys.stderr)
        return 2

    env = os.environ.copy()
    env["SPAWN_PROMPT_FILE"] = str(prompt_file)
    env["SPAWN_PACKET_FILE"] = str(spec.get("packet_file") or "")
    workspace = str(spec.get("workspace") or dest)

    import subprocess

    try:
        proc = subprocess.Popen(
            argv,
            cwd=workspace,
            env=env,
            stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            start_new_session=True,
        )
    except OSError as exc:
        face = infra_face(f"adapter failed to start: {exc}", "infra-start", str(raw_path))
        atomic_write(raw_path, str(exc) + "\n")
        atomic_write(face_path, json.dumps(face, indent=2) + "\n")
        print(json.dumps(face, indent=2))
        return 0

    try:
        out, _ = proc.communicate(input=stdin_text, timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError, OSError):
            proc.kill()
        try:
            out, _ = proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                proc.kill()
            out, _ = proc.communicate()
        raw = (out or "") + "\n[stall: timeout_sec={timeout}]\n".format(timeout=timeout_sec)
        atomic_write(raw_path, raw, allow_empty=True)
        face = infra_face(
            f"Worker stalled after {timeout_sec}s. Not a code failure.",
            "stall",
            str(raw_path),
        )
        atomic_write(face_path, json.dumps(face, indent=2) + "\n")
        print(json.dumps(face, indent=2))
        return 0

    atomic_write(raw_path, out or "", allow_empty=True)
    harvested = harvest_text(dest, out or "")
    face = {
        "disposition": "pass" if proc.returncode == 0 else "infra-red",
        "summary": (harvested[:500] if harvested else "adapter exited"),
        "verify_command": " ".join(argv),
        "verify_exit": proc.returncode,
        "commit_sha": None,
        "changed_files": [],
        "blockers": [] if proc.returncode == 0 else [f"adapter-exit-{proc.returncode}"],
        "raw_ref": str(raw_path),
    }
    atomic_write(face_path, json.dumps(face, indent=2) + "\n")
    print(json.dumps(face, indent=2))
    return 0


def consult_goal(args: argparse.Namespace) -> str:
    if args.goal:
        return str(args.goal).strip()
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read().strip()


def consult_routes(args: argparse.Namespace) -> list[dict[str, Any]]:
    scripts = Path(__file__).resolve().parent
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import ladder as ladder_mod  # noqa: WPS433

    data = ladder_mod.load()
    who = ladder_mod.parse_who(getattr(args, "who", None))
    picked = sum(bool(x) for x in (who, args.panel, args.route_id))
    if picked > 1:
        raise SystemExit("--who, --panel, and --id are mutually exclusive")
    if args.after and (who or args.panel):
        raise SystemExit("--after does not combine with --who or --panel")

    def spawnable_of(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        yes = [r for r in rows if adapter_for_harness(str(r.get("harness") or "")) != "none"]
        no = [r for r in rows if adapter_for_harness(str(r.get("harness") or "")) == "none"]
        return yes, no

    if who:
        rows = ladder_mod.resolve_who(
            data,
            args.shape,
            who,
            not_harness=args.not_harness,
            allow_unavailable=True,
        )
        spawnable, skipped = spawnable_of(rows)
        if skipped:
            names = ", ".join(str(r.get("id") or "?") for r in skipped)
            raise SystemExit(f"no adapter for named who ({names})")
        return spawnable

    hits = ladder_mod.candidates(
        data,
        args.shape,
        route_id=args.route_id,
        not_harness=args.not_harness,
        after=args.after,
    )
    spawnable, skipped = spawnable_of(hits)
    if args.route_id:
        if not hits:
            raise SystemExit(f"no route {args.route_id!r} for shape {args.shape!r}")
        if not spawnable:
            harness = str(hits[0].get("harness") or "none")
            raise SystemExit(f"no adapter for {args.route_id} (harness {harness})")
        return spawnable
    if args.panel:
        if not spawnable:
            names = ", ".join(str(r.get("id") or "?") for r in skipped) or "none"
            raise SystemExit(f"no spawnable readers for {args.shape!r} (skipped: {names})")
        return spawnable
    if not spawnable:
        raise SystemExit(f"no spawnable route for shape {args.shape!r}")
    return spawnable[:1]


def capture_json(fn, *a: Any, **kw: Any) -> tuple[int, dict[str, Any] | None, str]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = fn(*a, **kw)
    raw = buf.getvalue()
    try:
        return code, json.loads(raw), raw
    except json.JSONDecodeError:
        return code, None, raw


def cmd_consult(args: argparse.Namespace) -> int:
    goal = consult_goal(args)
    if not goal:
        print("empty consult brief (pipe stdin or pass --goal)", file=sys.stderr)
        return 2
    try:
        routes = consult_routes(args)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2

    root = args.root.resolve()
    paths = list(args.paths or [])
    opinions: list[dict[str, Any]] = []
    for route in routes:
        harness = str(route.get("harness") or "none")
        adapter = adapter_for_harness(harness)
        packet = consult_packet(goal, route, paths)
        dest = root / ".spawns"
        dest.mkdir(parents=True, exist_ok=True)
        pkt_path = dest / f"{packet['id']}.json"
        atomic_write(pkt_path, json.dumps(packet, indent=2) + "\n")
        staged, spec, _ = capture_json(
            cmd_stage,
            argparse.Namespace(
                packet=pkt_path,
                node="consult",
                surface="packet-only",
                timeout=args.timeout,
                root=root,
            ),
        )
        if staged != 0 or not spec or not spec.get("spec_file"):
            opinions.append(
                {
                    "id": route.get("id"),
                    "harness": harness,
                    "interface": route.get("interface"),
                    "disposition": "infra-red",
                    "verdict": "unknown",
                    "body": "stage failed",
                    "blockers": ["consult-stage"],
                }
            )
            continue
        spec_path = Path(str(spec["spec_file"]))
        code, face, raw_out = capture_json(
            cmd_run,
            argparse.Namespace(spec=spec_path, adapter=adapter, argv=None),
        )
        if face is None:
            face = infra_face("consult run did not return a face", "consult-run", "")
        dest_dir = spec_path.parent
        raw_file = dest_dir / "raw.txt"
        raw_text = raw_file.read_text(encoding="utf-8") if raw_file.is_file() else raw_out
        body = harvest_text(dest_dir, raw_text)
        if not body:
            body = str(face.get("summary") or "")
        opinions.append(
            {
                "id": route.get("id"),
                "harness": harness,
                "interface": route.get("interface"),
                "adapter": adapter,
                "disposition": face.get("disposition"),
                "verdict": parse_consult_verdict(body),
                "body": body,
                "raw_ref": face.get("raw_ref"),
                "blockers": face.get("blockers") or [],
                "exit": code,
            }
        )

    print(json.dumps({"shape": args.shape, "panel": bool(args.panel), "opinions": opinions}, indent=2))
    if not opinions:
        return 2
    return 0


def main() -> int:
    repo = Path(__file__).resolve().parents[3]
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    stage = sub.add_parser("stage", help="write a unique prompt file")
    stage.add_argument("--packet", type=Path, required=True)
    stage.add_argument("--node")
    stage.add_argument("--surface", choices=["skill-host", "packet-only"])
    stage.add_argument("--timeout", type=float, default=300)
    stage.add_argument("--root", type=Path, default=repo)
    stage.set_defaults(func=cmd_stage)

    run = sub.add_parser("run", help="run a staged spec")
    run.add_argument("--spec", type=Path, required=True)
    run.add_argument("--adapter")
    run.add_argument("--argv", nargs=argparse.REMAINDER)
    run.set_defaults(func=cmd_run)

    consult = sub.add_parser("consult", help="second opinion from ladder readers (no intend node)")
    consult.add_argument("--shape", default="architecture-review")
    consult.add_argument("--id", dest="route_id", help="exact ladder route id")
    consult.add_argument(
        "--who",
        action="append",
        help="nickname or id; comma list or repeatable (several). Not with --panel/--id",
    )
    consult.add_argument("--after", help="handoff: next spawnable route after this id")
    consult.add_argument("--not-harness", dest="not_harness", help="skip this harness (ADR-005)")
    consult.add_argument("--panel", action="store_true", help="every spawnable reader for the shape")
    consult.add_argument("--goal", help="brief; stdin is appended when piped")
    consult.add_argument("--paths", nargs="*", default=[], help="paths the reader should look at")
    consult.add_argument("--timeout", type=float, default=300)
    consult.add_argument("--root", type=Path, default=repo)
    consult.set_defaults(func=cmd_consult)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
