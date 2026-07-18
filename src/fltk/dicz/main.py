from collections.abc import Sequence
import polars as pl


from .base import DiczBase, DiczNames
from .bag import DiczBag
from . import get_bag

type DiczBags = tuple[DiczBag, ...]


class Dicz(DiczBase):
    def __init__(self, name: str):
        super().__init__(name=name)
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
    def bag_nms(self) -> DiczNames:
        # must return tuple
        return tuple(self.coll.keys())

    def append(self, bag_nm: str, data: pl.DataFrame):
        bag: DiczBag = get_bag.main(bag_nm=bag_nm, data=data)
        self.coll[bag_nm] = bag

    def bag(self, bag_nm: str) -> DiczBag:
        try:
            a_bag = self.coll[bag_nm]
        except KeyError as e:
            e.add_note(f"'{bag_nm}' is an invalid dicz bag name.")
            raise
        return a_bag

    def bags(self, bag_nms: Sequence[str] | None = None) -> DiczBags:
        if bag_nms:
            the_bags = tuple(self.bag(key) for key in bag_nms)
        else:
            the_bags = tuple(self.coll.values())
        return the_bags
