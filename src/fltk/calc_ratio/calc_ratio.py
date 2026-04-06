from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from typing import Iterable
from rich import print as rprint

from . import calc_ratio_load_ratios as lr
from . import calc_ratio_load_data as ld
# from . import calc_comb_get_invalid_data as gid
# from . import calc_comb_get_undetermined_data as gud
# from . import calc_comb_get_valid_data as gvd
# from . import calc_comb_calculate as calc
# from . import calc_comb_add_calc as ac


class CalcRatio:
    def __init__(
        self,
        name: str,
        concept_ratio: str = "concept_ratio",
        concept_num: str = "concept_num",
        concept_den: str = "concept_den",
        ratio_value: str = "ratio_value",
    ):
        self._name = name
        self._concept_ratio = concept_ratio
        self._concept_num = concept_num
        self._concept_den = concept_den
        self._ratio_value = ratio_value
        self._ratios_df: pd.Dataframe = pd.DataFrame()
        reserved_vars: tuple[str, ...] = (
            concept_ratio,
            concept_num,
            concept_den,
            ratio_value,
        )
        check: int = len(reserved_vars) - len(set(reserved_vars))
        if not check:
            self._reserved_vars = reserved_vars
        else:
            msg: str = f"There are {check} duplicated reserved vars."
            raise ValueError(msg)

    @property
    def ratios_df(self) -> pd.DataFrame:
        return self._ratios_df

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
        pass
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

    def load_ratios(self, path: Path, sheet_nm: str | None = None) -> None:
        lr.load_ratios(self, path=path, sheet_nm=sheet_nm)

    def load_data(
        self,
        data: pd.DataFrame,
        concept_var: str,
        value_var: str,
        group_vars: Iterable[str],
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            concept_var (str): Column with the concept used for calculations.
            value_var (str): Column with values used for calculations.
            group_vars (Iterable[str]): Columns making up a composite key.
        """
        self._data_concept: str = ""
        self._data_value = ""
        self._data_group: Iterable[str] = []
        self._data: pd.DataFrame = pd.DataFrame()
        self._data_keys: list[str] = []
        data = ld.load_data(
            self,
            data=data,
            concept_var=concept_var,
            value_var=value_var,
            group_vars=group_vars,
        )
        self._data = data

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = pd.DataFrame()
        # self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)
        # print(f"\ninvalid_data {self._invalid_data.shape}:\n", self._invalid_data)

    def get_undetermined_data(self) -> None:
        self._undetermined_data: pd.DataFrame = pd.DataFrame()
        # self._undetermined_data: pd.DataFrame = gud.get_undetermined_data(self)
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
        rprint(f"{self._name} fit() completed.")

    def transform(self) -> None:
        """Do the actual calculations."""
        self.get_valid_data()
        self.calculate()
        self.add_calc()
        rprint(f"{self._name} transform() completed.")

    def get_valid_data(self) -> None:
        self._valid_data: pd.DataFrame = pd.DataFrame()
        # try:
        #     self._valid_data = gvd.get_valid_data(self)
        # except AttributeError as e:
        #     msg: str = "Attribute Error: Are tou sure you ran fit()?"
        #     e.add_note(msg)
        #     raise

    def calculate(self) -> None:
        pass
        # self._valid_data = calc.calculate(self)
        # breakpoint()
        # print(
        #     f"\ncalculated {self._valid_data.shape}:\n",
        #     self._valid_data,
        # )

    def add_calc(self) -> None:
        pass
        # self._data = ac.add_calc(self)
        # print(
        #     f"\nfinal data {self._data.shape}:\n",
        #     self._data,
        # )
