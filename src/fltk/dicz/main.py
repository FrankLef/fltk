import polars as pl


from .bag import DiczBag

from .abc import DiczBase
from . import get_bag


class Dicz(DiczBase):
    def __init__(self, key: str):
        super().__init__(key=key)
        self.coll: dict[str, DiczBag] = {}

    @property
    def info(self) -> dict[str, str | int]:
        info: dict[str, str | int] = {
            "nbags": str(self.nbags),
        }
        return info

    @property
    def nbags(self) -> int:
        return len(self.coll)

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
