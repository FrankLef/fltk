from .dicz_line import DiczLine


class DiczGroup:
    def __init__(self, key: str):
        self.key = key
        self.coll: dict[str, DiczLine] = {}

    def __repr__(self) -> str:
        info: dict[str, str] = {
            "key": self.key,
            "nlines": str(self.nlines),
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

    def append(self, item: DiczLine):
        self.coll[item.key] = item

    def line(self, key) -> DiczLine:
        try:
            a_line = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid line key.")
        return a_line
