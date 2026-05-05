from __future__ import annotations  # Must be at the top
import pandas as pd

from pathlib import Path
from rich import print as rprint

from ..utils.value_cls import StrName
from ..utils import to_excel as xl

from . import vars
from . import load_raw_data as lrd
from . import load_ratios as lr
from . import periods as per
from . import bridge
from . import calculate as calc


class CalcBridge:
    def __init__(
        self,
        name: str,
        period_start: str = "period_start",
        period_end: str = "period_end",
        from_sfx: str = "from",
        to_sfx: str = "to",
        volume_diff: str = "vol_diff",
        price_diff: str = "price_diff",
        mix_diff: str = "mix_diff",
        total_diff: str = "tot_diff",
        total_check: str = "tot_check",
        check_diff: str = "check_diff",
        err: str = "err",
    ):
        self.name = StrName(name)
        self.periods_vars = vars.Periods(
            start=str(StrName(period_start)), end=str(StrName(period_end))
        )
        self.bridge_vars = vars.Bridge(
            from_sfx=str(StrName(from_sfx)),
            to_sfx=str(StrName(to_sfx)),
            volume_diff=str(StrName(volume_diff)),
            price_diff=str(StrName(price_diff)),
            mix_diff=str(StrName(mix_diff)),
            total_diff=str(StrName(total_diff)),
            total_check=str(StrName(total_check)),
            check_diff=str(StrName(check_diff)),
            err=str(StrName(err)),
        )

    def __repr__(self):
        summary = self.get_summary()
        title = f"{type(self).__name__}: {self.name}"
        out = title + "\n" + ("-" * len(title)) + "\n"
        for key, value in summary.items():
            out += f"{key:<10}: {value}\n"
        return out

    def add_suffix(self, var: str) -> tuple[str, str]:
        out = (
            var + "_" + self.bridge_vars.from_sfx,
            var + "_" + self.bridge_vars.to_sfx,
        )
        return out

    def load_ratios(self, data: pd.DataFrame, ratio_nm: str, num_nm: str, den_nm: str):
        self.ratios_vars = vars.Ratios(ratio_nm=ratio_nm, num_nm=num_nm, den_nm=den_nm)
        self.ratios = lr.load_ratios(self, data=data)

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
        self.raw_vars = vars.Raw(
            groups=groups,
            period=period,
            ratio_nm=ratio_nm,
            ratio_val=ratio_val,
            num_nm=num_nm,
            num_val=num_val,
            den_nm=den_nm,
            den_val=den_val,
        )
        self.raw = lrd.load_raw_data(self, data=data)

    def get_periods(self) -> None:
        self.periods = per.get_periods(self)

    def get_bridge(self) -> None:
        self.bridge = bridge.get_bridge(self)

    def calculate(self) -> None:
        self.bridge = calc.calculate(self)

    def fit_transform(self, verbose: bool = False) -> None:
        self.fit(verbose=verbose)
        self.transform(verbose=verbose)

    def fit(self, verbose: bool = False) -> None:
        self.get_periods()
        self.get_bridge()
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self.name} {type_nm}.fit() completed.")

    def transform(self, verbose: bool = False) -> None:
        self.calculate()
        if verbose:
            type_nm = type(self).__name__
            rprint(f"{self.name} {type_nm}.transform() completed.")

    def get_summary(self) -> dict[str, tuple[int, ...]]:
        summary = {
            "raw data": self.raw.shape,
            "ratios": self.ratios.shape,
            "periods": self.periods.shape,
            "bridge": self.bridge.shape,
        }
        return summary

    def to_excel(self, path: Path) -> None:
        dfs = {
            "raw": self.raw,
            "ratios": self.ratios,
            "periods": self.periods,
            "bridge": self.bridge,
        }
        name = f"{type(self).__name__} '{self.name}'"
        xl.to_excel(name, path=path, dfs=dfs)
