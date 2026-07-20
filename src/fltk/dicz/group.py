from collections.abc import Sequence
from typing import NamedTuple

from .base import DiczBase, DiczNames
from .line import DiczLine, DiczLines
from .processor import DiczProcessor
from .get_namestupl import main as nmstupl


class DiczGroup(DiczBase):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.coll: DiczLines = {}

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
    def line_nms(self) -> DiczNames:
        # must return tuple
        return tuple(self.coll.keys())

    @property
    def names_tupl(self) -> NamedTuple:
        names_tupl = nmstupl(group_nm=self.name, line_nms=self.line_nms)
        return names_tupl

    def append(self, dicz_obj: DiczLine):
        self.coll[dicz_obj.name] = dicz_obj

    def lines(self, line_nms: Sequence[str] | None = None) -> DiczProcessor:
        if line_nms:
            the_lines = {key: self.coll[key] for key in line_nms}
        else:
            the_lines = self.coll
        return DiczProcessor(the_lines)
