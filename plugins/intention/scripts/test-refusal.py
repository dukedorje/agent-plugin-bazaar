#!/usr/bin/env python3
"""Focused verify: refusal.py card for the relay specimen."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REF = Path(__file__).resolve().parents[1] / "skills" / "status" / "scripts" / "refusal.py"


def bead(i, title, labels=(), desc="", deps=(), typ="task", status="open"):
    return {"id": i, "title": title, "labels": list(labels), "description": desc,
            "issue_type": typ, "status": status,
            "dependencies": [{"depends_on_id": d, "type": t} for d, t in deps]}


def specimen() -> list[dict]:
    rows = [bead("gwk", "guild work", deps=[("o1", "blocks"), ("o2", "blocks"), ("o3", "blocks"),
                                            ("o4", "blocks"), ("g1", "blocks"), ("i1", "blocks"),
                                            ("d1", "related")])]
    for n, (proj, cap) in enumerate([("identikey-protocol", "guild-holder"), ("Tokenator", "mint"),
                                     ("Mjolnir", "sign"), ("IKEYW", "wallet")], 1):
        rows.append(bead(f"o{n}", f"{proj} owes {cap}", ["outside"],
                         f"project: {proj}\nexternal: external:{proj}:{cap}\nblocks: live-execute"
                         + ("\nupstream: ik-123" if n == 1 else "")))
    rows.append(bead(
        "g1", "Gate: human", typ="gate",
        desc="Ad-hoc gate blocking gwk\n\nReason: independent security review",
    ))
    rows.append(bead("i1", "internal lock", ["internal"]))
    rows.append(bead("d1", "later thing", ["deferred"]))
    return rows


def run(path, *args):
    return subprocess.run([sys.executable, str(REF), "gwk", "--export", str(path), *args],
                          text=True, capture_output=True, check=True).stdout


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "e.jsonl"
        p.write_text("\n".join(json.dumps(r) for r in specimen()))
        out = run(p, "--action", "live-execute")
        for want in ("identikey-protocol", "Tokenator", "Mjolnir", "IKEYW", "o1 · external:Tokenator" if False else "o2 · external:Tokenator:mint",
                     "upstream: ik-123", "Review\n- g1 · independent security review",
                     "internal · i1", "deferred · d1", "does not unlock live-execute"):
            assert want in out, (want, out)
        assert out == run(p, "--action", "live-execute")
        flip = run(p, "--action", "banner-flip")
        assert "Outside" not in flip and "outside · o1" in flip, flip
        gone = subprocess.run([sys.executable, str(REF), "gwk", "--export", str(Path(td) / "none")],
                              text=True, capture_output=True, check=True).stdout
        assert gone.strip() == "Could not read beads for gwk.", gone
        miss = run(p).replace("gwk", "gwk")
        q = Path(td) / "q.jsonl"
        q.write_text(json.dumps(bead("x", "t")))
        assert "Could not read" in run(q)
        q.write_text(json.dumps(bead("gwk", "t")))
        assert run(q).strip() == "No outside wait recorded for gwk."
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
