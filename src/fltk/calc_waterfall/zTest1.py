import pandas as pd
from pathlib import Path
from datetime import datetime as dt

from fltk.calc_waterfall.main import CalcWaterfall


fixtures_path = Path(__file__).parents[3].joinpath("tests", "fixtures")
data_path = fixtures_path.joinpath("waterfall.xlsx")
data_sheet: str = "data1"
out_fn = f"wfall_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)

wfall = CalcWaterfall(name="testWaterfallZ1", initial="absolue")

raw_data = pd.read_excel(
    data_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

wfall.load_raw_data(
    raw_data,
    groups=("entity", "pertype"),
    period_from="period_from",
    period_to="period_to",
    ratio_nm="concept_ratio",
    num_from_val="num_from",
    num_to_val="num_to",
    volume_diff="vol_diff",
    price_diff="price_diff",
    mix_diff="mix_diff",
    total_diff="tot_diff",
)

wfall.fit(verbose=True)
wfall.transform(verbose=True)

print("\n", wfall, sep="")


wfall.to_excel(out_path)
