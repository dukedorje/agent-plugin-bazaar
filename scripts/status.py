#!/usr/bin/env python3
"""Shim: the real script travels with the status skill."""

from __future__ import annotations

import runpy
from pathlib import Path

TARGET = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "intention"
    / "skills"
    / "status"
    / "scripts"
    / "status.py"
)
runpy.run_path(str(TARGET), run_name="__main__")
