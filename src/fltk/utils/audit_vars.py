import pandas as pd


def audit_cols(data: pd.DataFrame, vars: str | tuple[str, ...]) -> None:
    """Validate if some columns don't exist."""
    cols = data.columns.to_list()
    illegal_vars = [var for var in vars if var not in cols]
    if illegal_vars:
        msg: str = f"{illegal_vars} are not found in the column names."
        raise ValueError(msg)


def audit_illegal(data: pd.DataFrame, vars: str | tuple[str, ...]) -> None:
    """Validate if some columns have illegal names."""
    cols = data.columns.to_list()
    illegal_vars = [var for var in vars if var in cols]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)


def audit_keys(data: pd.DataFrame, keys: str | tuple[str, ...]) -> None:
    """Validate the keys."""
    if isinstance(keys, str):
        cols: str | list[str] = keys
    else:
        cols = list(keys)
    unique_counts = data[cols].value_counts()
    ndistinct = len(unique_counts)
    check = data.shape[0] - ndistinct
    if check:
        msg: str = f"Data has {check} duplicates in the keys."
        raise KeyError(msg)
