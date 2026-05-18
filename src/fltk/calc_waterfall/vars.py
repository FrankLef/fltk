from typing import NamedTuple


class RawVars(NamedTuple):
    groups: tuple[str, ...]
    period_from: str
    period_to: str
    ratio_nm: str
    num_from_val: str
    num_to_val: str
    volume_diff: str
    price_diff: str
    mix_diff: str
    total_diff: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        keys = (*self.groups, self.ratio_nm, self.period_from, self.period_to)
        return keys

    @property
    def factors(self) -> tuple[str, ...]:
        vars = (
            self.num_from_val,
            self.num_to_val,
            self.volume_diff,
            self.price_diff,
            self.mix_diff,
            self.total_diff,
        )
        return vars

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, *self.factors)
        return vars


class WaterfallVars(NamedTuple):
    initial: str
    diff_nm: str
    diff_val: str
    wfall_type: str
    wfall_amt: str
    is_initial: str

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (
            self.diff_nm,
            self.diff_val,
            self.wfall_type,
            self.wfall_amt,
            self.is_initial,
        )
        return vars
