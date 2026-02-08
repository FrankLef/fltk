import pandas as pd
from pathlib import Path
from typing import Iterable

class DiffMat:
    def __init__(self, idx_to:str="idx_to"):
        self._idx_to=idx_to
        self._idx_from="idx_from"
        self._idx_coef = "idx_coef"
        self._idx_value = "idx_value"
        self._idx_df= pd.DataFrame()
        self.set_reserved_vars()
    
    @property
    def idx_df(self):
        return self._idx_df
    
    @property
    def data(self):
        return self._data
    
    def set_reserved_vars(self)->None:
        reserved_vars = [self._idx_from, self._idx_coef, self._idx_value]
        if self._idx_to in reserved_vars:
            msg:str=f"'{self._idx_to}' is reserved. Use another name for idx_to."
            raise ValueError(msg)
        reserved_vars.append(self._idx_to)
        self._reserved_vars = reserved_vars
        
    def validate_idx_keys(self, idx_df: pd.Dataframe)->None:
        keys = [self._idx_to, self._idx_from]
        unique_counts = idx_df[keys].value_counts()
        ndistinct = len(unique_counts)
        if ndistinct != idx_df.shape[0]:
            msg: str = f"Matrix has invalid keys {keys}."
            raise ValueError(msg)
        
    def validate_data_names(self, data:pd.DataFrame)->None:
        reserved_vars = self._reserved_vars
        data_vars = data.columns.to_list()
        illegal_vars = [var for var in data_vars if var in reserved_vars]
        if illegal_vars:
            msg:str=f"""
            {illegal_vars} are reserved names.
            Please change these column names.
            """
            raise ValueError(msg)
        
    def validate_data_keys(self,data:pd.DataFrame,keys)->None:
        unique_counts = data[keys].value_counts()
        ndistinct = len(unique_counts)
        if ndistinct != data.shape[0]:
            msg: str = f"Data has invalid keys {keys}."
            raise ValueError(msg)
        
    
    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None)->None:
        df = pd.read_excel(path, sheet_name=sheet_nm)
        cols = df.columns[df.columns != self._idx_to].to_list()
        df = df.melt(id_vars=self._idx_to, value_vars=cols, var_name=self._idx_from, value_name=self._idx_value)
        df.dropna(inplace=True)
        self.validate_idx_keys(df)
        self._idx_df = df
        
    def load_data(self, data:pd.DataFrame, idx_var:str, value_var:str, key_vars: Iterable[str])->None:
        if self._idx_df.empty:
            msg:str="You must load the matrix before the data."
            raise ValueError(msg)
        self.validate_data_names(data)
        data_keys = [idx_var]
        data_keys.extend(key_vars)
        self.validate_data_keys(data, keys=data_keys)
        self._data_keys=data_keys
        self._data = data