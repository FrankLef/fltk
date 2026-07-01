from pathlib import Path
from typing import Any
from enum import StrEnum, auto
from great_tables import GT
import plotly.graph_objects as go
from rich.console import Console

from fltk.rich.print_msg import custom_theme, print_msg, MsgType

console = Console(theme=custom_theme)


class PrintObj:
    class PType(StrEnum):
        NONE = auto()
        SHOW = auto()
        FILE = auto()

    def __init__(self, path: Path):
        self.path = path

    def run(self, objs: dict[str, Any], ptype: PType | str) -> None:
        if not objs:
            raise ValueError("The dictionnary of objects is empty.")

        ptype = ptype.lower()
        if ptype not in self.PType:
            raise TypeError(f"'{ptype}' is an invalid PType value.")

        if ptype == self.PType.FILE:
            self.start_msg()

        for name, obj in objs.items():
            self.execute(obj, name=name, ptype=ptype)

    def start_msg(self) -> None:
        console.print("[process]Exporting file to:[/process]")
        console.print(f"[info]{self.path}[/info]")

    def execute(self, obj: Any, name: str, ptype: PType | str):
        if ptype != self.PType.NONE:
            if ptype == self.PType.SHOW:
                obj.show()
            elif ptype == self.PType.FILE:
                fn = name + ".html"
                path_fn = self.path.joinpath(fn)
                if isinstance(obj, go.Figure):
                    obj.write_html(path_fn)
                elif isinstance(obj, GT):
                    obj.write_raw_html(path_fn)
                else:
                    msg = f"Cannot handle object of type '{type(obj)}'"
                    raise TypeError(msg)
                print_msg(fn, type=MsgType.TRACE)
            else:
                raise ValueError(f"'{ptype}' is an invalid ptype.")
