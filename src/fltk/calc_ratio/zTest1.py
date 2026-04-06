import pandas as pd
from pathlib import Path

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_comb.calc_ratio import CalcRatio


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
ratio_path = fixtures_path.joinpath("ratio.xlsx")
out_path = fixtures_path.joinpath("ratio_z1.xlsx")
ratio_sheet: str = "concepts_ratios"
data_sheet: str= "data1"

ratio = CalcRatio(name="testRatioZ1")
ratio.ratio_df.info()

# print(ratio_path)
# raw_data = pd.read_excel(
#     comb_path,
#     sheet_name=data_sheet,
#     engine="openpyxl",
#     engine_kwargs={"data_only": True},
# )
# raw_data.info()

# group_vars = ["entity", "concept", "pertype"]
# comb.load_data(
#     raw_data,
#     idx_var="period",
#     value_var="amount",
#     group_vars=group_vars,
#     newvalue_var=newvalue_var,
# )
# print("load_data")
# # breakpoint()

# comb.fit()
# comb.transform()