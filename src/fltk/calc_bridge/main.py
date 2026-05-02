from __future__ import annotations  # Must be at the top
import pandas as pd
# from pathlib import Path
from rich import print as rprint
# from rich.pretty import pprint
# from rich.console import Console

from fltk.utils.value_cls import StrName

from . import load_data as ld


class CalcBridge:
    def __init__(
        self,
        name: str,
        base_var: str = "base",
        price_var: str = "price",
        from_sfx: str = "from",
        to_sfx: str= "to",
    ):
        self._name = StrName(name)
        self.__base_var = StrName(base_var)
        self.__price_var = StrName(price_var)
        self._from_sfx = str(StrName(from_sfx)),
        self._to_sfx = str(StrName(to_sfx))
    
    @property 
    def name(self) -> str:
        return self._name

    def load_data(
        self,
        data: pd.DataFrame,
        groups: list[str],
        period: str,
        ratio: str,
        from_nm: str,
        to_nm: str,
        from_value: str,
        to_value: str,
    ) -> None:
        self._groups = [str(StrName(var)) for var in groups]
        self._period = str(StrName(period))
        self._ratio = str(StrName(ratio))
        self._from_nm = str(StrName(from_nm))
        self._to_nm = str(StrName(to_nm))
        self._from_value = str(StrName(from_value))
        self._to_value = str(StrName(to_value))
        
        self._data_keys = groups + [period, ratio]
        self._data_vars = self._data_keys + [from_nm, to_nm, from_value, to_value]
        
        self._data = ld.load_data(self, data=data)

    def fit_transform(self, verbose: bool = False) -> None:
        self.fit(verbose=verbose)
        self.transform(verbose=verbose)

    def fit(self, verbose: bool = False) -> None:
        if verbose:
            rprint(f"{self._name} CalcSumprod.fit() completed.")

    def transform(self, verbose: bool = False) -> None:
        # self.calculate()
        if verbose:
            rprint(f"{self._name} CalcBridge.transform() completed.")