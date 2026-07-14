import polars as pl
from pathlib import Path

from ..base import Mung
from ...utils.value_cls import StrName

from . import vars
from . import load_mat_xl as lmx
from . import load_sump as lc
from . import load_raw_data as lrd
from .calculate import calculate as calc


class MungSumprod(Mung):
    def __init__(
        self,
        name: str,
        idx_to: str = "idx_to",
        idx_from: str = "idx_from",
        sump_coef: str = "sump_coef",
        sump_value: str = "sump_value",
    ):
        """_summary_

        Args:
            name (str): Name to identify the object. Does not affect the process itself.
            idx_to (str, optional): Name of the column with the target index used. Same as the upper left corner of the matrix. Defaults to "idx_to".
            idx_from (str, optional): Name of the column with the source index used. It is recommended to keep the default value. Defaults to "idx_from".
            sump_coef (str, optional): Column of coefficients to use. It is recommended to keep the default value. Defaults to "sump_coef".
            sump_value (str, optional): Column of values to use. It is recommended to keep the default value. Defaults to "sump_value".
        """
        super().__init__(StrName(name))
        self.sump_vars = vars.SumprodVars(
            idx_to=StrName(idx_to),
            idx_from=StrName(idx_from),
            sump_coef=StrName(sump_coef),
            sump_value=StrName(sump_value),
        )
        self.sump = pl.DataFrame()

    def _init_sump_vars(self) -> None:
        self._sump_vars: list[str] = []
        self._sump_keys: list[str] = []
        self._sump_vars_base: list[str] = []

    def load_sump(self, data: pl.DataFrame) -> None:
        """Load sumproduct specifications from a pandas dataframe.

        Args:
            data (pl.DataFrame): Dataframe of sumproduct specifications.
        """
        lc.load_sump(self, data=data)

    def load_raw_data(
        self,
        data: pl.DataFrame,
        idx: str,
        value: str,
        groups: tuple[str, ...],
        newvalue: str,
    ) -> None:
        """Raw data to process.

        Args:
            data (pl.DataFrame): Raw data dataframe.
            idx (str): Column with the concept used for calcXulations.
            value (str): Column with values used for calcXulations.
            groups (tuple[str, ...]): Columns making up a composite key.
            newvalue (str): _description_Column with calcXulated ratio value.
        """
        self.raw_vars = vars.RawVars(
            groups=groups, idx=idx, value=value, newvalue=newvalue
        )
        self.raw: pl.DataFrame = pl.DataFrame()

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

    def fit_transform(self, missing_to_zero: bool) -> None:
        """Process the fit and transform steps in a sequence.

        Args:
            is_merged (bool, optional): If True, merge the calcXulated data to the original dataframe. Otherwise, don't do it.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.fit()
        self.transform(missing_to_zero=missing_to_zero)

    def fit(self) -> None:
        """Fit the data."""
        # Not used.

    def transform(self, missing_to_zero: bool) -> None:
        """Do the calcXulations."""
        self.calculate(missing_to_zero=missing_to_zero)

    def calculate(self, missing_to_zero: bool) -> None:
        data = self.raw
        sump_df = self.sump
        calc_df = calc(
            data,
            sumprod=sump_df,
            raw_vars=self.raw_vars,
            sump_vars=self.sump_vars,
            missing_to_zero=missing_to_zero,
        )
        self.calc = calc_df

    @property
    def dfs(self):
        dfs = {
            "raw data": self.raw,
            "sump": self.sump,
            "calc": self.calc,
        }
        return dfs
