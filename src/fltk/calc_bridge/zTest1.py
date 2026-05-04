import pandas as pd
from pathlib import Path
from datetime import datetime as dt

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_bridge.main import CalcBridge


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
ratio_path = fixtures_path.joinpath("ratio.xlsx")
out_fn = f"bridge_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
ratio_sheet: str = "concepts_ratios"
data_sheet: str = "data1"

bridge = CalcBridge(name="testBridgeZ1")


ratios_df = pd.read_excel(
    ratio_path,
    sheet_name=ratio_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

bridge.load_ratios(
    data=ratios_df, ratio_nm="concept_ratio", num_nm="concept_num", den_nm="concept_den"
)


raw_data = pd.read_excel(
    ratio_path,
    sheet_name=data_sheet,
    names=("entity", "pertype", "period", "concept_ratio", "ratio"),
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

bridge.load_raw_data(
    raw_data,
    groups=("entity", "pertype"),
    period="period",
    ratio="concept_ratio",
    value="ratio",
)
# print("\ndata:", ratio.data.shape)
# ratio.data.info()

bridge.fit()
bridge.transform()
# print("\nmerged_data:", ratio.merged_data.shape)
# print(ratio.merged_data.head(20))

print(bridge)

# bridge.to_excel(out_path)
