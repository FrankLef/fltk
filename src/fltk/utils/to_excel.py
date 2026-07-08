from pathlib import Path
import polars as pl
import xlsxwriter as xlsxw
from rich.console import Console


def to_excel(name: str, path: Path, dfs: dict[str, pl.DataFrame]) -> None:
    """Export data to excel.

    Args:
        name (str): Name of the object.
        path (Path): Path to xl file.
        dfs (dict[str, pl.DataFrame]): Dictionary of dataframes.
    """
    start_msg(name, path=path)

    # NOTE: nan_inf_to_errors allows to send NaN and in to excel. Otherwise an exception will be triggered.
    with xlsxw.Workbook(path, {"nan_inf_to_errors": True}) as workbook:
        for sheet_nm, df in dfs.items():
            df.write_excel(workbook=workbook, worksheet=sheet_nm)
            Console().print(f"[green]{sheet_nm}[/green]")


def start_msg(name: str, path: Path) -> str:
    console = Console()
    msg: str = (
        f"\n[dark_orange]Exporting {name} to excel:[/dark_orange]\n[cyan]{path}[/cyan]"
    )
    console.print(msg)
    return msg
