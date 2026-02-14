import pandas as pd
from pathlib import Path
from fltk.diffmat.diffmat import DiffMat


xl_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures/diff_mat.xlsx")

diffmat = DiffMat(idx_to="idx")
diffmat.load_mat_from_xl(xl_path, sheet_nm="rolly")
# print("\nidx_df:")

# diffmat.idx_df.info()

raw_data = pd.read_excel(xl_path, sheet_name="data1")
# data.info()

group_vars = ["entity", "concept", "pertype"]
diffmat.load_data(
    raw_data,
    idx_var="period",
    value_var="amount",
    group_vars=group_vars,
    newvalue_var="rolly_amt",
)


diffmat.fit()
diffmat.transform()

print(f"\ninvalid data {diffmat.invalid_data.shape}:\n", diffmat.invalid_data)
print(
    f"\nundetermined data {diffmat.undetermined_data.shape}:\n",
    diffmat.undetermined_data,
)
