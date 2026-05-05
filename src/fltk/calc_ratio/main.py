from __future__ import annotations  # Must be at the top
import pandas as pd
from rich import print as rprint
from rich.pretty import pprint
from pathlib import Path

from ..utils.value_cls import StrName
from ..utils import to_excel as xl

from . import vars
from . import load_ratios as lr
from . import load_raw_data as lrd
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
        self.name = StrName(name)
        self.ratios_vars = vars.Ratios(
            concept_ratio=StrName(concept_ratio),
            concept_num=StrName(concept_num),
            concept_den=StrName(concept_den),
            concept_name=StrName(concept_name),
            concept_pos=StrName(concept_pos),
            value_ratio=StrName(value_ratio),
            value_num=StrName(value_num),
            value_den=StrName(value_den),
        )
        self.ratios: pd.Dataframe = pd.DataFrame()
        self.ratios_long: pd.Dataframe = pd.DataFrame()

    def __repr__(self):
        summary = self.get_summary()
        title = f"{type(self).__name__}: {self.name}"
        out = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in summary.items():
            out += f"{key:<10}: {value}\n"
        return out

    def load_ratios(self, data: pd.Dataframe) -> None:
        """Load dataframe of ratio definitions.

        Args:
            data (pd.Dataframe): dataframe of ratio definitions.
        """
        lr.load_ratios(self, data=data)

    def load_raw_data(
        self,
        data: pd.DataFrame,
        concept_var: str,
        value_var: str,
        group_vars: tuple[str, ...],
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            concept_var (str): Column with the concept used for calculations.
            value_var (str): Column with values used for calculations.
            group_vars (Iterable[str]): Columns making up a composite key.
        """
        self.raw_vars = vars.Raw(
            groups=group_vars, concept=concept_var, value=value_var
        )

        data = lrd.load_raw_data(self, data=data)
        self.raw = data

    def merge_data(self) -> None:
        self.merged: pd.DataFrame = md.merge_data(self)

    def get_invalid_data(self) -> None:
        self.invalid: pd.DataFrame = gid.get_invalid_data(self)

    def get_valid_data(self) -> None:
        self.valid: pd.DataFrame = gvd.get_valid_data(self)

    def fit_transform(self, is_cleaned: bool, verbose: bool = False) -> None:
        """Process the the fit and transform steps in sequence.

        Args:
            is_cleaned (bool): If True, remove rows with null of inf/-inf from calc_data.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.fit(verbose=verbose)
        self.transform(is_cleaned=is_cleaned, verbose=verbose)

    def fit(self, verbose: bool = False) -> None:
        """Create merged data and flag invalid.

        Args:
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.merge_data()
        self.get_invalid_data()
        self.get_valid_data()
        if verbose:
            rprint(f"{self.name} fit() completed.")

    def transform(self, is_cleaned: bool, verbose: bool = False) -> None:
        """Calculate ratios.

        Args:
            is_cleaned (bool): If True, remove rows with null of inf/-inf from calc_data.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.calculate()
        if is_cleaned:
            self.clean()
        if verbose:
            rprint(f"{self.name} transform() completed.")

    def calculate(self) -> None:
        """Calculate ratios."""
        self.calc = calc.calculate(self)

    def clean(self) -> None:
        """Remove rows with null of inf/-inf from calc_data."""
        _value_ratio = self.ratios_vars.value_ratio
        _value_num = self.ratios_vars.value_num
        _value_den = self.ratios_vars.value_den
        df = self.calc
        cols = (_value_ratio, _value_num, _value_den)
        df.replace([float("inf"), float("-inf")], value=None, inplace=True)
        df.dropna(subset=cols, inplace=True)

    def summary(self, verbose: bool = True) -> dict[str, int]:
        ndata = self.raw.shape[0]
        nratios_df = (self.ratios.shape[0],)
        nratios_df_long = (self.ratios_long.shape[0],)
        nmerged = self.merged.shape[0]
        ninvalid = self.invalid.shape[0]
        nvalid = self.valid.shape[0]
        ncalc = self.calc.shape[0]
        if verbose:
            out = {
                "data": ndata,
                "ratios_df": nratios_df,
                "ratios_df_long": nratios_df_long,
                "merged": nmerged,
                "invalid": ninvalid,
                "valid": nvalid,
                "calculated": ncalc,
            }
            pprint(out)
        return out

    def get_summary(self) -> dict[str, tuple[int, ...]]:
        summary = {
            "raw data": self.raw.shape,
            "ratios_df": self.ratios.shape,
            "ratios_long_df": self.ratios_long.shape,
            "merged_data": self.merged.shape,
            "invalid": self.invalid.shape,
            "valid_data": self.valid.shape,
            "calc_data": self.calc.shape,
        }
        return summary

    def to_excel(self, path: Path) -> None:
        dfs = {
            "data": self.raw,
            "ratios_df": self.ratios,
            "ratios_long_df": self.ratios_long,
            "merged_data": self.merged,
            "invalid": self.invalid,
            "valid_data": self.valid,
            "calc_data": self.calc,
        }
        name = f"{type(self).__name__} '{self.name}'"
        xl.to_excel(name, path=path, dfs=dfs)
