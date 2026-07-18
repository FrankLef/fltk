from collections.abc import Sequence
from typing import Self
from copy import deepcopy
from .base import DiczBase
from .group import DiczGroup


class DiczBag(DiczBase):
    def __init__(self, key: str) -> None:
        super().__init__(key=key)
        self.coll: dict[str, DiczGroup] = {}

    @property
    def info(self) -> dict[str, int]:
        info = {
            "ngroups": self.ngroups,
            "nlines": self.nlines,
        }
        return info

    @property
    def ngroups(self) -> int:
        return len(self.coll)

    @property
    def nlines(self) -> int:
        nlines = sum([x.nlines for x in self.coll.values()])
        return nlines

    @property
    def empty(self) -> bool:
        return not self.ngroups

    @property
    def keys(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

    def append(self, item: DiczGroup):
        self.coll[item.key] = item

    def group(self, key) -> DiczGroup:
        try:
            a_group = self.coll[key]
        except KeyError as e:
            e.add_note(f"'{key}' is an invalid group key.")
            raise
        return a_group

    def groups(self, group_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: self.group(key) for key in group_nms}
        new_self.coll = coll
        return new_self
