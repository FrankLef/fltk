from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from typing import Iterable
from rich import print as rprint

from . import calc_ratio_load_ratios as lr
from . import calc_ratio_load_data as ld
from . import calc_ratio_merge_data as md
from . import calc_ratio_invalid_data as gid
from . import calc_ratio_calculate as calc


class CalcRatio:
    def __init__(
        self,
        name: str,
        concept_ratio: str = "concept_ratio",
        concept_num: str = "concept_num",
        concept_den: str = "concept_den",
        concept_name: str = "concept_name",
        concept_pos: str = "concept_pos",
        value_ratio: str = "value_ratio",
        value_num: str = "value_num",
        value_den: str = "value_den",
    ):
        """Create object to calculate ratios of amounts.

        Args:
            name (str): Name to identify the object. Does not affect the process itself.
            concept_ratio (str, optional): Column of ratio names. Defaults to "concept_ratio".
            concept_num (str, optional): Column of concepts in numerator. Defaults to "concept_num".
            concept_den (str, optional): Column of concepts in denominator. Defaults to "concept_den".
            concept_name (str, optional): Column of concept names in the long ratio data. Defaults to "concept_name".
            concept_pos (str, optional): Column of concept positions, i.e. 'num or 'den', in the long ratio data. Defaults to "concept_pos".
            value_ratio (str, optional): Column of calculated ratio value. Defaults to "value_ratio".
            value_num (str, optional): Column of concept value used in merged data. Defaults to "value_num".
            value_den (str, optional): Column of concept value used in merged data. Defaults to "value_den".

        Raises:
            ValueError: Duplicate names.
        """
        self._name = name
        self._concept_ratio = concept_ratio
        self._concept_num = concept_num
        self._concept_den = concept_den
        self._concept_name = concept_name
        self._concept_pos = concept_pos
        self._value_ratio = value_ratio
        self._value_num = value_num
        self._value_den = value_den
        self._ratios_df: pd.Dataframe = pd.DataFrame()
        self._ratios_df_long: pd.Dataframe = pd.DataFrame()
        reserved_vars: tuple[str, ...] = (
            concept_ratio,
            concept_num,
            concept_den,
            concept_name,
            concept_pos,
            value_ratio,
            value_num,
            value_den,
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
    def ratios_df_long(self) -> pd.DataFrame:
        return self._ratios_df_long

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @property
    def merged_data(self) -> pd.DataFrame:
        return self._merged_data

    @property
    def invalid_data(self) -> pd.DataFrame:
        return self._invalid_data

    def summary(self, verbose: bool = True) -> dict[str, int]:
        pass
        nrows_data = self._data.shape[0]
        nrows_merged = self._merged_data.shape[0]
        nrows_invalid = self._invalid_data.shape[0]
        if verbose:
            msg: str = f"""
            Summary of {self._name}
            -------------------------
            Data: {nrows_data} rows
            Merged data: {nrows_merged} rows
            Invalid data: {nrows_invalid} rows
            """
            rprint(msg)
            out = {
                "data": nrows_data,
                "merged": nrows_merged,
                "invalid": nrows_invalid,
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

    def merge_data(self) -> None:
        self._merged_data: pd.DataFrame = md.merge_data(self)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)

    def fit_transform(self, is_cleaned: bool) -> None:
        """Process the the fit and transform steps in sequence."""
        self.fit()
        self.transform(is_cleaned=is_cleaned)

    def fit(self) -> None:
        """Create merged data and flag invalid."""
        self.merge_data()
        self.get_invalid_data()
        rprint(f"{self._name} fit() completed.")

    def transform(self, is_cleaned: bool) -> None:
        """Do the actual calculations."""
        self.calculate()
        if is_cleaned:
            self.clean()
        rprint(f"{self._name} transform() completed.")

    def calculate(self) -> None:
        self._merged_data = calc.calculate(self)

    def clean(self) -> None:
        df = self._merged_data
        cols = (self._value_ratio, self._value_num, self._value_den)
        df.replace([float("inf"), float("-inf")], value=None, inplace=True)
        df.dropna(subset=cols, inplace=True)
