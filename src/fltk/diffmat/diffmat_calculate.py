from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def calculate(inst: DiffMat)-> pd.DataFrame:
    return inst._valid_data