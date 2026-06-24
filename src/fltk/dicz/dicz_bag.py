from .dicz_group import DiczGroup


class DiczBag:
    def __init__(self) -> None:
        self.coll: dict[str, DiczGroup] = {}

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "ngroups": str(self.ngroups),
        }
        msg: str = "\n".join([key + ": " + val for key, val in info.items()])
        return msg

    @property
    def ngroups(self) -> int:
        return len(self.coll)

    @property
    def nlines(self) -> int:
        nlines = sum([x.nlines for x in self.coll.values()])
        return nlines

    @property
    def nitems(self) -> int:
        nitems = sum([x.nitems for x in self.coll.values()])
        return nitems

    def append(self, item: DiczGroup):
        self.coll[item.key] = item

    def group(self, key) -> DiczGroup:
        try:
            a_group = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid group key.")
        return a_group
