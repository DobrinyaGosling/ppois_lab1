"""Pytest configuration ensuring local packages are importable.

This makes `multitude` and `turing_machine` available when running plain
`pytest` without installing the project as a package.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

