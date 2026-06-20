import pandas as pd
from pathlib import Path
from datetime import datetime as dt

from fltk.mung.waterfall.main import MungWaterfall


fixtures_path = Path(__file__).parents[4].joinpath("tests", "mung", "fixtures")
data_path = fixtures_path.joinpath("waterfall.xlsx")
data_sheet: str = "data1"
out_fn = f"wfall_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)

wfall = MungWaterfall(name="testWaterfallZ1", initial="absolute")

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


# wfall.to_excel(out_path)
