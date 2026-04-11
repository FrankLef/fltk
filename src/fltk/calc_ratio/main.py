from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from rich import print as rprint

from fltk.utils.value_cls import StrName

from . import init_vars as iv
from . import load_ratios as lr
from . import load_data as ld
from . import merge_data as md
from . import invalid_data as gid
from . import valid_data as gvd
from . import calculate as calc


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
        self._name = StrName(name)
        self._concept_ratio = StrName(concept_ratio)
        self._concept_num = StrName(concept_num)
        self._concept_den = StrName(concept_den)
        self._concept_name = StrName(concept_name)
        self._concept_pos = StrName(concept_pos)
        self._value_ratio = StrName(value_ratio)
        self._value_num = StrName(value_num)
        self._value_den = StrName(value_den)
        self._ratios_df: pd.Dataframe = pd.DataFrame()
        self._ratios_df_long: pd.Dataframe = pd.DataFrame()
        self._init_ratio_vars()

    def _init_ratio_vars(self) -> None:
        self._ratio_vars: list[str] = []
        self._ratio_keys: list[str] = []
        iv._init_ratio_vars(self)

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
    
    @property
    def valid_data(self) -> pd.DataFrame:
        return self._valid_data
    
    @property
    def calc_data(self) -> pd.DataFrame:
        return self._calc_data

    def summary(self, verbose: bool = True) -> dict[str, int]:
        ndata = self._data.shape[0]
        nmerged = self._merged_data.shape[0]
        ninvalid = self._invalid_data.shape[0]
        nvalid = self._valid_data.shape[0]
        ncalc = self._calc_data.shape[0]
        if verbose:
            msg: str = f"""
            Summary of {self._name}
            -------------------------
            Data: {ndata} rows
            Merged data: {nmerged} rows
            Invalid data: {ninvalid} rows
            Valid data: {nvalid} rows
            Calculated data: {ncalc} rows
            """
            rprint(msg)
            out = {
                "data": ndata,
                "merged": nmerged,
                "invalid": ninvalid,
                "valid": nvalid,
                "calculated": ncalc,
            }
        return out

    def load_ratios(self, path: Path, sheet_nm: str | None = None) -> None:
        lr.load_ratios(self, path=path, sheet_nm=sheet_nm)

    def load_data(
        self,
        data: pd.DataFrame,
        concept_var: str,
        value_var: str,
        group_vars: list[str],
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            concept_var (str): Column with the concept used for calculations.
            value_var (str): Column with values used for calculations.
            group_vars (Iterable[str]): Columns making up a composite key.
        """
        self._data_concept = StrName(concept_var)
        self._data_value = StrName(value_var)
        self._data_group = [str(StrName(var)) for var in group_vars]
        self._data: pd.DataFrame = pd.DataFrame()

        self._init_data_vars()

        data = ld.load_data(
            self,
            data=data,
            concept_var=concept_var,
            value_var=value_var,
            group_vars=group_vars,
        )
        self._data = data

    def _init_data_vars(self) -> None:
        """Initialize the variables."""
        self._data_vars: list[str] = []
        self._data_keys: list[str] = []
        iv._init_data_vars(self)

    def merge_data(self) -> None:
        self._merged_data: pd.DataFrame = md.merge_data(self)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)
    
    def get_valid_data(self) -> None:
        self._valid_data: pd.DataFrame = gvd.get_valid_data(self)
    
    def fit_transform(self, is_cleaned: bool, verbose:bool=False) -> None:
        """Process the the fit and transform steps in sequence.

        Args:
            is_cleaned (bool): If True, remove rows with null of inf/-inf from calc_data.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.fit(verbose=verbose)
        self.transform(is_cleaned=is_cleaned, verbose=verbose)
        
        
    def fit(self, verbose:bool=False) -> None:
        """Create merged data and flag invalid.

        Args:
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.merge_data()
        self.get_invalid_data()
        self.get_valid_data()
        if verbose:
            rprint(f"{self._name} fit() completed.")

    def transform(self, is_cleaned: bool, verbose:bool=False) -> None:
        """Calculate ratios.

        Args:
            is_cleaned (bool): If True, remove rows with null of inf/-inf from calc_data.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.calculate()
        if is_cleaned:
            self.clean()
        if verbose:
            rprint(f"{self._name} transform() completed.")

    def calculate(self) -> None:
        """Calculate ratios."""
        self._calc_data = calc.calculate(self)

    def clean(self) -> None:
        """Remove rows with null of inf/-inf from calc_data."""
        df = self._calc_data
        cols = (self._value_ratio, self._value_num, self._value_den)
        df.replace([float("inf"), float("-inf")], value=None, inplace=True)
        df.dropna(subset=cols, inplace=True)
