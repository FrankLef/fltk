from pathlib import Path

from .clean_str import clean_sql


def get_sql(file_nm: str, path: Path | str) -> str:
    path = Path(path) if isinstance(path, str) else path
    fn = path.joinpath(file_nm)
    with open(fn, "r") as file:
        text = file.read()
    qry = clean_sql(text)
    return qry
