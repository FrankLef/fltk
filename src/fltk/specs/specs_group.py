from collections.abc import Sequence
import polars as pl
from typing import Any, NamedTuple

from .base import SpecsVar
from .processor import SpecsProcessor
from .get_namestupl import main as nmstupl

type TagsType = dict[str, dict[str, Any]]


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
        nms = tuple(self.df.get_column(SpecsVar.LINE).to_list())
        return nms

    @property
    def nlines(self) -> int:
        return len(self.df.get_column(SpecsVar.LINE))

    @property
    def names_tupl(self) -> NamedTuple:
        if isinstance(self.line_nms, str):
            nms: tuple[str, ...] = tuple(self.line_nms)
        else:
            nms = self.line_nms
        names_tupl = nmstupl(group_nm=self.name, line_nms=nms)
        return names_tupl

    @staticmethod
    def rem_non_dicts(tags: TagsType) -> TagsType:
        """Keep only the tags with a valid dictionnary.

        Args:
            tags (TagsType): Tags obtained using `cols(..., is_lit_val=True)`.

        Returns:
            TagsType: Tags containg only valid dictionnaries.
        """
        out = {key: val for key, val in tags.items() if isinstance(val, dict)}
        return out

    def lines(self, line_nms: str | Sequence[str] | None = None) -> SpecsProcessor:
        """Get lines from the specs with a processor to extract values.

        Args:
            line_nms (str | Sequence[str] | None, optional): Names of lines to select. Defaults to None.

        Returns:
            SpecsProcessor: Processor to obtain the values from the lines.
        """
        if line_nms:
            if isinstance(line_nms, str):
                df = self.df.filter(pl.col(SpecsVar.LINE).eq(line_nms))
            else:
                df = self.df.filter(pl.col(SpecsVar.LINE).is_in(line_nms))
        else:
            df = self.df
        if df.is_empty():
            msg: str = (
                f"Specs group '{self.name}' returns no records for lines '{line_nms}'"
            )
            raise KeyError(msg)
        return SpecsProcessor(df)
