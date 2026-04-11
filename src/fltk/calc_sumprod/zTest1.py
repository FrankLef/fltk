import pandas as pd
from pathlib import Path
from datetime import datetime as dt

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_sumprod.main import CalcSumprod


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
sumprod_path = fixtures_path.joinpath("sumprod.xlsx")
out_fn = f"sumprod_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "rolly"
data_sheet = "data1"
newvalue_var = "rolly_amt"

sumprod = CalcSumprod(name="testSumprodZ1", idx_to="idx")
sumprod.load_mat_from_xl(sumprod_path, sheet_nm=idx_sheet)
sumprod.sump_df.info()

print(sumprod_path)
raw_data = pd.read_excel(
    sumprod_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)
raw_data.info()

group_vars = ["entity", "concept", "pertype"]
sumprod.load_data(
    raw_data,
    idx_var="period",
    value_var="amount",
    group_vars=group_vars,
    newvalue_var=newvalue_var,
)
print("load_data")
# breakpoint()

sumprod.fit()
sumprod.transform(is_merged=True)

# print(f"\ninvalid data {comb.invalid_data.shape}:\n", comb.invalid_data)
# print(
#     f"\nundetermined data {comb.undetermined_data.shape}:\n",
#     comb.undetermined_data,
# )
# print(f"\nvalid data {comb.valid_data.shape}:\n", comb.valid_data)

# print(f"\nfinal data {comb.data.shape}:\n", comb.data)

add_to_xl: bool = True
if add_to_xl:
    # IMPORTANT INFO FOR USER:
    msg: str = """
    If you use this, make sure to recalculate the spreadheet by adding any value and pressing F9 in Excel.
    Otherwise, next time, pandas will load the cell with formula as formula, not as value.
    The best way to avoid this issue is to output the data in a different file.
    Do you want to do it anyway?
    """
    # is_ok = Confirm.ask(prompt=msg)
    # if is_ok:

    # Create the initial file
    sumprod.data.to_excel(out_path, sheet_name="data", index=False, engine="openpyxl")
    # Append other sheets
    with pd.ExcelWriter(
        out_path, mode="a", engine="openpyxl", if_sheet_exists="replace"
    ) as writer:
        dfs = {
            "invalid_data": sumprod.invalid_data,
            "valid_data": sumprod.valid_data,
            "calc_data": sumprod.calc_data,
            "output": sumprod.output,
        }
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
