from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from typing import Iterable
from rich import print as rprint

from . import calc_comb_load_mat_xl as lmx
from . import calc_comb_load_data as ld
from . import calc_comb_get_invalid_data as gid
from . import calc_comb_get_undetermined_data as gud
from . import calc_comb_get_valid_data as gvd
from . import calc_comb_calculate as calc
from . import calc_comb_add_calc as ac


class CalcComb:
    def __init__(
        self,
        name: str,
        idx_to: str = "idx_to",
        idx_from: str = "idx_from",
        comb_coef: str = "comb_coef",
        comb_value: str = "comb_value",
    ):
        """Create object to calculate combinations of amounts.

        Args:
            name (str): Name to identify the object. Does not affect the process itself.
            idx_to (str, optional): Name of the column with the target index used. Same as the upper left corner of the matrix. Defaults to "idx_to".
            idx_from (str, optional): Name of the column with the source index used. It is recommended to keep the default value. Defaults to "idx_from".
            comb_coef (str, optional): Column of coefficients to use. It is recommended to keep the default value. Defaults to "comb_coef".
            comb_value (str, optional): Column of values to use. It is recommended to keep the default value. Defaults to "comb_value".

        Raises:
            ValueError: Duplicate names.
        """
        self._name = name
        self._idx_to = idx_to
        self._idx_from = idx_from
        self._comb_coef = comb_coef
        self._comb_value = comb_value
        self._comb_keys: list[str] = []
        self._comb_df: pd.Dataframe = pd.DataFrame()
        reserved_vars: tuple[str, ...] = (idx_to, idx_from, comb_coef, comb_value)
        check: int = len(reserved_vars) - len(set(reserved_vars))
        if not check:
            self._reserved_vars = reserved_vars
        else:
            msg: str = f"There are {check} duplicated reserved vars."
            raise ValueError(msg)

    @property
    def comb_df(self) -> pd.DataFrame:
        return self._comb_df

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def invalid_data(self):
        return self._invalid_data

    @property
    def undetermined_data(self) -> pd.DataFrame:
        return self._undetermined_data

    @property
    def valid_data(self) -> pd.DataFrame:
        return self._valid_data

    def summary(self, verbose: bool = True) -> dict[str, int]:
        nrows_data = self._data.shape[0]
        nrows_valid = self._valid_data.shape[0]
        nrows_invalid = self._invalid_data.shape[0]
        nrows_undetermined = self._undetermined_data.shape[0]
        if verbose:
            msg: str = f"""
            Summary of {self._name}
            -------------------------
            Data: {nrows_data} rows
            Valid data: {nrows_valid} rows
            Invalid data: {nrows_invalid} rows
            Undetermined data: {nrows_undetermined} rows
            """
            rprint(msg)
            out = {
                "data": nrows_data,
                "valid": nrows_valid,
                "invalid": nrows_invalid,
                "undetermined": nrows_undetermined,
            }
        return out

    def load_data(
        self,
        data: pd.DataFrame,
        idx_var: str,
        value_var: str,
        group_vars: Iterable[str],
        newvalue_var: str,
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            idx_var (str): Column with the index used for calculations.
            value_var (str): Column with values used for calculations.
            group_vars (Iterable[str]): Columns making up a composite key.
            newvalue_var (str): New column for calculated values.
        """
        self._data_idx: str = ""
        self._data_value = ""
        self._data_group: Iterable[str] = []
        self._data_newvalue = ""
        self._data: pd.DataFrame = pd.DataFrame()
        self._data_keys: list[str] = []
        data = ld.load_data(
            self,
            data=data,
            idx_var=idx_var,
            value_var=value_var,
            group_vars=group_vars,
            newvalue_var=newvalue_var,
        )
        self._data = data

    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None) -> None:
        """Load difference matrix from Excel to a pandas dataframe.

        Args:
            path (Path): Full filename of excel file.
            sheet_nm (str | None, optional): Name of excel sheet. Defaults to None.
        """
        lmx.load_mat_from_xl(self, path=path, sheet_nm=sheet_nm)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)

    def get_undetermined_data(self) -> None:
        self._undetermined_data: pd.DataFrame = gud.get_undetermined_data(self)

    def fit_transform(self) -> None:
        """Process the the fit and transform steps in a sequnce."""
        self.fit()
        self.transform()

    def fit(self) -> None:
        """Fit the data. Find invalid and undetermined data."""
        self.get_invalid_data()
        self.get_undetermined_data()
        rprint(f"{self._name} fit() completed.")

    def transform(self) -> None:
        """Do the actual calculations."""
        self.get_valid_data()
        self.calculate()
        self.add_calc()
        rprint(f"{self._name} transform() completed.")

    def get_valid_data(self) -> None:
        try:
            self._valid_data = gvd.get_valid_data(self)
        except AttributeError as e:
            msg: str = "Attribute Error: Are tou sure you ran fit()?"
            e.add_note(msg)
            raise

    def calculate(self) -> None:
        self._valid_data = calc.calculate(self)

    def add_calc(self) -> None:
        self._data = ac.add_calc(self)
