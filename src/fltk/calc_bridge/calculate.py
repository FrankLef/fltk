from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .main import CalcBridge  # Only imported when checking types


def calculate(inst: CalcBridge) -> pd.DataFrame:
    _bridge = inst.bridge_df
    _volume = inst.bridge.volume_diff
    _price = inst.bridge.price_diff
    _mix = inst.bridge.mix_diff
    _total = inst.bridge.total_diff
    _check = inst.bridge.check_diff
    _is_err = inst.bridge.is_err
    _den = inst.raw.den_val
    _ratio = inst.raw.ratio_val
    _num = inst.raw.num_val

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

    _bridge[_is_err] = _bridge[_check] - _bridge[_total]

    return _bridge
