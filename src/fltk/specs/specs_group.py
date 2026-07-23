from collections.abc import Sequence
import polars as pl
from typing import NamedTuple

from .base import SpecsVar
from .processor import SpecsProcessor
from .get_namestupl import main as nmstupl


class SpecsGroup:
    def __init__(self, name: str, df: pl.DataFrame) -> None:
        self.name = name
        self.df = df

    def __repr__(self) -> str:
        # !r to use the repr() version of the variable (adds quotes)
        msg = f"SpecsGroup(name={self.name!r}, df={self.df.shape})"
        return msg

    def __str__(self) -> str:
        msg = f"{self.nlines} specs lines in the {self.name} specs group"
        return msg

    @property
    def line_nms(self) -> tuple[str, ...]:
        line_nms = self.df.get_column(SpecsVar.LINE).unique(maintain_order=True)
        return tuple(line_nms)

    @property
    def nlines(self) -> int:
        return len(self.line_nms)

    @property
    def names_tupl(self) -> NamedTuple:
        names_tupl = nmstupl(group_nm=self.name, line_nms=self.line_nms)
        return names_tupl

    def lines(self, line_nms: str | Sequence[str] | None = None) -> SpecsProcessor:
        if line_nms:
            if isinstance(line_nms, str):
                the_lines = self.df.filter(pl.col(SpecsVar.LINE).eq(line_nms))
            else:
                the_lines = self.df.filter(pl.col(SpecsVar.LINE).is_in(line_nms))
        else:
            the_lines = self.df
        return SpecsProcessor(the_lines)
