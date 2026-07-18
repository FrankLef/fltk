from collections.abc import Sequence

from .base import DiczBase, DiczNames
from .group import DiczGroup

type DiczGroups = tuple[DiczGroup, ...]


class DiczBag(DiczBase):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.coll: dict[str, DiczGroup] = {}

    @property
    def info(self) -> dict[str, int]:
        info = {
            "ngroups": self.ngroups,
            "nlines": self.nlines,
        }
        return info

    @property
    def ngroups(self) -> int:
        return len(self.coll)

    @property
    def nlines(self) -> int:
        nlines = sum([x.nlines for x in self.coll.values()])
        return nlines

    @property
    def empty(self) -> bool:
        return not self.ngroups

    @property
    def group_nms(self) -> DiczNames:
        # must return tuple
        return tuple(self.coll.keys())

    def append(self, dicz_obj: DiczGroup):
        self.coll[dicz_obj.name] = dicz_obj

    def group(self, group_nm: str) -> DiczGroup:
        try:
            a_group = self.coll[group_nm]
        except KeyError as e:
            e.add_note(f"'{group_nm}' is an invalid dicz group name.")
            raise
        return a_group

    def groups(self, group_nms: Sequence[str] | None = None) -> DiczGroups:
        if group_nms:
            the_groups = tuple(self.group(key) for key in group_nms)
        else:
            the_groups = tuple(self.coll.values())
        return the_groups
