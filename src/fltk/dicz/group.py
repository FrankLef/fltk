from collections.abc import Sequence
from typing import Any, Self, NamedTuple
from copy import deepcopy

from .base import DiczBase, DiczVar as vars
from .line import DiczLine
from .get_namestupl import main as nmstupl


class DiczGroup(DiczBase):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.coll: dict[str, DiczLine] = {}

    @property
    def info(self) -> dict[str, int]:
        info = {
            "nlines": self.nlines,
            "nitems": self.nitems,
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
    def line_nms(self) -> tuple[str, ...]:
        # must return tuple
        return tuple(self.coll.keys())

    @property
    def names_tupl(self) -> NamedTuple:
        names_tupl = nmstupl(group_nm=self.name, line_nms=self.line_nms)
        return names_tupl

    def append(self, dicz_obj: DiczLine):
        self.coll[dicz_obj.name] = dicz_obj

    def line(self, line_nm: str) -> DiczLine:
        try:
            a_line = self.coll[line_nm]
        except KeyError as e:
            e.add_note(f"'{line_nm}' is an invalid dicz line name.")
            raise
        return a_line

    def lines(self, line_nms: Sequence[str]) -> Self:
        new_self = deepcopy(self)
        coll = {key: self.line(key) for key in line_nms}
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
        new_self: Self = self.lines(line_nms)
        return new_self

    def filter_role(self, role: str) -> Self:
        new_self: Self = self.filter_pattern(item_nm=vars.ROLE, pattern=role)
        return new_self

    def filter_rule(self, rule: str) -> Self:
        new_self: Self = self.filter_pattern(item_nm=vars.RULE, pattern=rule)
        return new_self

    def lines_value(
        self, line_nms: Sequence[str] | None, item_nm: str
    ) -> dict[str, Any]:
        if line_nms:
            values: dict[str, Any] = {
                key: self.line(key).value(item_nm) for key in line_nms
            }
        else:
            values = {key: self.line(key).value(item_nm) for key in self.coll.keys()}
        return values

    def lines_tag(
        self, line_nms: Sequence[str] | None, item_nm: str, default: dict[str, Any]
    ) -> dict[str, Any]:
        if line_nms:
            tags: dict[str, Any] = {
                key: self.line(key).item(item_nm).split_tag(default=default)
                for key in line_nms
            }
        else:
            tags = {
                key: self.line(key).item(item_nm).split_tag(default=default)
                for key in self.coll.keys()
            }
        return tags
