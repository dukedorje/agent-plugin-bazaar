#!/usr/bin/env python3
"""Shim: the real script travels with the fold skill."""

from __future__ import annotations

import runpy
from pathlib import Path

TARGET = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "fold"
    / "scripts"
    / "fold_base.py"
)
runpy.run_path(str(TARGET), run_name="__main__")
