import plotly.graph_objects as go
import pandas as pd
from typing import Self


class PlyWaterfall:
    def __init__(self) -> None:
        self.fig: go.Figure = go.Figure()

    def add_base(
        self,
        data: pd.DataFrame,
        x_year: str,
        x_label: str,
        measure: str,
        y: str,
        text: str,
        base: float,
    ) -> Self:
        fig = go.Figure(
            go.Waterfall(
                x=[data[x_year], data[x_label]],
                measure=data[measure],
                y=data[y],
                textposition="outside",
                text=data[text],
                base=base,
                decreasing={
                    "marker": {"color": "Maroon", "line": {"color": "red", "width": 2}}
                },
                increasing={"marker": {"color": "Teal"}},
                totals={
                    "marker": {
                        "color": "deep sky blue",
                        "line": {"color": "blue", "width": 3},
                    }
                },
            )
        )
        fig.update_layout(waterfallgap=0.3)
        self.fig = fig
        return self

    def add_titles(self, titles: dict[str, str]) -> Self:
        self.fig.update_layout(
            title=titles["title"],
            title_font=dict(size=16, color="navy", family="Verdana"),
        )
        return self

    def add_style(self, styles: dict[str, str]) -> Self:
        self.fig.update_layout(
            plot_bgcolor=styles["plot_bgcolor"], paper_bgcolor=styles["paper_bgcolor"]
        )
        return self
