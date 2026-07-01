#  Iterable imported from collections with Python 3.9+
# with string, it is preferable to use Sequence. Otherwise a string is also an Iterable and the type checker will not consider a single string as invali
from collections.abc import ValuesView, Sequence
from typing import Self
from copy import deepcopy
from .abc import DiczBase
from .item import DiczItem


class DiczLine(DiczBase):
    def __init__(self, key: str):
        self.key = key
        self.coll: dict[str, DiczItem] = {}

    @property
    def info(self) -> dict[str, str | int]:
        info: dict[str, str | int] = {
            "key": self.key,
            "nitems": self.nitems,
        }
        return info

    @property
    def nitems(self) -> int:
        return len(self.coll)

    @property
    def empty(self) -> bool:
        return not self.nitems

    @property
    def keys(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

    @property
    def values(self) -> ValuesView:
        return self.coll.values()

    def append(self, item: DiczItem):
        self.coll[item.key] = item

    def item(self, key) -> DiczItem:
        try:
            a_item = self.coll[key]
        except KeyError as e:
            e.add_note(f"'{key}' is an invalid item key.")
            raise
        return a_item

    def filter(self, item_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: new_self.coll[key] for key in item_nms}
        new_self.coll = coll
        return new_self

    def is_matched(self, item_nm: str, pattern: str) -> bool:
        a_item = self.item(item_nm)
        is_matched = a_item.is_matched(pattern)
        return is_matched
