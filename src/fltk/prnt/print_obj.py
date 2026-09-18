import warnings

# This is a known bug in plotly 6.3.1, maybe will not be necessary in a future version
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*engine.*")  # noqa

from pathlib import Path  # noqa
from typing import Any  # noqa
from enum import StrEnum, auto  # noqa
from great_tables import GT  # noqa
import plotly.graph_objects as go  # noqa
from rich.console import Console  # noqa

from fltk.prnt.print_msg import custom_theme, print_msg, MsgType  # noqa

console = Console(theme=custom_theme)


class PrintObj:
    class PType(StrEnum):
        NONE = auto()
        SHOW = auto()
        HTML = auto()
        PDF = auto()
        SVG = auto()

    def __init__(self, path: Path, width: float = 450 * 16 / 9, height: float = 450):
        self.path = path
        self.width = width
        self.height = height

    def run(self, objs: dict[str, Any], ptype: PType | str) -> None:
        if not objs:
            raise ValueError("The dictionnary of objects is empty.")

        ptype = ptype.lower()
        if ptype not in self.PType:
            raise TypeError(f"'{ptype}' is an invalid PType value.")

        if ptype in (self.PType.HTML, self.PType.PDF, self.PType.SVG):
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
            elif ptype == self.PType.HTML:
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
            elif ptype == self.PType.PDF:
                fn = name + ".pdf"
                path_fn = self.path.joinpath(fn)
                if isinstance(obj, go.Figure):
                    obj.write_image(path_fn, width=self.width, height=self.height)
                elif isinstance(obj, GT):
                    obj.save(path_fn)
                else:
                    msg = f"Cannot handle object of type '{type(obj)}'"
                    raise TypeError(msg)
                print_msg(fn, type=MsgType.TRACE)
            elif ptype == self.PType.SVG:
                fn = name + ".svg"
                path_fn = self.path.joinpath(fn)
                if isinstance(obj, go.Figure):
                    obj.write_image(path_fn, width=self.width, height=self.height)
                elif isinstance(obj, GT):
                    msg = "Great Tables cannot export to SVG. Use pdf."
                    raise TypeError(msg)
                else:
                    msg = f"Cannot handle object of type '{type(obj)}'"
                    raise TypeError(msg)
                print_msg(fn, type=MsgType.TRACE)
            else:
                raise ValueError(f"'{ptype}' is an invalid ptype.")
