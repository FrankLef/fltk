from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from typing import Iterable

from . import diffmat_get_invalid_data as fi
from . import diffmat_load_mat_xl as lmx
from . import diffmat_load_data as ld


class DiffMat:
    def __init__(self, idx_to: str = "idx_to"):
        self._idx_to = idx_to  # column with index of values to replace
        self._idx_from: str = "idx_from"  # column with index of values to use
        self._idx_coef: str = "idx_coef"  # column of coefficients used
        self._idx_value: str = "idx_value"  # name of column with new values in data
        self._idx_keys: list[str] = []
        self._idx_df: pd.Dataframe = pd.DataFrame()
        self.set_reserved_vars()

    @property
    def idx_df(self):
        return self._idx_df

    @property
    def data(self):
        return self._data

    @property
    def idx_validation(self):
        return self._idx_validation

    def set_reserved_vars(self) -> None:
        reserved_vars = [self._idx_from, self._idx_coef, self._idx_value]
        if self._idx_to in reserved_vars:
            msg: str = f"'{self._idx_to}' is reserved. Use another name for idx_to."
            raise ValueError(msg)
        reserved_vars.append(self._idx_to)
        self._reserved_vars = reserved_vars

    def load_data(
        self,
        data: pd.DataFrame,
        idx_var: str,
        value_var: str,
        group_vars: Iterable[str],
    ) -> None:
        self._data_idx: str = ""
        self._data_value = ""
        self._data_group: Iterable[str] = []
        self._data: pd.DataFrame = pd.DataFrame()
        self._data_keys: list[str] = []
        ld.load_data(
            self, data=data, idx_var=idx_var, value_var=value_var, group_vars=group_vars
        )

    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None) -> None:
        lmx.load_mat_from_xl(self, path=path, sheet_nm=sheet_nm)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = fi.get_invalid_data(self)
        print(f"\ninvalid_data {self._invalid_data.shape}:\n", self._invalid_data)

    def fit(self) -> None:
        self.get_invalid_data()
        # self.fit_invalid_idx()

    def fit_invalid_idx(self) -> None:
        left_df = self._idx_df
        right_df = self._data
        left_on = self._idx_from
        right_on = self._data_idx
        idx_validation = pd.merge(
            left_df,
            right_df,
            left_on=left_on,
            right_on=right_on,
            how="left",
            indicator=True,
        )
        # cols=self._idx_keys
        # cols.extend([right_on, "_merge"])
        # self._idx_validation = idx_validation[cols]
        self._idx_validation = idx_validation
