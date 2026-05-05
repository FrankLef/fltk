from typing import NamedTuple


class Raw(NamedTuple):
    groups: tuple[str, ...]
    idx: str
    value: str
    newvalue: str

    @property
    def keys(self) -> str | tuple[str, ...]:
        keys = (*self.groups, self.idx)
        return keys

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, self.value, self.newvalue)
        return vars


class Sumprod(NamedTuple):
    idx_to: str
    idx_from: str
    sump_coef: str
    sump_value: str
    
    @property
    def keys(self) -> tuple[str, ...]:
        vars = (self.idx_to, self.idx_from)
        return vars
    
    @property
    def vars(self) -> tuple[str, ...]:
        vars = (
            self.idx_to,
            self.idx_from,
            self.sump_coef,
            self.sump_value,
        )
        return vars
    
    @property
    def base(self)->tuple[str,...]:
        vars=(self.idx_to, self.idx_from, self.sump_coef)
        return vars
