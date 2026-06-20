from great_tables import GT, html, style as gt_style, loc as gt_loc
import pandas as pd
from typing import Self

from ...graphics.basics import IBaseGeom
from ...graphics.titles import ITitles


class GtRatios:
    def __init__(self, name: str) -> None:
        self.name = str

    def add_base(
        self,
        data: pd.DataFrame,
        rowname_col: str,
        groupname_col: str,
        tab_spanner_label: str,
        num_col_pos: int,
        hidden_cols: list[str] | None = None,
    ) -> Self:
        num_cols = data.columns[num_col_pos:].to_list()
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

    def add_titles(self, titles: ITitles, geom: IBaseGeom) -> Self:
        a_title = titles.title  # type: ignore
        a_subtitle = titles.subtitle  # type: ignore

        a_color: str | None = geom.title.color  # type: ignore[attr-defined]
        a_size: str | None = geom.title.size  # type: ignore[attr-defined]
        a_shape: str | None = geom.title.shape  # type: ignore[attr-defined]
        a_color_sub: str | None = geom.subtitle.color  # type: ignore[attr-defined]
        a_size_sub: str | None = geom.subtitle.size  # type: ignore[attr-defined]
        # a_shape_sub: str | None = geom.subtitle.shape  # type: ignore[attr-defined]

        self.tabl = self.tabl.tab_header(
            title=html(str(a_title)),
            subtitle=html(str(a_subtitle)),
        )

        self.tabl = self.tabl.opt_table_font(a_shape)  # type: ignore
        self.tabl = self.tabl.tab_style(
            style=gt_style.text(color=a_color, size=f"{a_size}px"),
            locations=gt_loc.title(),
        )
        self.tabl = self.tabl.tab_style(
            style=gt_style.text(color=a_color_sub, size=f"{a_size_sub}px"),
            locations=gt_loc.subtitle(),
        )
        return self

    def add_style(self, attrs) -> Self:
        self.tabl = self.tabl.opt_stylize(
            style=attrs.style_no,
            color=attrs.style_color,
            add_row_striping=attrs.row_strip,
        )
        return self
