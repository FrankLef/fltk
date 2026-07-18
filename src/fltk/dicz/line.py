from collections.abc import Sequence
from typing import Self, Any
from copy import deepcopy
from .base import DiczBase
from .item import DiczItem


class DiczLine(DiczBase):
    def __init__(self, key: str):
        super().__init__(key=key)
        self.coll: dict[str, DiczItem] = {}

    @property
    def info(self) -> dict[str, int]:
        info = {
            "nitems": self.nitems,
        }
        return info

    @property
    def nitems(self) -> int:
        # NOTE: Total includes the `skipped` column if loaded.
        return len(self.coll)

    @property
    def empty(self) -> bool:
        return not self.nitems

    @property
    def keys(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

    def append(self, item: DiczItem):
        self.coll[item.key] = item

    def item(self, item_nm: str) -> DiczItem:
        try:
            a_item = self.coll[item_nm]
        except KeyError as e:
            e.add_note(f"'{item_nm}' is an invalid item key.")
            raise
        return a_item

    def items(self, item_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: self.item(key) for key in item_nms}
        new_self.coll = coll
        return new_self

    def value(self, item_nm: str) -> Any:
        a_value = self.item(item_nm).value
        return a_value

    def values(self, item_nms: Sequence[str]) -> dict[str, Any]:
        values = {key: self.value(key) for key in item_nms}
        return values

    def filter(self, item_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: new_self.item(key) for key in item_nms}
        new_self.coll = coll
        return new_self

    def is_matched(self, item_nm: str, pattern: str) -> bool:
        a_item = self.item(item_nm)
        is_matched = a_item.is_matched(pattern)
        return is_matched
