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

# print(diffmat._data_keys)
# print("\nraw_data:")
# diffmat.data.info()
diffmat.fit()
print("\ntest find_invalid:", diffmat._invalid, "\n")


groups_df = diffmat.data[group_vars]
groups_df.drop_duplicates(inplace=True)
# print("\ngroups_df:")
# print(groups_df.head())


def get_invalid_rows(idx_df, data):
    left_df = idx_df
    right_df = data
    left_on = "idx_from"
    right_on = "period"
    merged_df = pd.merge(
        left_df,
        right_df,
        left_on=left_on,
        right_on=right_on,
        how="left",
        indicator=True,
    )
    return merged_df


out = []
i = 0
for ndx, row in groups_df.iterrows():
    row_dict = row.to_dict()
    left_df = pd.DataFrame([row_dict])
    matching_df = pd.merge(left=left_df, right=raw_data, on=group_vars, how="inner")
    # print(f"\nmatching_df {i}")
    # matching_df.info()
    merged_df = get_invalid_rows(idx_df=diffmat.idx_df, data=matching_df)
    # print(f"\nmerged_df {i}")
    # merged_df.info()
    invalid_df = merged_df.loc[merged_df._merge != "both"]
    # print(f"\ninvalid_df {i}")
    # invalid_df.info()
    invalid_df = invalid_df[["idx_from", "idx"]]
    print(invalid_df.head())
    i += 1
    out.append([row_dict, invalid_df])

# diffmat.fit()
# print("\nidx_validation:")
# diffmat.idx_validation.info()
# df = diffmat.idx_validation
# print(df)
# diffmat.idx_validation.head()
# invalid_df = diffmat.idx_validation.loc[diffmat.idx_validation._merge != "both"]
# invalid_df.info()
# print(invalid_df.head())
