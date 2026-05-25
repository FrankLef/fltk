from typing import NamedTuple


class RawVars(NamedTuple):
    groups: tuple[str, ...]
    period: str
    values: tuple[str, ...]
    values_ewm: dict[str, str]

    @property
    def keys(self) -> str | tuple[str, ...]:
        keys = (*self.groups, self.period)
        return keys

    @property
    def vars(self) -> tuple[str, ...]:
        vars = (*self.keys, *self.values)
        return vars


class EwmVars(NamedTuple):
    suffix: str
    span: int
