from collections.abc import Sequence
from typing import Self
from copy import deepcopy
import polars as pl


from .bag import DiczBag

from .base import DiczBase
from . import get_bag


class Dicz(DiczBase):
    def __init__(self, key: str):
        super().__init__(key=key)
        self.coll: dict[str, DiczBag] = {}

    @property
    def info(self) -> dict[str, int]:
        info = {
            "nbags": self.nbags,
        }
        return info

    @property
    def nbags(self) -> int:
        return len(self.coll)

    @property
    def empty(self) -> bool:
        return not self.nbags

    @property
    def keys(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

    def append(self, key: str, data: pl.DataFrame):
        bag: DiczBag = get_bag.main(key=key, data=data)
        self.coll[bag.key] = bag

    def bag(self, key) -> DiczBag:
        try:
            a_bag = self.coll[key]
        except KeyError as e:
            e.add_note(f"'{key}' is an invalid bag key.")
            raise
        return a_bag

    def bags(self, bag_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: self.bag(key) for key in bag_nms}
        new_self.coll = coll
        return new_self
