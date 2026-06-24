import pandas as pd

from .dicz_bag import DiczBag
from .dicz_group import DiczGroup
# from .dicz_line import DiczLine
# from .dicz_item import DiczItem

from . import get_dicts
from . import get_bag

# type NamesArg = str | list[str] | None
type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


class Dicz:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "name": self.name,
            "ngroups": str(self.ngroups),
            "nlines": str(self.nlines),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    def build(self, data: pd.DataFrame) -> None:
        self.get_dicts(data)
        self.get_bag()

    def get_dicts(self, data: pd.DataFrame) -> None:
        self.dicts: GroupDict = get_dicts.main(data)
        self.ngroups = len(self.dicts)
        self.nlines = sum([len(x) for x in self.dicts.values()])

    def get_bag(self) -> None:
        bag: DiczBag = get_bag.main(self.dicts)
        is_err: bool = bag.nlines != self.nlines
        if is_err:
            msg: str = (
                f"Data has {self.nlines} lines but the bag has {bag.nlines} lines."
            )
            raise AssertionError(msg)
        self.bag: DiczBag = bag

    def group(self, key: str) -> DiczGroup:
        return self.bag.group(key)
