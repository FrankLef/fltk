from pathlib import Path
import pandas as pd
from datetime import datetime as dt

from fltk.dicz.main import Dicz


fixtures_path = Path(__file__).parents[3].joinpath("tests", "dicz")
xlpath = fixtures_path.joinpath("dicz1.xlsx")
xlsheet: str = "data1"
out_fn = f"dicz1_z1_{dt.now().date().isoformat()}.xlsx"
out_path = Path(__file__).parent.joinpath(out_fn)

dicz = Dicz(name="ztest1")

data = pd.read_excel(xlpath, sheet_name=xlsheet)
# dicz.get_data(data)
# dicz.get_bag()
dicz.build(data)
print("\ndicz:\n", dicz, "\n", sep="")

a_group = dicz.group("entities")
print("\na_group:\n", a_group, sep="")

a_line = dicz.group("entities").line("CieA")
print("\na_line:\n", a_line, sep="")

a_item = dicz.group("entities").line("CieA").item("role")
print("\na_item:\n", a_item.value, sep="")

a_group_role = dicz.group("entities").filter_role("core")
print("\na_group_role:\n", a_group_role, sep="")

a_group_role_cieA = dicz.group("entities").filter_role("core").line("CieA")
print("\na_group_role_cieA:\n", a_group_role_cieA, sep="")

# groupA = dicz.groups("entities").lines("CieA")
# print("groupA:\n", groupA)


# print(dicz.data)
