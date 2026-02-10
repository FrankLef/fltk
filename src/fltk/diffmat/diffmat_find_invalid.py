from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types

def find_invalid_test(inst: DiffMat):
    inst._invalid = 1
    