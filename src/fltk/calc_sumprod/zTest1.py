import pandas as pd
from pathlib import Path
from datetime import datetime as dt

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_sumprod.main import CalcSumprod


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
sumprod_path = fixtures_path.joinpath("sumprod.xlsx")
out_fn = f"sumprod_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "rolly"
data_sheet = "data1"
newvalue_var = "rolly_amt"

sumprod = CalcSumprod(name="testSumprodZ1", idx_to="idx")
sumprod.load_mat_from_xl(sumprod_path, sheet_nm=idx_sheet)

raw_data = pd.read_excel(
    sumprod_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

sumprod.load_data(
    raw_data,
    idx_var="period",
    value_var="amount",
    group_vars=["entity", "concept", "pertype"],
    newvalue_var=newvalue_var,
)

sumprod.fit(is_fillna=False)
sumprod.transform(is_merged=True)

print("\n", sumprod, sep="")

sumprod.to_excel(out_path)
