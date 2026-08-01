import polars as pl

from .base import SpecsVar
from .specs_group import SpecsGroup


class Specs:
    def __init__(self, name: str, df: pl.DataFrame) -> None:
        self.name = name
        self.df = df

    def __repr__(self) -> str:
        # !r to use the repr() version of the variable (adds quotes)
        msg = f"Specs(name={self.name!r}, df={self.df.shape})"
        return msg

    def __str__(self) -> str:
        msg = f"{self.ngroups} specs groups in the {self.name} specs"
        return msg

    @property
    def group_nms(self) -> tuple[str, ...]:
        nms = tuple(
            self.df.get_column(SpecsVar.GROUP).unique(maintain_order=True).to_list()
        )
        return nms

    @property
    def ngroups(self) -> int:
        return len(self.group_nms)

    def group(self, group_nm: str) -> SpecsGroup:
        group_df = self.df.filter(pl.col(SpecsVar.GROUP).eq(group_nm))
        if group_df.is_empty():
            msg: str = f"Group '{group_nm}' in specs '{self.name}' returns no records."
            raise KeyError(msg)
        return SpecsGroup(group_nm, df=group_df)
