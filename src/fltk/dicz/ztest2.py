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

print("\nkeys:\n", a_group.keys)

print("\nnames_tupl:\n", a_group.names_tupl)