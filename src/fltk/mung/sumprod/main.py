import polars as pl
from pathlib import Path
from rich import print as rprint

from ..abc import Mung
from ...utils.value_cls import StrName

from . import vars
from . import load_mat_xl as lmx
from . import load_sump as lc
from . import load_raw_data as lrd
from . import incomplete_sump as incomp
from . import incomplete_flag as incomp_flag

# from . import invalid_data as gid
# from . import valid_data as gvd
from . import calculate as calc
from . import add_calc as ac


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
            idx (str): Column with the concept used for calculations.
            value (str): Column with values used for calculations.
            groups (tuple[str, ...]): Columns making up a composite key.
            newvalue (str): _description_Column with calculated ratio value.
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

    def get_incomplete_sump(self) -> None:
        incomplete_dfs = incomp.get_incomplete_sump(self)
        self.incomplete = incomplete_dfs["incomplete"]
        self.incomplete_uniq = incomplete_dfs["incomplete_uniq"]
        # self.invalid: pl.DataFrame = gid.get_invalid_data(self)

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

    def fit(self, is_fillna: bool = False, verbose: bool = False) -> None:
        """Fit the data. Find invalid and undetermined data.

        Args:
            is_fillna (bool): If True, replace missing values by zero. If False, eliminate rows summprod that have invalid input, e.g. when computing period values.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.get_incomplete_sump()
        # if is_fillna:
        #     self.fillna()
        #     self.invalid = pl.DataFrame()
        # else:
        #     self.get_invalid_data()
        #     self.get_valid_data()
        # if verbose:
        #     rprint(f"{self.name} MungSumprod.fit() completed.")

    def transform(self, is_merged: bool, verbose: bool = False) -> None:
        """Do the calculations.

        Args:
            is_merged (bool, optional): If True, merge the calculated data to the original dataframe. Otherwise, don't do it.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.calculate()

        # if is_merged:
        #     self.output = self.add_calc()
        # else:
        #     self.output = self.calc
        # if verbose:
        #     rprint(f"{self.name} MungSumprod.transform() completed.")

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
        self.calc_aug = incomp_flag.flag_incomplete(self)

    def add_calc(self) -> pl.DataFrame:
        return ac.add_calc(self)

    @property
    def dfs(self):
        dfs = {
            "raw data": self.raw,
            "sumprod": self.sump,
            "incomplete": self.incomplete,
            "incomplete_uniq": self.incomplete_uniq,
            "calc": self.calc,
            "calc_aug": self.calc_aug,
        }
        return dfs
