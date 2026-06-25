#  Iterable imported from collections with Python 3.9+
# with string, it is preferable to use Sequence. Otherwise a string is also an Iterable and the type checker will not consider a single string as invali
from collections.abc import KeysView, ValuesView, Sequence
from typing import Any
from .item import DiczItem


class DiczLine:
    def __init__(self, key: str):
        self.key = key
        self.coll: dict[str, DiczItem] = {}

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "key": self.key,
            "nitems": str(self.nitems),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    @property
    def nitems(self) -> int:
        return len(self.coll)

    @property
    def empty(self) -> bool:
        return not self.nitems

    @property
    def keys(self) -> KeysView:
        return self.coll.keys()

    @property
    def values(self) -> ValuesView:
        return self.coll.values()

    def append(self, item: DiczItem):
        self.coll[item.key] = item

    def item(self, key) -> DiczItem:
        try:
            a_item = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid item key.")
        return a_item

    def filter(self, item_nms: Sequence[str]) -> Any:
        """Filter the items using item names.

        This is not the same as the filter for dicz_group.

        Args:
            item_nms (Sequence[str]): Iterable of item names.

        Returns:
            Any: A dicz_line
        """
        dicz_line = DiczLine(key=self.key)
        for nm in item_nms:
            dicz_line.append(self.item(nm))
        return dicz_line

    def is_matched(self, item_nm: str, pattern: str) -> bool:
        a_item = self.item(item_nm)
        is_matched = a_item.is_matched(pattern)
        return is_matched
