from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .main import CalcRatio  # Only imported when checking types


def _init_ratio_vars(inst: CalcRatio) -> None:
    ratio_vars: list[str] = [
        inst._concept_ratio,
        inst._concept_num,
        inst._concept_den,
        inst._concept_name,
        inst._concept_pos,
        inst._value_ratio,
        inst._value_num,
        inst._value_den
    ]
    check: int = len(ratio_vars) - len(set(ratio_vars))
    if check:
        msg: str = f"There are {check} duplicated ratio variables."
        raise ValueError(msg)
    inst._ratio_vars = ratio_vars


def _init_data_vars(inst:CalcRatio) -> None:
    data_vars: list[Any] = [
        inst._data_concept,
        inst._data_value,
    ] + inst._data_group
    check: int = len(data_vars) - len(set(data_vars))
    if check:
        msg: str = f"There are {check} duplicated data variables."
        raise ValueError(msg)
    inst._data_vars = data_vars
    
    data_keys: list[str] = inst._data_group.copy()
    data_keys.append(inst._data_concept)
    inst._data_keys = data_keys
