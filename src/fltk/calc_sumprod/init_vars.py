from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .main import CalcSumprod  # Only imported when checking types


def _init_sump_vars(inst: CalcSumprod) -> None:
    sump_vars: list[str] = [
        inst._idx_to,
        inst._idx_from,
        inst._sump_coef,
        inst._sump_value,
    ]
    check: int = len(sump_vars) - len(set(sump_vars))
    if check:
        msg: str = f"There are {check} duplicated comb variables."
        raise ValueError(msg)
    inst._sump_vars = sump_vars

    inst._sump_keys = [inst._idx_to, inst._idx_from]
    # NOTE: Used to exclude varibale in combs_df that are irrelevant. See load_combs.
    inst._sump_vars_base = [
        inst._idx_to,
        inst._idx_from,
        inst._sump_coef,
    ]


def _init_data_vars(inst: CalcSumprod) -> None:
    data_vars: list[Any] = [
        inst._data_idx,
        inst._data_value,
        inst._data_newvalue,
    ] + inst._data_group
    check: int = len(data_vars) - len(set(data_vars))
    if check:
        msg: str = f"There are {check} duplicated data variables."
        raise ValueError(msg)
    inst._data_vars = data_vars

    data_keys = inst._data_group.copy()
    data_keys.append(inst._data_idx)
    inst._data_keys = data_keys
