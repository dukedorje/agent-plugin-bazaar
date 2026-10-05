#!/usr/bin/env python3
"""Focused, offline routing/health contract checks with injectable dependencies."""
import copy
import json
import tempfile
from pathlib import Path

import ladder
import routing


def expect(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    now = [10000.0]
    health = routing.HealthStore(clock=lambda: now[0])
    raw = routing.registry()
    env = {"OPENAI_API_KEY": "secret-never-persist", "INTENTION_CREDENTIAL_ID_OPENAI": "account-a"}
    def load(permission="write", which=lambda _: "/stub", env=env):
        return ladder.apply_env(copy.deepcopy(raw), permission, store=health, env=env, which=which)
    data = load()
    orders = {"known": ["sonnet-known", "terra-known"], "implementation": ["sol-implement", "opus-implement"], "thinking": ["sol-implement", "opus-implement"], "design": ["opus-design"], "plan": ["opus-plan", "astra-plan"], "replan": ["opus-plan", "astra-plan"], "intend-consult": ["opus-plan", "astra-plan"], "fold": ["opus-fold"], "architecture-review": ["opus-arch-review", "astra-arch-review", "grok-arch-review"]}
    for shape, expected in orders.items():
        expect([r["id"] for r in ladder.candidates(data, shape)] == expected, shape)
        expect(ladder.assign(data, shape)["health"] == "unknown", shape)
    expect(ladder.assign(data, "architecture-review")["effort"] == "high", "Opus high")
    expect(ladder.assign(data, "architecture-review", author_family="opus")["id"] == "astra-arch-review", "Claude author")
    expect(ladder.assign(data, "architecture-review", author_family="codex")["id"] == "opus-arch-review", "Codex author")
    no_codex = load(which=lambda binary: None if binary == "codex" else "/stub", env={})
    expect(ladder.assign(no_codex, "architecture-review", author_family="claude")["id"] == "grok-arch-review", "Claude author fallback")
    expect(ladder.assign(data, "architecture-review", route_id="opus-4.8-arch-review", author_family="opus")["id"] == "opus-arch-review", "explicit migration override")
    for alias, target in raw["migration_aliases"].items():
        route = next(r for r in data["routes"] if r["id"] == target)
        expect(ladder.assign(data, route["shapes"][0], route_id=alias)["id"] == target, alias)
    expect(ladder.assign(data, "known", after="sonnet-5")["id"] == "terra-known", "alias after")
    expect(ladder.resolve_who(data, "plan", ["astra", "opus"])[0]["id"] == "opus-plan", "shape nicknames preserve priority")
    for name in ("sol", "terra", "fable"):
        try:
            ladder.resolve_who(data, "architecture-review", [name])
        except SystemExit:
            pass
        else:
            raise AssertionError("forbidden architecture nickname " + name)
    expect(all("verified_at" in f for f in raw["families"].values()), "verification dates")
    expect(routing.model_of("opus-4.8") == raw["families"]["opus"]["model"], "launcher interface alias")
    expect(routing.model_of("grok") == "grok-4.7", "Grok concrete model")
    expect(all(r["family"] != "fable" for r in raw["routes"]), "no retired live family")
    bad = {"id": "bad", "family": "sol", "harness": "codex", "shapes": ["architecture-review"]}
    expect(not routing.resolve(bad, raw, store=health, which=lambda _: "/stub")["configured"], "policy validation")
    pinned = {"id": "pin", "family": "opus", "model": "older", "harness": "claude"}
    expect(not routing.resolve(pinned, raw, store=health)["configured"], "old model requires reason")
    pinned["pin_reason"] = "controlled comparison"
    expect(routing.resolve(pinned, raw, store=health)["configured"], "documented pin")
    read_only = load("read", which=lambda _: None)
    write_only = load("write", which=lambda _: None)
    astra = next(r for r in read_only["routes"] if r["id"] == "astra-arch-review")
    sol = next(r for r in write_only["routes"] if r["id"] == "sol-implement")
    expect(astra["configured"] and astra["executable"] and astra["adapter"] == "openai", "API read")
    expect(sol["configured"] and not sol["executable"], "API write refused")
    first = ladder.assign(data, "architecture-review")
    args = (first["adapter"], first["interface"], first["credential_identity"], first["mapping"])
    health.record(*args, "success")
    expect(health.state(*args) == "verified", "success")
    now[0] += 3600
    expect(health.state(*args) == "unknown", "success TTL")
    for outcome, ttl in (("quota", 1800), ("auth", 86400)):
        health.record(*args, outcome)
        expect(health.state(*args) == "degraded", outcome)
        if outcome == "auth":
            expect(health.state(args[0], args[1], "new-identity", args[3]) == "unknown", "auth identity reset")
        health.record(*args, "task-red")
        health.record(*args, "baseline-red")
        expect(health.state(*args) == "degraded", "task evidence ignored")
        now[0] += ttl
        expect(health.state(*args) == "unknown", outcome + " TTL")
    health.record(*args, "model-not-found")
    now[0] += 864000
    expect(health.state(*args) == "degraded", "model failure persists")
    expect(health.state(*args[:3], "registry-changed") == "unknown", "registry reset")
    health.reset(*args[:3])
    health.record(*args, "stall")
    expect(health.state(*args) == "unknown", "one stall")
    now[0] += 899
    health.record(*args, "stall")
    expect(health.state(*args) == "degraded", "two stalls")
    now[0] += 900
    expect(health.state(*args) == "unknown", "stall TTL")
    health.reset(*args[:3])
    health.record(*args, "stall")
    now[0] += 901
    health.record(*args, "stall")
    expect(health.state(*args) == "unknown", "separated stalls")
    health.record(*args, "quota")
    current = load()
    expect(ladder.assign(current, "architecture-review")["id"] == "astra-arch-review", "skip degraded in priority")
    explicit = ladder.assign(current, "architecture-review", route_id="opus-arch-review")
    expect(explicit["id"] == "opus-arch-review" and explicit["warnings"], "human health override")
    expect(ladder.resolve_who(current, "architecture-review", ["opus"])[0]["warnings"], "human nickname warning")
    try:
        ladder.assign(current, "architecture-review", after="astra-arch-review", fallback_hops=2)
    except SystemExit:
        pass
    else:
        raise AssertionError("third fallback accepted")
    expect(ladder.assign(current, "architecture-review", after="astra-arch-review", fallback_hops=1)["id"] == "grok-arch-review", "second fallback allowed")
    ident = routing.credential_identity("openai", env)
    expect(ident == routing.credential_identity("openai", {**env, "OPENAI_API_KEY": "rotated-secret"}), "identity never derives from key")
    expect(ident != routing.credential_identity("openai", {**env, "INTENTION_CREDENTIAL_ID_OPENAI": "account-b"}), "nonsecret identity epoch")
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "health.json"
        stored = routing.HealthStore(path, clock=lambda: now[0])
        stored.record("openai", "model", ident, "mapping", "auth")
        expect("secret" not in path.read_text(), "no secret in health store")
        expect(routing.HealthStore(path, clock=lambda: now[0]).state("openai", "model", ident, "mapping") == "degraded", "scratch persistence")
    print("pass approved routes, aliases, permission, cross-family review, priority, two-hop bound, TTLs and nonsecret scratch health")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
