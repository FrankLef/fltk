import pandas as pd
from pathlib import Path
from fltk.diffmat.diffmat import DiffMat


fixtures_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures")
diffmat_path = fixtures_path.joinpath("diffmat.xlsx")
idx_sheet: str = "rolly"
data_sheet = "data1"
newvalue_var = "rolly_amt"

diffmat = DiffMat(idx_to="idx")
diffmat.load_mat_from_xl(diffmat_path, sheet_nm=idx_sheet)
# print("\nidx_df:")

# diffmat.idx_df.info()
print(diffmat_path)
raw_data = pd.read_excel(diffmat_path, sheet_name=data_sheet)
raw_data.info()

group_vars = ["entity", "concept", "pertype"]
diffmat.load_data(
    raw_data,
    idx_var="period",
    value_var="amount",
    group_vars=group_vars,
    newvalue_var=newvalue_var,
)
print("load_data")
# breakpoint()

diffmat.fit()
diffmat.transform()

print(f"\ninvalid data {diffmat.invalid_data.shape}:\n", diffmat.invalid_data)
print(
    f"\nundetermined data {diffmat.undetermined_data.shape}:\n",
    diffmat.undetermined_data,
)
print(f"\nvalid data {diffmat.valid_data.shape}:\n", diffmat.valid_data)

print(f"\nfinal data {diffmat.data.shape}:\n", diffmat.data)

add_to_xl: bool = False
if add_to_xl:
    with pd.ExcelWriter(
        diffmat_path, mode="a", engine="openpyxl", if_sheet_exists="replace"
    ) as writer:
        diffmat.data.to_excel(writer, sheet_name="final_data", index=False)
        diffmat.invalid_data.to_excel(writer, sheet_name="invalid_data", index=False)
        diffmat.undetermined_data.to_excel(
            writer, sheet_name="undetermined_data", index=False
        )
        diffmat.valid_data.to_excel(writer, sheet_name="valid_data", index=False)
