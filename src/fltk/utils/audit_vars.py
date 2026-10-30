import polars as pl


def audit_missing(data: pl.DataFrame, vars: str | tuple[str, ...]) -> bool:
    """Validate if some variables are not found in the columns."""
    cols = data.columns
    missing_vars = [var for var in vars if var not in cols]
    if missing_vars:
        msg: str = f"{missing_vars} are not found in the column names."
        raise ValueError(msg)
    return True


def audit_illegal(data: pl.DataFrame, vars: str | tuple[str, ...]) -> bool:
    """Validate if some columns have illegal names."""
    cols = data.columns
    illegal_vars = [var for var in vars if var in cols]
    if illegal_vars:
        msg = f"""
        {illegal_vars} are reserved names.
        Please change these column names.
        """
        raise ValueError(msg)
    return True
