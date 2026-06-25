from pathlib import Path
import pandas as pd
from datetime import datetime as dt

from fltk.dicz.main import Dicz


fixtures_path = Path(__file__).parents[3].joinpath("tests", "dicz")
xlpath = fixtures_path.joinpath("bag1.xlsx")
xlsheet: str = "data1"
out_fn = f"dicz1_z1_{dt.now().date().isoformat()}.xlsx"
out_path = Path(__file__).parent.joinpath(out_fn)

dicz = Dicz(name="ztest1")

data = pd.read_excel(xlpath, sheet_name=xlsheet)
dicz.append(key="bag1", data=data)
print("\ndicz:\n", dicz, "\n", sep="")

a_bag = dicz.bag("bag1")
print("\na_bag:\n", a_bag, sep="")

a_group = a_bag.group("entities")
print("\na_group:\n", a_group, sep="")

a_line = a_bag.group("entities").line("CieA")
print("\na_line:\n", a_line, sep="")

a_item = a_bag.group("entities").line("CieA").item("role")
print("\na_item:\n", a_item.value, sep="")

a_group_role = a_bag.group("entities").filter_role("core")
print("\na_group_role:\n", a_group_role, sep="")

a_line_role_cieA = a_bag.group("entities").filter_role("core").line("CieA")
print("\na_line_role_cieA:\n", a_line_role_cieA, sep="")
