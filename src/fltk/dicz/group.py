from collections.abc import Sequence
from typing import Any, NamedTuple

from .base import DiczBase, DiczVar as vars
from .line import DiczLine
from .get_namestupl import main as nmstupl

type DiczLines = tuple[DiczLine, ...]
type DiczNames = tuple[str, ...]


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

    def lines(self, line_nms: Sequence[str] | None = None) -> DiczLines:
        if line_nms:
            the_lines = tuple(self.line(key) for key in line_nms)
        else:
            the_lines = tuple(self.coll.values())
        return the_lines

    def filter_pattern(self, item_nm: str, pattern: str) -> tuple[str, ...]:
        """Filter the lines using the value of a given item.

        Args:
            item_nm (str): Name of the item.
            pattern (str): Pattern used to select the item.

        Returns:
            Self: Filtered dicz_group.
        """
        line_nms = tuple(
            key
            for key, val in self.coll.items()
            if val.is_matched(item_nm=item_nm, pattern=pattern)
        )
        # the_lines = self.lines(line_nms)
        return line_nms

    def filter_role(self, role: str, names_only: bool = False) -> DiczLines | DiczNames:
        line_nms = self.filter_pattern(item_nm=vars.ROLE, pattern=role)
        if not names_only:
            out: DiczLines | DiczNames = self.lines(line_nms)
        else:
            out = line_nms
        return out

    def filter_rule(self, rule: str, names_only: bool = False) -> DiczLines | DiczNames:
        line_nms = self.filter_pattern(item_nm=vars.RULE, pattern=rule)
        if not names_only:
            out: DiczLines | DiczNames = self.lines(line_nms)
        else:
            out = line_nms
        return out

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
