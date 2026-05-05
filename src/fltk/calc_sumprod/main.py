from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from rich import print as rprint

from ..utils.value_cls import StrName
from ..utils import to_excel as xl

from . import vars
from . import load_mat_xl as lmx
from . import load_sump as lc
from . import load_raw_data as lrd
from . import invalid_data as gid
from . import valid_data as gvd
from . import calculate as calc
from . import add_calc as ac


class CalcSumprod:
    def __init__(
        self,
        name: str,
        idx_to: str = "idx_to",
        idx_from: str = "idx_from",
        sump_coef: str = "sump_coef",
        sump_value: str = "sump_value",
    ):
        """Create object to calculate the sum of products.

        Args:
            name (str): Name to identify the object. Does not affect the process itself.
            idx_to (str, optional): Name of the column with the target index used. Same as the upper left corner of the matrix. Defaults to "idx_to".
            idx_from (str, optional): Name of the column with the source index used. It is recommended to keep the default value. Defaults to "idx_from".
            sump_coef (str, optional): Column of coefficients to use. It is recommended to keep the default value. Defaults to "sump_coef".
            sump_value (str, optional): Column of values to use. It is recommended to keep the default value. Defaults to "sump_value".

        Raises:
            ValueError: Duplicate names.
        """
        self.name = StrName(name)
        self.sump_vars = vars.Sumprod(
            idx_to=StrName(idx_to),
            idx_from=StrName(idx_from),
            sump_coef=StrName(sump_coef),
            sump_value=StrName(sump_value),
        )
        self.sump = pd.DataFrame()

    def __repr__(self):
        summary = self.get_summary()
        title = f"{type(self).__name__}: {self.name}"
        out = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in summary.items():
            out += f"{key:<10}: {value}\n"
        return out

    def _init_sump_vars(self) -> None:
        self._sump_vars: list[str] = []
        self._sump_keys: list[str] = []
        self._sump_vars_base: list[str] = []


    def load_sump(self, data: pd.DataFrame) -> None:
        """Load sumproduct specifications from a pandas dataframe.

        Args:
            data (pd.DataFrame): Dataframe of sumproduct specifications.
        """
        lc.load_sump(self, data=data)

    def load_raw_data(
        self,
        data: pd.DataFrame,
        idx: str,
        value: str,
        groups: tuple[str, ...],
        newvalue: str,
    ) -> None:
        """Load the data for processing.

        Args:
            data (pd.DataFrame): Dataframe to process.
            idx (str): Column with the index used for calculations.
            value (str): Column with values used for calculations.
            groups (Iterable[str]): Columns making up a composite key.
            newvalue (str): New column for calculated values.
        """
        self.raw_vars = vars.Raw(groups=groups, idx=idx, value=value, newvalue=newvalue)
        self.raw: pd.DataFrame = pd.DataFrame()


        data = lrd.load_raw_data(self, data=data)
        self.raw = data


    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None) -> None:
        """Load combinations from Excel to a pandas dataframe.

        Args:
            path (Path): Full filename of excel file.
            sheet_nm (str | None, optional): Name of excel sheet. Defaults to None.
        """
        df = lmx.load_mat_from_xl(self, path=path, sheet_nm=sheet_nm)
        self.load_sump(df)

    def get_invalid_data(self) -> None:
        self.invalid: pd.DataFrame = gid.get_invalid_data(self)

    def fit_transform(
        self, is_fillna: bool, is_merged: bool, verbose: bool = False
    ) -> None:
        """Process the fit and transform steps in a sequence.

        Args:
            is_merged (bool, optional): If True, merge the calculated data to the original dataframe. Otherwise, don't do it.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.fit(is_fillna=is_fillna, verbose=verbose)
        self.transform(is_merged=is_merged, verbose=verbose)

    def fit(self, is_fillna: bool, verbose: bool = False) -> None:
        """Fit the data. Find invalid and undetermined data.

        Args:
            is_fillna (bool): If True, replace missing values by zero. If False, eliminate rows summprod that have invalid input, e.g. when computing period values.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        if is_fillna:
            self.fillna()
            self.invalid = pd.DataFrame()
        else:
            self.get_invalid_data()
            self.get_valid_data()
        if verbose:
            rprint(f"{self.name} CalcSumprod.fit() completed.")

    def transform(self, is_merged: bool, verbose: bool = False) -> None:
        """Do the calculations.

        Args:
            is_merged (bool, optional): If True, merge the calculated data to the original dataframe. Otherwise, don't do it.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.calculate()
        if is_merged:
            self.output = self.add_calc()
        else:
            self.output = self.calc
        if verbose:
            rprint(f"{self.name} CalcSumprod.transform() completed.")

    def get_valid_data(self) -> None:
        try:
            self.valid = gvd.get_valid_data(self)
        except AttributeError as e:
            msg: str = "Attribute Error: Are you sure you ran fit()?"
            e.add_note(msg)
            raise

    def fillna(self) -> None:
        self.valid = gvd.fill_na(self)

    def calculate(self) -> None:
        """Calculate sumprods."""
        self.calc = calc.calculate(self)

    def add_calc(self) -> pd.DataFrame:
        return ac.add_calc(self)

    def get_summary(self) -> dict[str, tuple[int, ...]]:
        summary = {
            "raw data": self.raw.shape,
            "sumprod": self.sump.shape,
            "invalid": self.invalid.shape,
            "valid": self.valid.shape,
            "calculated": self.calc.shape,
            "output": self.output.shape,
        }
        return summary

    def to_excel(self, path: Path) -> None:
        dfs = {
            "raw data": self.raw,
            "sumprod_df": self.sump,
            "invalid_data": self.invalid,
            "valid_data": self.valid,
            "calc_data": self.calc,
            "output": self.output,
        }
        name = f"{type(self).__name__} '{self.name}'"
        xl.to_excel(name, path=path, dfs=dfs)
