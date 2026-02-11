import pandas as pd
from pathlib import Path
from fltk.diffmat.diffmat import DiffMat

xl_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures/diff_mat.xlsx")

diffmat = DiffMat(idx_to="idx")
diffmat.load_mat_from_xl(xl_path, sheet_nm="qrtr")
# print("\nidx_df:")
# diffmat.idx_df.info()

raw_data = pd.read_excel(xl_path, sheet_name="data")
# data.info()

group_vars = ["entity", "concept", "pertype"]
diffmat.load_data(raw_data, idx_var="period", value_var="amount", group_vars=group_vars)


diffmat.fit()
# print("\ntest find_invalid_items:", diffmat._invalid_items, "\n")
