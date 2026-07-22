from collections.abc import Sequence
import polars as pl

from .processor import SpecsProcessor
from .base import SpecsVar


class SpecsGroup:
    def __init__(self, df: pl.DataFrame) -> None:
        self.df = df

    @property
    def line_nms(self) -> tuple[str, ...]:
        line_nms = self.df.get_column(SpecsVar.LINE).unique(maintain_order=True)
        return tuple(line_nms)

    @property
    def nlines(self) -> int:
        return len(self.line_nms)

    def lines(self, line_nms: str | Sequence[str] | None = None) -> SpecsProcessor:
        if line_nms:
            if isinstance(line_nms, str):
                the_lines = self.df.filter(pl.col(SpecsVar.LINE).eq(line_nms))
            else:
                the_lines = self.df.filter(pl.col(SpecsVar.LINE).is_in(line_nms))
        else:
            the_lines = self.df
        return SpecsProcessor(the_lines)
