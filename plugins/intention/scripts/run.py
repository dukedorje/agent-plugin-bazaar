#!/usr/bin/env python3
"""Shim: the real script travels with the skill so other repos can find it."""

from __future__ import annotations

import runpy
from pathlib import Path

TARGET = (
    Path(__file__).resolve().parents[1] / "skills" / "run" / "scripts" / "run.py"
)
runpy.run_path(str(TARGET), run_name="__main__")
