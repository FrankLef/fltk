import pandas as pd
from pathlib import Path
# from typing import NamedTuple, Iterable, Final, Any

class DiffMat:
    def __init__(self, idx_to:str="idx_to"):
        self._idx_to=idx_to
        self._idx_from="idx_from"
        self._idx_value = "idx_value"
    
    @property
    def idx_df(self):
        return self._idx_df
    
    def validate(self)->None:
        if self._idx_to in (self._idx_from,self._idx_value):
            msg:str=f"'{self._idx_to}' is reserved. Use another name for idx_to."
            raise ValueError(msg)
    
    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None)->None:
        df = pd.read_excel(path, sheet_name=sheet_nm)
        cols = df.columns[df.columns != self._idx_to].to_list()
        df = df.melt(id_vars=self._idx_to, value_vars=cols, var_name=self._idx_from, value_name=self._idx_value)
        df.dropna(inplace=True)
        # mat.fillna(0,inplace=True)
        self._idx_df = df