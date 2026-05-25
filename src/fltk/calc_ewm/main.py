import pandas as pd

from rich import print as rprint

from ..calc.abc import Calc
from ..utils.value_cls import StrName

from . import vars
from . import load_raw_data as lrd
from . import base
from . import ewm


class CalcEwm(Calc):
    def __init__(self, name: str, suffix: str = "ewm", span: int = 4):
        super().__init__(StrName(name))
        self.ewm_vars = vars.EwmVars(
            suffix=str(StrName(suffix)),
            span=self.assert_span(span),
        )

    def assert_span(self, span: int) -> int:
        if span < 2:
            msg: str = f"EWM span is {span}. It must be >= 2."
            raise ValueError(msg)
        return span

    def load_raw_data(
        self,
        data: pd.DataFrame,
        groups: tuple[str, ...],
        period: str,
        values: tuple[str, ...],
    ) -> None:
        self.raw_vars = vars.RawVars(
            groups=groups,
            period=str(StrName(period)),
            values=values,
        )
        self.raw = lrd.load_raw_data(self, data=data)

    def fit_transform(self, verbose: bool = False) -> None:
        self.fit(verbose=verbose)
        self.transform(verbose=verbose)

    def fit(self, verbose: bool = False) -> None:
        self.base = base.get_base(self)
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self.name} {type_nm}.fit() completed.")

    def transform(self, verbose: bool = False) -> None:
        self.ewm = ewm.get_ewm(self)
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self.name} {type_nm}.transform() completed.")

    @property
    def dfs(self):
        dfs = {
            "raw": self.raw,
            "base": self.base,
            "ewm": self.ewm,
        }
        return dfs
