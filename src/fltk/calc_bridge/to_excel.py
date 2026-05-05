from pathlib import Path
import pandas as pd
from rich.console import Console
from rich import print as rprint
    
    
def to_excel(name: str, path: Path, dfs: dict[str, pd.DataFrame]) -> None:
    """Export data to excel.

    Args:
        name (str): Name of the object.
        path (Path): Path to xl file.
        dfs (dict[str, pd.DataFrame]): Dictionary of dataframes.
    """
    start_msg(name, path=path)
    
    items_iter = iter(dfs.items())
    
    sheet_nm, df = next(items_iter)
    rprint(f"'{sheet_nm}'")
    df.to_excel(path, sheet_name=sheet_nm, index=False, engine="openpyxl")
    
    with pd.ExcelWriter(
        path, mode="a", engine="openpyxl", if_sheet_exists="replace"
    ) as writer:
        while True:
            try:
                sheet_nm, df = next(items_iter)
                rprint(f"'{sheet_nm}'")
                df.to_excel(writer, sheet_name=sheet_nm, index=False)
            except StopIteration:
                break
                

def start_msg(name: str, path: Path)-> str:
    console = Console()
    msg: str = f"\n[bright_white]Exporting '{name}' to:[/bright_white]\n[cyan]{path}[/cyan]"
    console.print(msg)
    return msg
    

