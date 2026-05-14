from __future__ import annotations  # Must be at the top
import pandas as pd
from rich import print as rprint

from ..calc.abc import Calc
from ..utils.value_cls import StrName

from . import vars
from . import load_ratios as lr
from . import load_raw_data as lrd
from . import merge_data as md

from . import calculate as calc


class CalcRatio(Calc):
    def __init__(
        self,
        name: str,
        data: pd.Dataframe,
        concept_ratio: str = "concept_ratio",
        concept_num: str = "concept_num",
        concept_den: str = "concept_den",
        value_ratio: str = "value_ratio",
        value_num: str = "value_num",
        value_den: str = "value_den",
        concept_nm: str = "concept_nm",
        concept_pos: str = "concept_pos",
    ):
        """Object with ratio definitions to calculate ratios using raw data.

        Args:
            name (str): Name to identify the object.
            data (pd.Dataframe): Ratio definitions.
            concept_ratio (str, optional): Names of ratio. Defaults to "concept_ratio".
            concept_num (str, optional): Names of concepts in numerator. Defaults to "concept_num".
            concept_den (str, optional): Names of Concepts in denominator. Defaults to "concept_den".
            value_ratio (str, optional): Calculated ratio value. Defaults to "value_ratio".
            value_num (str, optional): Numerator value. Defaults to "value_num".
            concept_nm (str, optional): Concept name used by the long format. Defaults to "concept_name".
            concept_pos (str, optional): Concept position, 'num' or 'den' used by the long format. Defaults to "concept_pos".
        """
        (super().__init__(StrName(name)),)
        self.ratios_vars = vars.RatioVars(
            concept_ratio=StrName(concept_ratio),
            concept_num=StrName(concept_num),
            concept_den=StrName(concept_den),
            value_ratio=StrName(value_ratio),
            value_num=StrName(value_num),
            value_den=StrName(value_den),
            concept_nm=StrName(concept_nm),
            concept_pos=StrName(concept_pos),
        )
        self.ratios = lr.load_ratios(self, data=data)
        self.ratios_long = lr.melt_ratios(
            self.ratios,
            concept_ratio=self.ratios_vars.concept_ratio,
            concept_nm=self.ratios_vars.concept_nm,
            concept_pos=self.ratios_vars.concept_pos,
        )

    def load_raw_data(
        self,
        data: pd.DataFrame,
        concept: str,
        value: str,
        groups: tuple[str, ...],
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            concept (str): Column with the concept used for calculations.
            value (str): Column with values used for calculations.
            group (tuple[str, ...]): Columns making up a composite key.
        """
        self.raw_vars = vars.RawVars(groups=groups, concept=concept, value=value)

        data = lrd.load_raw_data(self, data=data)
        self.raw = data

    def merge_data(self) -> None:
        self.merged: pd.DataFrame = md.merge_data(self)

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

    def get_dfs(self) -> dict[str, pd.DataFrame]:
        dfs = {
            "data": self.raw,
            "ratios": self.ratios,
            "ratios long": self.ratios_long,
            "merged": self.merged,
            "calc": self.calc,
        }
        return dfs
