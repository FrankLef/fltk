import pandas as pd

from .bag import DiczBag
# from .dicz_group import DiczGroup
# from .dicz_line import DiczLine
# from .dicz_item import DiczItem

# from . import get_dicts
from . import get_bag

# type NamesArg = str | list[str] | None
type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


class Dicz:
    def __init__(self, name: str):
        self.name = name
        self.coll: dict[str, DiczBag] = {}

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "name": self.name,
            "nbags": str(self.nbags),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    @property
    def nbags(self) -> int:
        return len(self.coll)

    def append(self, key: str, data: pd.DataFrame):
        bag: DiczBag = get_bag.main(key=key, data=data)
        self.coll[bag.key] = bag

    def bag(self, key) -> DiczBag:
        try:
            a_bag = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid bag key.")
        return a_bag
