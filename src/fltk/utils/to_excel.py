from pathlib import Path
import polars as pl
import xlsxwriter
from rich.console import Console


def to_excel(name: str, path: Path, dfs: dict[str, pl.DataFrame]) -> None:
    """Export data to excel.

    Args:
        name (str): Name of the object.
        path (Path): Path to xl file.
        dfs (dict[str, pl.DataFrame]): Dictionary of dataframes.
    """
    start_msg(name, path=path)

    # items_iter = iter(dfs.items())

    # sheet_nm, df = next(items_iter)
    # Console().print(f"[green]{sheet_nm}[/green]")
    # df.write_excel(path, worksheet=sheet_nm)

    # with pd.ExcelWriter(
    #     path, mode="a", engine="openpyxl", if_sheet_exists="replace"
    # ) as writer:
    #     while True:
    #         try:
    #             sheet_nm, df = next(items_iter)
    #             Console().print(f"[green]{sheet_nm}[/green]")
    #             df.to_excel(writer, sheet_name=sheet_nm, index=False)
    #         except StopIteration:
    #             break

    with xlsxwriter.Workbook(path) as workbook:
        for sheet_nm, df in dfs.items():
            # Polars handles writing directly to the xlsxwriter workbook object
            df.write_excel(workbook=workbook, worksheet=sheet_nm)
            Console().print(f"[green]{sheet_nm}[/green]")


def start_msg(name: str, path: Path) -> str:
    console = Console()
    msg: str = (
        f"\n[dark_orange]Exporting {name} to excel:[/dark_orange]\n[cyan]{path}[/cyan]"
    )
    console.print(msg)
    return msg
