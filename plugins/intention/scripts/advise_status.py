"""Loader — canonical module is skills/status/scripts/advise_status.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SRC = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "status"
    / "scripts"
    / "advise_status.py"
)
_spec = importlib.util.spec_from_file_location("ready_advise_status", _SRC)
if _spec is None or _spec.loader is None:
    raise ImportError(f"missing {_SRC}")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

change_rigor = _mod.change_rigor
last_advise_verdict = _mod.last_advise_verdict
needs_advise = _mod.needs_advise
needs_advise_ids = _mod.needs_advise_ids
write_node_blocked = _mod.write_node_blocked
