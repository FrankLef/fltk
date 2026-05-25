import pandas as pd
from pathlib import Path
from datetime import datetime as dt

from fltk.calc_ewm.main import CalcEwm


fixtures_path = Path(__file__).parents[3].joinpath("tests", "fixtures")
data_path = fixtures_path.joinpath("ewm.xlsx")
data_sheet: str = "data1"
out_fn = f"ewm_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)

ewm = CalcEwm(name="testEwmZ1")

raw_data = pd.read_excel(
    data_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

ewm.load_raw_data(
    raw_data,
    groups=("entity", "concept"),
    period="period",
    values=("cum", "qrtr"),
)

ewm.fit(verbose=True)
ewm.transform(verbose=True)

print("\n", ewm, sep="")


ewm.to_excel(out_path)
