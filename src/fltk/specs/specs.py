import polars as pl

from .base import SpecsVar
from .specs_group import SpecsGroup


class Specs:
    def __init__(self, name: str, df: pl.DataFrame) -> None:
        self.name = name
        self.df = df

    @property
    def group_nms(self) -> tuple[str, ...]:
        group_nms = self.df.get_column(SpecsVar.GROUP).unique(maintain_order=True)
        return tuple(group_nms)

    @property
    def ngroups(self) -> int:
        return len(self.group_nms)

    def group(self, group_nm: str) -> SpecsGroup:
        group_df = self.df.filter(pl.col(SpecsVar.GROUP).eq(group_nm))
        if group_df.is_empty():
            msg: str = f"The group '{group_nm}' returns no records."
            raise KeyError(msg)
        return SpecsGroup(group_nm, df=group_df)
