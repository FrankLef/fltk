import pandas as pd


from .bag import DiczBag

from .abc import DiczBase
from . import get_bag


class Dicz(DiczBase):
    def __init__(self, name: str):
        self.name: str = name
        self.coll: dict[str, DiczBag] = {}

    @property
    def info(self) -> dict[str, str | int]:
        info: dict[str, str | int] = {
            "name": self.name,
            "nbags": str(self.nbags),
        }
        return info

    @property
    def nbags(self) -> int:
        return len(self.coll)

    def append(self, key: str, data: pd.DataFrame):
        bag: DiczBag = get_bag.main(key=key, data=data)
        self.coll[bag.key] = bag

    def bag(self, key) -> DiczBag:
        try:
            a_bag = self.coll[key]
        except KeyError as e:
            e.add_note(f"'{key}' is an invalid bag key.")
            raise
        return a_bag
