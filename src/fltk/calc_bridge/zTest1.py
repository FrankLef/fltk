import pandas as pd
from pathlib import Path
from datetime import datetime as dt

from fltk.calc_bridge.main import CalcBridge


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
data_path = fixtures_path.joinpath("bridge.xlsx")
data_sheet: str = "data1"
out_fn = f"bridge_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)


ratios = (
    "Ebitda2TangibleAssetsNoncash",
    "Ebitda2Sales",
    "Sales2TangibleAssetsNoncash",
    "Sales2DirectLabor",
    "Sales2MaterialCosts",
    "MaterialCosts2DirectLabor",
)
bridge = CalcBridge(name="testBridgeZ1", ratios=ratios)

cols = (
    "entity",
    "pertype",
    "period",
    "concept_ratio",
    "concept_num",
    "concept_den",
    "ratio",
    "num",
    "den",
)
raw_data = pd.read_excel(
    data_path,
    sheet_name=data_sheet,
    usecols=cols,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

bridge.load_raw_data(
    raw_data,
    groups=("entity", "pertype"),
    period="period",
    ratio_nm="concept_ratio",
    ratio_val="ratio",
    num_nm="concept_num",
    num_val="num",
    den_nm="concept_den",
    den_val="den",
)

bridge.fit(verbose=True)
bridge.transform(verbose=True)

print("\n", bridge, sep="")

# print("\n", bridge.bridge.head(), sep="")

# bridge.to_excel(out_path)
