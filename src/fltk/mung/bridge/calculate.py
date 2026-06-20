from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def calculate(inst: CalcBridge) -> pd.DataFrame:
    _bridge = inst.bridge
    _volume = inst.bridge_vars.volume_diff
    _price = inst.bridge_vars.price_diff
    _mix = inst.bridge_vars.mix_diff
    _total = inst.bridge_vars.total_diff
    _check = inst.bridge_vars.check_diff
    _err = inst.bridge_vars.err
    _den = inst.raw_vars.den_val
    _ratio = inst.raw_vars.ratio_val
    _num = inst.raw_vars.num_val

    _ratio_sfx = inst.add_suffix(_ratio)
    _num_sfx = inst.add_suffix(_num)
    _den_sfx = inst.add_suffix(_den)

    _bridge[_volume] = (_bridge[_den_sfx[1]] - _bridge[_den_sfx[0]]) * _bridge[
        _ratio_sfx[0]
    ]

    _bridge[_price] = (_bridge[_ratio_sfx[1]] - _bridge[_ratio_sfx[0]]) * _bridge[
        _den_sfx[0]
    ]

    _bridge[_mix] = (_bridge[_ratio_sfx[1]] - _bridge[_ratio_sfx[0]]) * (
        _bridge[_den_sfx[1]] - _bridge[_den_sfx[0]]
    )

    _bridge[_total] = _bridge[_volume] + _bridge[_price] + _bridge[_mix]

    _bridge[_check] = _bridge[_num_sfx[1]] - _bridge[_num_sfx[0]]

    _bridge[_err] = _bridge[_check] - _bridge[_total]

    return _bridge
