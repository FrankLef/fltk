from __future__ import annotations  # Must be at the top
import pandas as pd
from typing import Literal, Final

from rich import print as rprint

from ..calc.abc import Calc
from ..utils.value_cls import StrName

from . import vars
from . import load_raw_data as lrd
from . import base
from . import wfall


class CalcWaterfall(Calc):
    def __init__(
        self,
        name: str,
        initial=Literal["absolute", "relative"],
        diff_nm: str = "diff_nm",
        diff_val: str = "diff_val",
        wfall_type="wfall_type",
        wfall_amt: str = "wfall_amt",
        is_initial: str = "is_initial",
    ):
        super().__init__(StrName(name))
        self.wfall_vars = vars.WaterfallVars(
            initial=str(StrName(initial)),
            diff_nm=str(StrName(diff_nm)),
            diff_val=str(StrName(diff_val)),
            wfall_type=str(StrName(wfall_type)),
            wfall_amt=str(StrName(wfall_amt)),
            is_initial=str(StrName(is_initial)),
        )
        self.INITIAL: Final[str] = "initial"

    def load_raw_data(
        self,
        data: pd.DataFrame,
        groups: tuple[str, ...],
        period_from: str,
        period_to: str,
        ratio_nm: str,
        num_from_val: str,
        num_to_val: str,
        volume_diff: str,
        price_diff: str,
        mix_diff: str,
        total_diff: str,
    ) -> None:
        self.raw_vars = vars.RawVars(
            groups=groups,
            period_from=str(StrName(period_from)),
            period_to=str(StrName(period_to)),
            ratio_nm=str(StrName(ratio_nm)),
            num_from_val=str(StrName(num_from_val)),
            num_to_val=str(StrName(num_to_val)),
            volume_diff=str(StrName(volume_diff)),
            price_diff=str(StrName(price_diff)),
            mix_diff=str(StrName(mix_diff)),
            total_diff=str(StrName(total_diff)),
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
        self.wfall = wfall.get_wfall(self)
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self.name} {type_nm}.transform() completed.")

    @property
    def dfs(self):
        dfs = {
            "raw": self.raw,
            "base": self.base,
            "wfall": self.wfall,
        }
        return dfs
