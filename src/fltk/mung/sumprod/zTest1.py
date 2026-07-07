import polars as pl
from pathlib import Path
from datetime import datetime as dt

from fltk.mung.sumprod.main import MungSumprod


fixtures_path = Path(__file__).parents[4].joinpath("tests", "mung", "fixtures")
sumprod_path = fixtures_path.joinpath("sumprod.xlsx")
out_fn = f"sumprod_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "qrtr"
data_sheet = "data1"
newvalue_var = "qrtr_amt"

sumprod = MungSumprod(name="testSumprodZ1", idx_to="idx")
sumprod.load_mat_from_xl(sumprod_path, sheet_nm=idx_sheet)

raw_data = pl.read_excel(sumprod_path, sheet_name=data_sheet)

sumprod.load_raw_data(
    raw_data,
    idx="period",
    value="amount",
    groups=("entity", "concept", "pertype"),
    newvalue=newvalue_var,
)

sumprod.fit()
sumprod.transform()

print("\n", sumprod, sep="")

# sumprod.to_excel(out_path)
