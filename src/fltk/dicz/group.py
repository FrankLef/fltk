from collections.abc import KeysView, ValuesView, Sequence
from typing import Any, NamedTuple

from .line import DiczLine
from .enums import DiczVar as vars
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
        """Filter the lines using the value of a given item.

        Args:
            item_nm (str): Name of the item.
            pattern (str): Pattern used to select the item.

        Returns:
            Any: A dicz_group.
        """
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

    def get_many_lines_value(
        self, line_keys: Sequence[str], item_nm: str
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for line_key in line_keys:
            a_item = self.coll[line_key].item(item_nm)
            values[line_key] = a_item.value
        return values

    def get_many_lines_tag(
        self, line_keys: Sequence[str], item_nm: str, default: dict[str, Any]
    ) -> dict[str, Any]:
        tags: dict[str, Any] = {}
        for line_key in line_keys:
            tag = self.coll[line_key].item(item_nm).split_tag(default=default)
            tags[line_key] = tag
        return tags
