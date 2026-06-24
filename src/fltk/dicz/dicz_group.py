from collections.abc import KeysView, ValuesView
from typing import Any, NamedTuple

from .dicz_line import DiczLine
from .dicz_enum import DiczVar as vars
from .get_namestupl import main as nmstupl


class DiczGroup:
    def __init__(self, key: str):
        self.key = key
        self.coll: dict[str, DiczLine] = {}

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "key": self.key,
            "nlines": str(self.nlines),
            "nitems": str(self.nitems),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    @property
    def nlines(self) -> int:
        return len(self.coll)

    @property
    def nitems(self) -> int:
        nitems = sum([x.nitems for x in self.coll.values()])
        return nitems

    @property
    def empty(self) -> bool:
        return not self.nlines

    @property
    def keys(self) -> KeysView:
        return self.coll.keys()

    @property
    def values(self) -> ValuesView:
        return self.coll.values()

    @property
    def names_tupl(self) -> NamedTuple:
        names_tupl = nmstupl(group_nm=self.key, line_keys=self.keys)
        return names_tupl

    def append(self, item: DiczLine):
        self.coll[item.key] = item

    def line(self, key) -> DiczLine:
        try:
            a_line = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid line key.")
        return a_line

    def filter(self, item_nm: str, pattern: str) -> Any:
        dicz_group = DiczGroup(key=self.key)
        for line_val in self.values:
            is_matched = line_val.is_matched(item_nm=item_nm, pattern=pattern)
            if is_matched:
                dicz_group.append(line_val)
        return dicz_group

    def filter_role(self, role: str) -> Any:
        a_group = self.filter(item_nm=vars.ROLE, pattern=role)
        return a_group

    def filter_rule(self, rule: str) -> Any:
        a_group = self.filter(item_nm=vars.RULE, pattern=rule)
        return a_group
