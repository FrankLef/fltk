import pandas as pd
from pathlib import Path
from datetime import datetime as dt

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_ratio.main import CalcRatio


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
ratio_path = fixtures_path.joinpath("ratio.xlsx")
out_fn = f"ratio_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
ratio_sheet: str = "concepts_ratios"
data_sheet: str = "data1"

ratio = CalcRatio(name="testRatioZ1")


ratios_df = pd.read_excel(
    ratio_path,
    sheet_name=ratio_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)

ratio.load_ratios(ratios_df)


raw_data = pd.read_excel(
    ratio_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)
group_vars = ["entity", "pertype", "period"]
ratio.load_data(
    raw_data,
    concept_var="concept",
    value_var="amount",
    group_vars=group_vars,
)

ratio.fit()
ratio.transform(is_cleaned=True)

print("\n", ratio, sep="")

ratio.to_excel(out_path)
