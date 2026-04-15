from __future__ import annotations  # Must be at the top
import pandas as pd
from pathlib import Path
from rich import print as rprint
from rich.pretty import pprint
from rich.console import Console

from fltk.utils.value_cls import StrName

from . import init_vars as iv
from . import load_mat_xl as lmx
from . import load_sump as lc
from . import load_data as ld
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
        self._name = StrName(name)
        self._idx_to = StrName(idx_to)
        self._idx_from = StrName(idx_from)
        self._sump_coef = StrName(sump_coef)
        self._sump_value = StrName(sump_value)
        self._sump_df = pd.DataFrame()
        self._init_sump_vars()

    def _init_sump_vars(self) -> None:
        self._sump_vars: list[str] = []
        self._sump_keys: list[str] = []
        self._sump_vars_base: list[str] = []
        iv._init_sump_vars(self)

    @property
    def sump_df(self) -> pd.DataFrame:
        """Dataframe of combinations' specifications."""
        return self._sump_df

    @property
    def data(self) -> pd.DataFrame:
        """Original data. Augmented with calculations if `is_merged` flag is True."""
        return self._data

    @property
    def invalid_data(self):
        """Dataframe of rows that cannot be calculated."""
        return self._invalid_data

    @property
    def valid_data(self):
        """Dataframe of rows without invalid rows. Used for be calulations."""
        return self._valid_data

    @property
    def calc_data(self):
        """Dataframe of calculated results."""
        return self._calc_data

    @property
    def output(self) -> pd.DataFrame:
        """Dataframe of final output data."""
        return self._output

    def load_sump(self, data: pd.DataFrame) -> None:
        """Load sumproduct specifications from a pandas dataframe.

        Args:
            data (pd.DataFrame): Dataframe of sumproduct specifications.
        """
        lc.load_sump(self, data=data)

    def load_data(
        self,
        data: pd.DataFrame,
        idx_var: str,
        value_var: str,
        group_vars: list[str],
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
        self._data_idx = str(StrName(idx_var))
        self._data_value = str(StrName(value_var))
        self._data_group = [str(StrName(var)) for var in group_vars]
        self._data_newvalue = str(StrName(newvalue_var))
        self._data: pd.DataFrame = pd.DataFrame()

        self._init_data_vars()

        data = ld.load_data(
            self,
            data=data,
            idx_var=idx_var,
            value_var=value_var,
            group_vars=group_vars,
            newvalue_var=newvalue_var,
        )
        self._data = data

    def _init_data_vars(self) -> None:
        """Initialize the variables."""
        self._data_vars: list[str] = []
        self._data_keys: list[str] = []
        iv._init_data_vars(self)

    def load_mat_from_xl(self, path: Path, sheet_nm: str | None = None) -> None:
        """Load combinations from Excel to a pandas dataframe.

        Args:
            path (Path): Full filename of excel file.
            sheet_nm (str | None, optional): Name of excel sheet. Defaults to None.
        """
        df = lmx.load_mat_from_xl(self, path=path, sheet_nm=sheet_nm)
        self.load_sump(df)

    def get_invalid_data(self) -> None:
        self._invalid_data: pd.DataFrame = gid.get_invalid_data(self)

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
            self._invalid_data = pd.DataFrame()
        else:
            self.get_invalid_data()
            self.get_valid_data()
        if verbose:
            rprint(f"{self._name} CalcSumprod.fit() completed.")

    def transform(self, is_merged: bool, verbose: bool = False) -> None:
        """Do the calculations.

        Args:
            is_merged (bool, optional): If True, merge the calculated data to the original dataframe. Otherwise, don't do it.
            verbose (bool, optional): If True, display info. Defaults to False.
        """
        self.calculate()
        if is_merged:
            self._output = self.add_calc()
        else:
            self._output = self._calc_data
        if verbose:
            rprint(f"{self._name} CalcSumprod.transform() completed.")

    def get_valid_data(self) -> None:
        try:
            self._valid_data = gvd.get_valid_data(self)
        except AttributeError as e:
            msg: str = "Attribute Error: Are you sure you ran fit()?"
            e.add_note(msg)
            raise

    def fillna(self) -> None:
        self._valid_data = gvd.fill_na(self)

    def calculate(self) -> None:
        """Calculate sumprods."""
        self._calc_data = calc.calculate(self)

    def add_calc(self) -> pd.DataFrame:
        return ac.add_calc(self)

    def summary(self, verbose: bool = True) -> dict[str, int]:
        nsump = self._sump_df.shape[0]
        ndata = self._data.shape[0]
        ninvalid = self._invalid_data.shape[0]
        nvalid = self._valid_data.shape[0]
        ncalc = self._calc_data.shape[0]
        noutput = self._output.shape[0]
        if verbose:
            out = {
                "sumprod": nsump,
                "data": ndata,
                "invalid": ninvalid,
                "valid": nvalid,
                "calculated": ncalc,
                "output": noutput,
            }
            pprint(out)
        return out

    def to_excel(self, path: Path) -> None:
        """Export data to excel.

        Args:
            path (Path): Path to excel file, including file name.
        """
        console = Console()
        msg: str = f"\n[bright_white]Exporting CalcRatio to:[/bright_white]\n[cyan]{path}[/cyan]"
        console.print(msg)
        rprint("'data'")
        self._data.to_excel(path, sheet_name="data", index=False, engine="openpyxl")
        with pd.ExcelWriter(
            path, mode="a", engine="openpyxl", if_sheet_exists="replace"
        ) as writer:
            dfs = {
                "sumprod_df": self._sump_df,
                "invalid_data": self._sump_df,
                "valid_data": self._valid_data,
                "calc_data": self._calc_data,
                "output": self._output,
            }
            for sheet_name, df in dfs.items():
                msg = f"'{sheet_name}'"
                rprint(msg)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
