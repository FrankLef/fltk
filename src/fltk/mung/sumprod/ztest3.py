import polars as pl
from pathlib import Path
from datetime import datetime as dt

from fltk.mung.sumprod.main import MungSumprod

fixtures_path = Path(__file__).parents[4].joinpath("tests", "mung", "fixtures")
sumprod_path = fixtures_path.joinpath("sumprod.xlsx")
out_fn = f"sumprod_z3_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "concepts_adds"
data_sheet = "data2"
newvalue_var = "adds_amt"

sumprod = MungSumprod(
    name="testSumprodZ2",
    idx_to="concept_add",
    idx_from="concept_addend",
    sump_coef="coef",
    sump_value="summ_amt",
)
sump_df = pl.read_excel(sumprod_path, sheet_name="concepts_adds")
sumprod.load_sump(sump_df)

raw_data = pl.read_excel(sumprod_path, sheet_name=data_sheet)

sumprod.load_raw_data(
    raw_data,
    idx="concept",
    value="amount",
    groups=("entity", "period", "pertype"),
    newvalue=newvalue_var,
)

sumprod.fit()
sumprod.transform(missing_to_zero=True)

print("\n", sumprod, sep="")

# sumprod.to_excel(out_path)
