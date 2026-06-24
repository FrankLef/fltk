import pandas as pd

from .dicz_enum import DiczVar as vars

type ItemDict = dict[str, str]
type LineDict = dict[str, ItemDict]
type GroupDict = dict[str, LineDict]


def main(data: pd.DataFrame) -> GroupDict:
    if data.empty:
        raise ValueError("The data is empty.")
    audit_columns(data)
    out = get_dictionnaries(data)
    return out


def audit_columns(data: pd.DataFrame) -> None:
    cols = data.columns

    check = sum(cols.duplicated())
    if check:
        msg: str = f"Data has {check} duplicates in its columns."
        raise KeyError(msg)

    reserved_nms = [x.value for x in vars]
    missing_nms = [x for x in reserved_nms if x not in cols]
    if missing_nms:
        msg = f"{len(missing_nms)} required columns missing\n{missing_nms}"
        raise KeyError(msg)


def get_dictionnaries(data) -> GroupDict:
    groups = get_groups(data, col=vars.GROUP)
    out = {nm: get_lines(df, col=vars.LINE) for nm, df in groups.items()}
    return out


def get_groups(data: pd.DataFrame, col: str) -> dict[str, pd.DataFrame]:
    nms = data[col].unique()
    out = {nm: get_df(data, col=col, value=nm) for nm in nms}
    return out


def get_lines(data: pd.DataFrame, col: str) -> LineDict:
    nms = data[col].unique()
    out = {
        nm: get_df(data, col=col, value=nm).to_dict(orient="records")[0] for nm in nms
    }
    return out


def get_df(data: pd.DataFrame, col: str, value: str) -> pd.DataFrame:
    df = data[data[col] == value]
    df.drop(columns=col, inplace=True)
    return df
