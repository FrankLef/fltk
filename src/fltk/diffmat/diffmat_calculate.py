from __future__ import annotations  # Must be at the top
from typing import TYPE_CHECKING
import pandas as pd

if TYPE_CHECKING:
    from .diffmat import DiffMat  # Only imported when checking types


def calculate(inst: DiffMat) -> pd.DataFrame:
    newdata = calc_newvalue(inst)
    return newdata

def calc_newvalue(inst:DiffMat)->pd.DataFrame:
    newdata = get_newvalues(inst)
    
    newvalid = pd.merge(
        left=inst._valid_data,
        right=newdata,
        on=inst._data_keys,
        )
    # breakpoint()
    
    ndata = inst._valid_data.shape[0]
    nnew = newvalid.shape[0]
    if nnew != ndata:
        msg:str=f"""
        Data and merged df must have the same nb of rows.
        Data has {ndata} rows, merged df has {nnew} rows.
        Weird!
        """
        raise AssertionError(msg)
    # breakpoint()
    return newvalid

def get_newvalues(inst:DiffMat)->pd.DataFrame:
    df = pd.merge(
        left=inst._valid_data,
        right=inst._idx_df,
        left_on=inst._data_idx,
        right_on=inst._idx_from
        )
    df[inst._data_newvalue] = df[inst._idx_coef] * df[inst._data_value]
    newkeys = list(inst._data_group)
    newkeys.append(inst._idx_to)
    newdata = df.groupby(by=newkeys, as_index=False)[inst._data_newvalue].sum()
    newdata.rename(columns={inst._idx_to: inst._data_idx}, inplace=True)
    # breakpoint()
    return newdata