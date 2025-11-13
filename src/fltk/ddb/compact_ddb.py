"""Compacting duckdb database by copying."""
# source:
# https://duckdb.org/docs/operations_manual/footprint_of_duckdb/reclaiming_space

import duckdb as ddb
from pathlib import Path
from rich import print as rprint


def copy_db(duckdb_path: Path, temp_path: Path):
    try:
        temp_path.unlink()
    except FileNotFoundError:
        pass
    qry = f"""
    ATTACH '{duckdb_path}' AS db1;
    ATTACH '{temp_path}' AS db2;
    COPY FROM DATABASE db1 to db2;
    """
    ddb.execute(qry)
    qry = """
    DETACH db1;
    DETACH db2;
    """
    ddb.execute(qry)


def ren_db(duckdb_path: Path, temp_path: Path):
    new_path = temp_path.with_name(duckdb_path.name)
    duckdb_path.unlink()
    temp_path.replace(new_path)


def test_db(duckdb_path: Path):
    with ddb.connect(duckdb_path) as conn:
        data = conn.sql("DESCRIBE TABLES").fetchall()
        rprint(f"{len(data)} tables in '{duckdb_path.name}'.")


def main(duckdb_path: Path, temp_file: str = "temp.duckdb") -> None:
    rprint(f"Compacting '{duckdb_path.name}'.")
    size_before = duckdb_path.stat().st_size / 1024**2
    temp_path = duckdb_path.with_name(temp_file)
    copy_db(duckdb_path=duckdb_path, temp_path=temp_path)
    ren_db(duckdb_path=duckdb_path, temp_path=temp_path)
    size_after = duckdb_path.stat().st_size / 1024**2
    msg : str = f"File size: before = {size_before:0.2f} MB, after = {size_after:0.2f} MB."
    rprint(msg)
    test_db(duckdb_path=duckdb_path)
