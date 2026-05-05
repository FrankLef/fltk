import pandas as pd
from pathlib import Path
from datetime import datetime as dt

from fltk.calc_sumprod.main import CalcSumprod

fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
sumprod_path = fixtures_path.joinpath("sumprod.xlsx")
out_fn = f"sumprod_z2_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "concepts_adds"
data_sheet = "data2"
newvalue_var = "adds_amt"

sumprod = CalcSumprod(
    name="testSumprodZ2",
    idx_to="concept_add",
    idx_from="concept_from",
    sump_coef="coef",
    sump_value="summ_amt",
)
sump_df = pd.read_excel(sumprod_path, sheet_name="concepts_adds")
sumprod.load_sump(sump_df)
# sumprod.sump_df.info()

raw_data = pd.read_excel(
    sumprod_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)
# raw_data.info()

sumprod.load_raw_data(
    raw_data,
    idx="concept",
    value="amount",
    groups=("entity", "period", "pertype"),
    newvalue=newvalue_var,
)

sumprod.fit(is_fillna=True)
sumprod.transform(is_merged=False)

print("\n", sumprod, sep="")

sumprod.to_excel(out_path)
