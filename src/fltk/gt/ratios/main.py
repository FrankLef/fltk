from great_tables import GT, html, style as gt_style, loc as gt_loc
import polars as pl
from typing import Self
from types import SimpleNamespace

title_geom = SimpleNamespace(shape="Arial", size=18, color="navy")
subtitle_geom = SimpleNamespace(shape="Arial", size=14, color="navy")


class GtRatios:
    def __init__(self, name: str) -> None:
        self.name = str
        self._title_geom = title_geom
        self._subtitle_geom = subtitle_geom

    @property
    def title_geom(self) -> SimpleNamespace:
        return self._title_geom

    @title_geom.setter
    def title_geom(self, shape: str, size: int, color: str) -> None:
        self._title_geom.shape = shape
        self._title_geom.size = size
        self._title_geom.color = color

    @property
    def subtitle_geom(self) -> SimpleNamespace:
        return self._subtitle_geom

    @subtitle_geom.setter
    def subtitle_geom(self, shape: str, size: int, color: str) -> None:
        self._subtitle_geom.shape = shape
        self._subtitle_geom.size = size
        self._subtitle_geom.color = color

    def add_base(
        self,
        data: pl.DataFrame,
        rowname_col: str,
        groupname_col: str,
        tab_spanner_label: str,
        num_col_pos: int,
        hidden_cols: list[str] | None = None,
    ) -> Self:
        num_cols = data.columns[num_col_pos:]
        tabl = (
            GT(
                data=data,
                rowname_col=rowname_col,
                groupname_col=groupname_col,
            )
            .tab_spanner(label=tab_spanner_label, columns=num_cols)
            .cols_hide(columns=hidden_cols)
        )
        self.tabl = tabl
        return self

    def add_titles(self, title: str, subtitle: str) -> Self:
        self.tabl = self.tabl.tab_header(
            title=html(str(title)),
            subtitle=html(str(subtitle)),
        )

        a_color = self._title_geom.color
        a_size = self._title_geom.size
        self.tabl = self.tabl.tab_style(
            style=gt_style.text(color=a_color, size=f"{a_size}px"),
            locations=gt_loc.title(),
        )
        a_color = self._subtitle_geom.color
        a_size = self._subtitle_geom.size
        self.tabl = self.tabl.tab_style(
            style=gt_style.text(color=a_color, size=f"{a_size}px"),
            locations=gt_loc.subtitle(),
        )
        return self

    def add_style(self, style: int, color: str, row_strip: bool) -> Self:
        self.tabl = self.tabl.opt_stylize(
            style=style,
            color=color,
            add_row_striping=row_strip,
        )
        return self
