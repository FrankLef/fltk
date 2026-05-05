from typing import NamedTuple


class Raw(NamedTuple):
    groups: tuple[str, ...]
    period: str
    ratio_nm: str
    ratio_val: str
    num_nm: str
    den_nm: str
    num_val: str
    den_val: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        keys = (*self.groups, self.period, self.ratio_nm)
        return keys

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (
            *self.keys,
            self.ratio_val,
            self.num_nm,
            self.num_val,
            self.den_nm,
            self.den_val,
        )
        return vars


class Periods(NamedTuple):
    start: str
    end: str


class Ratios(NamedTuple):
    ratio_nm: str
    num_nm: str
    den_nm: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        return self.ratio_nm

    @property
    def vars(self) -> tuple[str, ...]:
        if isinstance(self.keys, str):
            vars: tuple[str, ...] = (self.keys, self.num_nm, self.den_nm)
        else:
            vars = tuple(list(self.keys) + [self.num_nm, self.den_nm])
        return vars


class Bridge(NamedTuple):
    from_sfx: str
    to_sfx: str
    volume_diff: str
    price_diff: str
    mix_diff: str
    total_diff: str
    total_check: str
    check_diff: str
    err: str

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (
            self.volume_diff,
            self.price_diff,
            self.mix_diff,
            self.total_diff,
            self.total_check,
            self.check_diff,
            self.err,
        )
        return vars
