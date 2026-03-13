from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Final, Any, NamedTuple
from pathlib import Path
import pandas as pd
from enum import StrEnum, auto

if TYPE_CHECKING:
    from .dic import IDic  # Only imported when checking types

class AttrName(StrEnum):
    GROUP = auto()
    NAME = auto()
    SKIPPED = auto()
    ROLE = auto()
    RULE = auto()

type dic_lines = list[NamedTuple]

def load_data(
        inst: IDic, path: Path, sheet_nm: str | None = None, is_xl: bool = True
    ) -> dic_lines:
    VARS_DTYPE: Final[dict[str, Any]] = {
        AttrName.GROUP: str,
        AttrName.NAME: str,
        AttrName.SKIPPED: bool,
        AttrName.ROLE: str,
        AttrName.RULE: str,
    }

    # NOTE: Important to specify the dtypes.
    # Otherwise problem, e.g. with the 'skipped' field which will not be interpreted as boolean.

    if is_xl:
        data = pd.read_excel(path, sheet_name=sheet_nm, dtype=VARS_DTYPE)
    else:
        data = pd.read_csv(path, dtype=VARS_DTYPE)

    if data.empty:
        raise ValueError(f"The import file '{path.name}' is empty.")

    is_subset = set(VARS_DTYPE.keys()).issubset(data.columns)
    if not is_subset:
        msg: str = f"Required column names in '{path.name}' are missing."
        raise ValueError(msg)

    EMPTY_STR: Final[str] = ""
    # NOTE: Remove NaN put by pandas. Not sure this is necessary anymore since using xl_dtypes above.  Keep it.
    for var in VARS_DTYPE.keys():
        data[var] = data[var].fillna(EMPTY_STR)

    lines: dic_lines = []
    for row in data.itertuples(index=False):
        lines.append(row)

    lines = inst.filter_skipped(lines)

    return lines