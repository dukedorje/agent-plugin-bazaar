#!/usr/bin/env python3
"""Shim: observe script is status.py in this directory."""

from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "status.py"), run_name="__main__")
