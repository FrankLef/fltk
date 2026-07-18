from pathlib import Path
import polars as pl
from datetime import datetime as dt

from fltk.dicz.main import Dicz


fixtures_path = Path(__file__).parents[3].joinpath("tests", "dicz", "fixtures")
xlpath = fixtures_path.joinpath("bag_xbr.xlsx")
xlsheet: str = "data"
out_fn = f"dicz1_z1_{dt.now().date().isoformat()}.xlsx"
out_path = Path(__file__).parent.joinpath(out_fn)

dicz = Dicz(name="ztest1")

data = pl.read_excel(xlpath, sheet_name=xlsheet)
dicz.append(bag_nm="xbr", data=data)
print("\ndicz:\n", dicz, "\n", sep="")

a_bag = dicz.bag("xbr")
print("\na_bag:\n", a_bag, sep="")

a_group = a_bag.group("xbr_fstypes")
print("\na_group:\n", a_group, sep="")

print("\nline_nms:\n", a_group.line_nms)

print("\nnames_tupl:\n", a_group.names_tupl)
