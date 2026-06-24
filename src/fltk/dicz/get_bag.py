from .dicz_bag import DiczBag
from .dicz_group import DiczGroup
from .dicz_line import DiczLine
from .dicz_item import DiczItem

type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


def main(data: GroupDict) -> DiczBag:
    dicz_bag = DiczBag()
    for group_nm, group_val in data.items():
        dicz_group = DiczGroup(key=group_nm)
        for line_nm, line_val in group_val.items():
            dicz_line = DiczLine(key=line_nm)
            for item_nm, item_val in line_val.items():
                dicz_item = DiczItem(key=item_nm, value=item_val)
                dicz_line.append(dicz_item)
            dicz_group.append(dicz_line)
        dicz_bag.append(dicz_group)
    return dicz_bag
