from .dicz_line import DiczLine
from .dicz_enum import DiczVar as vars


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

    def append(self, item: DiczLine):
        self.coll[item.key] = item

    def line(self, key) -> DiczLine:
        try:
            a_line = self.coll[key]
        except KeyError:
            raise KeyError(f"'{key}' is an invalid line key.")
        return a_line

    def filter_role(self, role: str)-> DiczGroup:
        a_group = self.filter_lines(item_nm=vars.ROLE, pattern=role)
        return a_group
    
    def filter_rule(self, rule: str)-> DiczGroup:
        a_group = self.filter_lines(item_nm=vars.RULE, pattern=rule)
        return a_group
    
    def filter_lines(self, item_nm: str, pattern: str)->DiczGroup:
        dicz_group = DiczGroup(key=self.key)
        for line_val in self.coll.values():
            a_item = line_val.coll[item_nm]
            if a_item.is_matched(pattern=pattern):
                dicz_group.append(line_val)
        return dicz_group
