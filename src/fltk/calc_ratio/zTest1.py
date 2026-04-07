import pandas as pd
from pathlib import Path

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_ratio.calc_ratio import CalcRatio


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
ratio_path = fixtures_path.joinpath("ratio.xlsx")
out_path = fixtures_path.joinpath("ratio_z1.xlsx")
ratio_sheet: str = "concepts_ratios"
data_sheet: str = "data1"

ratio = CalcRatio(name="testRatioZ1")

ratio.load_ratios(ratio_path, sheet_nm=ratio_sheet)
print("\nratios_df:", ratio.ratios_df.shape)
# ratio.ratios_df.info()
print("\nratios_df_long:", ratio.ratios_df_long.shape)
# ratio.ratios_df_long.info()


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
print("\ndata:", ratio.data.shape)
# ratio.data.info()

ratio.fit()
print("\nmerged_data:", ratio.merged_data.shape)

print(ratio.merged_data.head(20))
