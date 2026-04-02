from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from typing import Iterable
from rich import print as rprint

from . import diffmat_load_mat_xl as lmx
from . import diffmat_load_data as ld
from . import diffmat_get_invalid_data as gid
from . import diffmat_get_undetermined_data as gud
from . import diffmat_get_valid_data as gvd
from . import diffmat_calculate as calc
from . import diffmat_add_calc as ac


class DiffMat:
    def __init__(self, name: str, idx_to: str = "idx_to"):
        """Compute new amounts with a new index using a difference matrix.

        Args:
            name (str: Name for the object.)
            idx_to (str, optional): Name of the column with the new index used with the new calculated amounts. This is also the top left corner of a matrix given in excel. Defaults to "idx_to".
        """
        self._name = name
        self._idx_to = idx_to
        self._idx_keys: list[str] = []
        self._idx_df: pd.Dataframe = pd.DataFrame()
        self.set_reserved_vars()

    @property
    def idx_df(self) -> pd.DataFrame:
        return self._idx_df

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
    
    @property
    def summary(self) -> dict[str, int]:
        nrows_data = self._data.shape[0]
        nrows_valid = self._valid_data.shape[0]
        nrows_invalid = self._invalid_data.shape[0]
        nrows_undetermined = self._undetermined_data.shape[0]
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
            "undetermined": nrows_undetermined
        }
        return out
    
    def set_reserved_vars(
        self,
        idx_from: str = "idx_from",
        idx_coef: str = "idx_coef",
        idx_value: str = "idx_value",
    ) -> None:
        """Set the reserved words used when doing computations internally.

        Args:
            idx_from (str, optional): Column with index to use. Defaults to "idx_from".
            idx_coef (str, optional): Column of coefficients to use. Defaults to "idx_coef".
            idx_value (str, optional): Column of values to use. Defaults to "idx_value".

        Raises:
            ValueError: Name conflict in reserved words.
        """
        self._idx_from: str = idx_from
        self._idx_coef: str = idx_coef
        self._idx_value: str = idx_value
        reserved_vars = [self._idx_from, self._idx_coef, self._idx_value]
        if self._idx_to in reserved_vars:
            msg: str = f"'{self._idx_to}' is reserved. Use another name."
            raise ValueError(msg)
        reserved_vars.append(self._idx_to)
        self._reserved_vars = reserved_vars

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
        # print("load_data")
        # breakpoint()

    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None) -> None:
        """Load difference matrix from Excel to a pandas dataframe.

        Args:
            path (Path): Full filename of excel file.
            sheet_nm (str | None, optional): Name of excel sheet. Defaults to None.
        """
        lmx.load_mat_from_xl(self, path=path, sheet_nm=sheet_nm)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)
        # print(f"\ninvalid_data {self._invalid_data.shape}:\n", self._invalid_data)

    def get_undetermined_data(self) -> None:
        self._undetermined_data: pd.DataFrame = gud.get_undetermined_data(self)
        # print(
        #     f"\nundetermined_data {self._undetermined_data.shape}:\n",
        #     self._undetermined_data,
        # )

    def fit_transform(self) -> None:
        """Process the the fit and transform steps in a sequnce."""
        self.fit()
        self.transform()

    def fit(self) -> None:
        """Fit the data. Find invalid and undetermined data."""
        self.get_invalid_data()
        self.get_undetermined_data()
        rprint("Diffmat fit() completed.")

    def transform(self) -> None:
        """Do the actual calculations."""
        self.get_valid_data()
        self.calculate()
        self.add_calc()
        rprint("Diffmat transform() completed.")

    def get_valid_data(self) -> None:
        try:
            self._valid_data = gvd.get_valid_data(self)
        except AttributeError as e:
            msg: str = "Attribute Error: Are tou sure you ran fit()?"
            e.add_note(msg)
            raise

        # print(
        #     f"\nvalid_data {self._valid_data.shape}:\n",
        #     self._valid_data,
        # )

    def calculate(self) -> None:
        self._valid_data = calc.calculate(self)
        # breakpoint()
        # print(
        #     f"\ncalculated {self._valid_data.shape}:\n",
        #     self._valid_data,
        # )

    def add_calc(self) -> None:
        self._data = ac.add_calc(self)
        # print(
        #     f"\nfinal data {self._data.shape}:\n",
        #     self._data,
        # )
