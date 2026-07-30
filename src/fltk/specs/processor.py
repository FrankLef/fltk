import polars as pl
from typing import Any
from collections.abc import Sequence
import ast

from .base import SpecsVar

type TagsType = dict[str, dict[str, Any]]


class SpecsProcessor:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    @property
    def line_nms(self) -> tuple[str, ...]:
        line_nms = self.df.get_column(SpecsVar.LINE).to_list()
        return tuple(line_nms)

    @property
    def nlines(self) -> int:
        return len(self.line_nms)

    def cols(
        self, col_nms: str | Sequence[str] | None = None, is_lit_eval: bool = False
    ) -> Any:
        """Get the columnar values from the specs.

        Args:
            col_nms (str | Sequence[str] | None, optional): Column names. Defaults to None.
            is_lit_eval (bool, optional): True will cause the content to be read by `ast.literal_eval()` from Python. Defaults to False.

        Returns:
            Any: Columnar values in a format easy to use in python scripts.
        """
        if col_nms:
            col_nms = (col_nms,) if isinstance(col_nms, str) else col_nms
            cols = [SpecsVar.LINE] + list(col_nms)
            df = self.df.select(cols)
            if df.height == 1:
                if df.width == 2:
                    out = df.to_dicts()[0]
                    out = out[col_nms[0]]
                    if is_lit_eval:
                        out = self.get_lit_eval(out)

                else:
                    out = df.rows_by_key(key=[SpecsVar.LINE], named=True, unique=True)
                    out = next(iter(out.values()))
                    if is_lit_eval:
                        out = {key: self.get_lit_eval(val) for key, val in out.items()}
            else:
                if df.width == 2:
                    out = df.rows_by_key(key=[SpecsVar.LINE], named=True, unique=True)
                    combined_out = {}
                    for key, val in out.items():
                        combined_out[key] = val[col_nms[0]]
                    out = combined_out
                    if is_lit_eval:
                        out = {key: self.get_lit_eval(val) for key, val in out.items()}
                else:
                    out = df.rows_by_key(key=[SpecsVar.LINE], named=True, unique=True)
        else:
            out = self.df.rows_by_key(key=[SpecsVar.LINE], named=True, unique=True)
        return out

    def get_lit_eval(self, val: Any) -> Any:
        text: str = str(val)
        try:
            out: Any = ast.literal_eval(text)
        except ValueError:
            out = text
        return out

    @staticmethod
    def keep_dicts(tags: TagsType) -> TagsType:
        """Keep only the tags with a valid dictionnary.

        Args:
            tags (TagsType): Tags obtained using `cols(..., is_lit_val=True)`.

        Returns:
            TagsType: Tags containg only valid dictionnaries.
        """
        out = {key: val for key, val in tags.items() if isinstance(val, dict)}
        return out

    def filter_role(self, role: str) -> "SpecsProcessor":
        """Filter the specs by role.

        Args:
            role (str): Role name used as a filter.

        Returns:
            SpecsProcessor: Filtered specs by role.
        """
        # NOTE: (?i) is for case insensitivity
        pat: str = rf"\b(?i){role}\b"
        filtered_df = self.df.filter(
            pl.col(SpecsVar.ROLE).str.replace_all(r"\s", "").str.contains(pat)
        )
        return SpecsProcessor(filtered_df)

    def filter_rule(self, rule: str) -> "SpecsProcessor":
        """Filter the specs by rule.

        Args:
            rule (str): Rule name used as a filter.

        Returns:
            SpecsProcessor: Filtered specs by rule.
        """
        # NOTE: (?i) is for case insensitivity
        pat: str = rf"\b(?i){rule}\b"
        filtered_df = self.df.filter(
            pl.col(SpecsVar.RULE).str.replace_all(r"\s", "").str.contains(pat)
        )
        return SpecsProcessor(filtered_df)
