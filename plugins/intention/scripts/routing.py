#!/usr/bin/env python3
"""Shared family resolution, permission-aware adapters, passive runtime health."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "references" / "ladder.json"
VENDORS = {"claude": "anthropic", "codex": "openai", "openai": "openai", "grok": "xai"}


def registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def family_of(interface, data=None):
    for family, row in (data or registry()).get("families", {}).items():
        if interface in {family, row["model"], *(row.get("aliases") or [])}:
            return family
    return None


def vendor_of(author, data=None):
    if author in VENDORS:
        return VENDORS[author]
    family = family_of(author, data)
    if family:
        return (data or registry())["families"][family]["vendor"]
    if author in VENDORS.values():
        return author
    raise ValueError(f"unknown author family {author!r}; supply a harness, family, or interface")


def model_of(interface, data=None):
    data = data or registry()
    family = family_of(interface, data)
    if not family:
        raise ValueError(f"unconfigured model interface {interface!r}")
    return data["families"][family]["model"]


def adapter_for(harness, permission="write", env=None, which=None):
    env = os.environ if env is None else env
    which = shutil.which if which is None else which
    if harness in {"codex", "openai"}:
        if which(env.get("CODEX_BIN", "codex")):
            return "codex"
        if permission == "read" and (env.get("OPENAI_API_KEY") or "").strip():
            return "openai"
    if harness in {"claude", "grok"} and which(env.get(harness.upper() + "_BIN", harness)):
        return harness
    return "none"


def credential_identity(adapter, env=None):
    """Fingerprint an operator-provided NON-SECRET login id/epoch, never a key.

    Key rotation also updates INTENTION_CREDENTIAL_ID_OPENAI; CLI login changes
    update the corresponding adapter id or explicitly reset runtime health.
    """
    env = os.environ if env is None else env
    public_id = env.get("INTENTION_CREDENTIAL_ID_" + adapter.upper()) or env.get("OPENAI_ORG") or "default-login"
    return hashlib.sha256((adapter + ":" + public_id).encode()).hexdigest()[:24]


class HealthStore:
    def __init__(self, path=None, *, clock=time.time, records=None):
        self.clock, self.path = clock, path
        self.records = records if records is not None else {}
        if path and path.is_file():
            try:
                self.records = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self.records = {}

    @staticmethod
    def key(adapter, model, identity):
        return "|".join((adapter, model, identity))

    def state(self, adapter, model, identity, mapping):
        row = self.records.get(self.key(adapter, model, identity), {})
        if row.get("mapping") != mapping or self.clock() >= row.get("until", 0):
            return "unknown"
        return row.get("state", "unknown")

    def record(self, adapter, model, identity, mapping, outcome):
        if outcome not in {"success", "quota", "auth", "model-not-found", "stall"}:
            return
        key, now = self.key(adapter, model, identity), self.clock()
        row = self.records.get(key, {})
        stalls = [s for s in row.get("stalls", []) if now - s < 900]
        if outcome == "stall":
            stalls.append(now)
            if len(stalls) < 2:
                self.records[key] = {**row, "stalls": stalls}
                self.save()
                return
        ttl = {"success": 3600, "quota": 1800, "auth": 86400, "stall": 900, "model-not-found": 1e30}[outcome]
        self.records[key] = {"state": "verified" if outcome == "success" else "degraded", "until": now + ttl, "mapping": mapping, "reason": outcome, "stalls": stalls if outcome == "stall" else []}
        self.save()

    def reset(self, adapter, model, identity):
        self.records.pop(self.key(adapter, model, identity), None)
        self.save()

    def save(self):
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_name(self.path.name + ".tmp")
            tmp.write_text(json.dumps(self.records), encoding="utf-8")
            tmp.replace(self.path)


def runtime_health():
    path = os.environ.get("INTENTION_HEALTH_FILE")
    root = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return HealthStore(Path(path) if path else root / "intention" / "routing-health.json")


def mapping_token(family):
    return hashlib.sha256(json.dumps(family, sort_keys=True).encode()).hexdigest()[:24]


def resolve(route, data, permission="write", *, store=None, env=None, which=None):
    row = dict(route)
    family = data.get("families", {}).get(row.get("family"), {})
    configured = bool(row.get("enabled", True) and family.get("model"))
    if "architecture-review" in (row.get("shapes") or []) and row.get("family") not in {"opus", "astra", "grok"}:
        configured = False
    if row.get("model") and row["model"] != family.get("model") and not row.get("pin_reason"):
        configured = False
    model = row.get("model") or family.get("model")
    adapter = adapter_for(str(row.get("harness") or ""), permission, env, which)
    identity, mapping = credential_identity(adapter, env), mapping_token(family)
    row.update(interface=model, configured=configured, executable=configured and adapter != "none", adapter=adapter, vendor=family.get("vendor"), health=(store or runtime_health()).state(adapter, model or "", identity, mapping), credential_identity=identity, mapping=mapping)
    row["available"] = row["executable"]  # one-release output compatibility
    return row


def infra_outcome(text, *, status=None, success=False):
    low = text.lower()
    if status in {401, 403} or any(s in low for s in ("invalid api key", "authentication failed", "unauthorized", "not logged in")):
        return "auth"
    if status == 429 or any(s in low for s in ("quota", "rate limit", "credit balance is too low", "usage limit")):
        return "quota"
    if any(s in low for s in ("model_not_found", "model not found", "unknown model", "model does not exist")):
        return "model-not-found"
    return "success" if success else None


def record_execution(spec, adapter, outcome, *, store=None, env=None):
    if adapter not in {"claude", "codex", "openai", "grok"} or not outcome:
        return
    data = registry()
    family = family_of(str(spec.get("interface") or ""), data)
    if family:
        row = data["families"][family]
        (store or runtime_health()).record(adapter, row["model"], credential_identity(adapter, env), mapping_token(row), outcome)
