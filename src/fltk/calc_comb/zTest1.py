import pandas as pd
from pathlib import Path
from datetime import datetime as dt

# from rich.prompt import Confirm
# from rich.console import Console
from fltk.calc_comb.calc_comb import CalcComb


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
comb_path = fixtures_path.joinpath("comb.xlsx")
out_fn = f"comb_z1_{dt.now().date().isoformat()}.xlsx"
out_path = fixtures_path.joinpath(out_fn)
idx_sheet: str = "rolly"
data_sheet = "data1"
newvalue_var = "rolly_amt"

comb = CalcComb(name="testCombZ1", idx_to="idx")
comb.load_mat_from_xl(comb_path, sheet_nm=idx_sheet)
comb.combs_df.info()

print(comb_path)
raw_data = pd.read_excel(
    comb_path,
    sheet_name=data_sheet,
    engine="openpyxl",
    engine_kwargs={"data_only": True},
)
raw_data.info()

group_vars = ["entity", "concept", "pertype"]
comb.load_data(
    raw_data,
    idx_var="period",
    value_var="amount",
    group_vars=group_vars,
    newvalue_var=newvalue_var,
)
print("load_data")
# breakpoint()

comb.fit()
comb.transform(is_merged=True)

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
    comb.data.to_excel(out_path, sheet_name="data", index=False, engine="openpyxl")
    # Append other sheets
    with pd.ExcelWriter(
        out_path, mode="a", engine="openpyxl", if_sheet_exists="replace"
    ) as writer:
        dfs = {
            "invalid_data": comb.invalid_data,
            # "undetermined_data": comb.undetermined_data,
            "valid_data": comb.valid_data,
        }
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
