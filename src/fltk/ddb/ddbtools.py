import duckdb as ddb
from os import getlogin
from config import settings
from rich import print as rprint

duckdb_path = settings.paths.duckdb


def show_ddb(tbl: str = "%", is_stop: bool = True) -> None:
    qry = f"SELECT * FROM (SHOW TABLES) WHERE name like '{tbl}'"
    with ddb.connect(duckdb_path) as conn:
        tbl_nms = conn.sql(qry).fetchall()
        for tbl_nm in tbl_nms:
            nm = tbl_nm[0]
            nrows = conn.sql(f"SELECT count(*) as nb FROM {nm}").fetchone()[0]  # type: ignore
            rprint(f"{nm} with {nrows} rows.")
            conn.sql(f"DESCRIBE {nm}").show()
    if is_stop:
        rprint(f"Process stopped by user '{getlogin()}'.")
        raise KeyboardInterrupt()
