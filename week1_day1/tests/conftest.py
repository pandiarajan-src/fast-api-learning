"""Pytest configuration to ensure project root is on sys.path for imports.

This makes `import week1_day1...` work regardless of the working directory
or pytest import mode.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Repo root: <repo> / week1_day1 / tests / this_file
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
