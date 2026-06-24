from collections.abc import KeysView
from .dicz_item import DiczItem


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

    def append(self, item: DiczItem):
        self.coll[item.key] = item

    def item(self, key) -> DiczItem:
        try:
            a_item = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid item key.")
        return a_item
