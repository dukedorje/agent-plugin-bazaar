#!/usr/bin/env python3
"""Stand-in content hash for a signed result.

Reads a result JSON, sets signature.content_hash to sha256 of the
canonical payload (signature.content_hash and signature.bytes removed),
writes the file back unless --check (then exit 1 if mismatch).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def payload(data: dict) -> dict:
    out = json.loads(json.dumps(data))
    sig = out.get("signature")
    if isinstance(sig, dict):
        sig.pop("content_hash", None)
        sig.pop("bytes", None)
    return out


def digest(data: dict) -> str:
    blob = json.dumps(payload(data), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("result", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    data = json.loads(args.result.read_text(encoding="utf-8"))
    got = digest(data)
    have = (data.get("signature") or {}).get("content_hash")
    if args.check:
        if have != got:
            print(f"mismatch have={have} want={got}")
            return 1
        print(got)
        return 0
    data.setdefault("signature", {})["content_hash"] = got
    args.result.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(got)
    return 0


if __name__ == "__main__":
    sys.exit(main())
