from __future__ import annotations  # Must be at the top
import pandas as pd

from pathlib import Path
from rich import print as rprint

from fltk.utils.value_cls import StrName

from . import vars
from . import load_raw_data as lrd
from . import load_ratios as lr
from . import periods as per
from . import bridge
from . import calculate as calc
from . import to_excel as xl


class CalcBridge:
    def __init__(
        self,
        name: str,
        period_start: str = "period_start",
        period_end: str = "period_end",
        price: str = "price",
        from_sfx: str = "from",
        to_sfx: str = "to",
    ):
        self._name = StrName(name)
        self.periods = vars.Periods(
            start=str(StrName(period_start)), end=str(StrName(period_end))
        )
        self.bridge = vars.Bridge(
            price=str(StrName(price)),
            from_sfx=str(StrName(from_sfx)),
            to_sfx=str(StrName(to_sfx)),
        )

    def __repr__(self):
        summary = self.get_summary()
        title = f"{type(self).__name__}: {self.name}"
        out = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in summary.items():
            out += f"{key:<10}: {value}\n"
        return out

    @property
    def name(self) -> str:
        return self._name

    def load_ratios(self, data: pd.DataFrame, ratio_nm: str, num_nm: str, den_nm: str):
        self.ratios = vars.Ratios(ratio_nm=ratio_nm, num_nm=num_nm, den_nm=den_nm)
        self.ratios_df = lr.load_ratios(self, data=data)

    def load_raw_data(
        self,
        data: pd.DataFrame,
        groups: tuple[str, ...],
        period: str,
        ratio_nm: str,
        ratio_val: str,
        num_nm: str,
        num_val: str,
        den_nm: str,
        den_val: str,
    ) -> None:
        self.raw = vars.Raw(
            groups=groups,
            period=period,
            ratio_nm=ratio_nm,
            ratio_val=ratio_val,
            num_nm=num_nm,
            num_val=num_val,
            den_nm=den_nm,
            den_val=den_val,
        )
        self.raw_df = lrd.load_raw_data(self, data=data)

    def get_periods(self) -> None:
        self.periods_df = per.get_periods(self)

    def get_bridge(self) -> None:
        self.bridge_df = bridge.get_bridge(self)

    def calculate(self) -> None:
        self.bridge_df = calc.calculate(self)

    def fit_transform(self, verbose: bool = False) -> None:
        self.fit(verbose=verbose)
        self.transform(verbose=verbose)

    def fit(self, verbose: bool = False) -> None:
        self.get_periods()
        self.get_bridge()
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self._name} {type_nm}.fit() completed.")

    def transform(self, verbose: bool = False) -> None:
        self.calculate()
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self._name} {type_nm}.transform() completed.")

    def get_summary(self) -> dict[str, int]:
        summary = {
            "raw data": self.ratios_df.shape,
            "ratios": self.raw_df.shape,
            "periods": self.periods_df.shape,
            "bridge": self.bridge_df.shape,
        }
        return summary

    def to_excel(self, path: Path) -> None:
        dfs = {
            "raw": self.raw_df,
            "ratios": self.ratios_df,
            "periods": self.periods_df,
            "bridge": self.bridge_df,
        }
        xl.to_excel(self.name, path=path, dfs=dfs)
