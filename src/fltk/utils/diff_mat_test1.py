import pandas as pd
from pathlib import Path
from fltk.utils.diff_mat import DiffMat

xl_path = Path("C:/Users/Public/MyPy/Packages/fltk/tests/fixtures/diff_mat.xlsx")

diffmat = DiffMat(idx_to="idx")
diffmat.load_mat_from_xl(xl_path,sheet_nm="qrtr")
print(diffmat.idx_df)

data=pd.read_excel(xl_path, sheet_name="data")
# data.info()

diffmat.load_data(data,idx_var="period", value_var="amount", key_vars=["entity", "concept", "pertype"])

print(diffmat._data_keys)
