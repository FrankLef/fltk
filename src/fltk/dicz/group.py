from collections.abc import ValuesView, Sequence
from typing import Any, Self, NamedTuple
from copy import deepcopy

from .abc import DiczBase
from .line import DiczLine
from .enums import DiczVar as vars
from .get_namestupl import main as nmstupl


class DiczGroup(DiczBase):
    def __init__(self, key: str):
        self.key = key
        self.coll: dict[str, DiczLine] = {}

    @property
    def info(self) -> dict[str, str | int]:
        info: dict[str, str | int] = {
            "key": self.key,
            "nlines": str(self.nlines),
            "nitems": str(self.nitems),
        }
        return info

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
    def keys(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

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
        except KeyError as e:
            e.add_note(f"'{key}' is an invalid line key.")
            raise
        return a_line

    def filter(self, line_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: new_self.coll[key] for key in line_nms}
        new_self.coll = coll
        return new_self

    def filter_pattern(self, item_nm: str, pattern: str) -> Self:
        """Filter the lines using the value of a given item.

        Args:
            item_nm (str): Name of the item.
            pattern (str): Pattern used to select the item.

        Returns:
            Self: Filtered dicz_group.
        """
        line_nms = [
            key
            for key, val in self.coll.items()
            if val.is_matched(item_nm=item_nm, pattern=pattern)
        ]
        new_self: Self = self.filter(line_nms)
        return new_self

    def filter_role(self, role: str) -> Self:
        new_self: Self = self.filter_pattern(item_nm=vars.ROLE, pattern=role)
        return new_self

    def filter_rule(self, rule: str) -> Self:
        new_self: Self = self.filter_pattern(item_nm=vars.RULE, pattern=rule)
        return new_self

    def lines_value(
        self, line_keys: Sequence[str] | None, item_nm: str
    ) -> dict[str, Any]:
        if line_keys:
            values: dict[str, Any] = {
                key: self.coll[key].item(item_nm).value for key in line_keys
            }
        else:
            values = {
                key: self.coll[key].item(item_nm).value for key in self.coll.keys()
            }
        return values

    def lines_tag(
        self, line_keys: Sequence[str] | None, item_nm: str, default: dict[str, Any]
    ) -> dict[str, Any]:
        if line_keys:
            tags: dict[str, Any] = {
                key: self.coll[key].item(item_nm).split_tag(default=default)
                for key in line_keys
            }
        else:
            tags = {
                key: self.coll[key].item(item_nm).split_tag(default=default)
                for key in self.coll.keys()
            }
        return tags
