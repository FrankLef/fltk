import pandas as pd

from .bag import DiczBag
from .group import DiczGroup
from .line import DiczLine
from .item import DiczItem
from . import get_dicts

type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


def main(key: str, data: pd.DataFrame) -> DiczBag:
    dicts: GroupDict = get_dicts.main(data)
    bag: DiczBag = build_bag(key=key, dicts=dicts)
    nlines = sum([len(x) for x in dicts.values()])
    if bag.nlines != nlines:
        msg: str = f"Bag '{key}' has {bag.nlines} lines. It must have {nlines} lines."
        raise AssertionError(msg)
    return bag


def build_bag(key: str, dicts: GroupDict) -> DiczBag:
    dicz_bag = DiczBag(key=key)
    for group_nm, group_val in dicts.items():
        dicz_group = DiczGroup(key=group_nm)
        for line_nm, line_val in group_val.items():
            dicz_line = DiczLine(key=line_nm)
            for item_nm, item_val in line_val.items():
                dicz_item = DiczItem(key=item_nm, value=item_val)
                dicz_line.append(dicz_item)
            dicz_group.append(dicz_line)
        dicz_bag.append(dicz_group)
    return dicz_bag
