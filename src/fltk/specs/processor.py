import polars as pl
from typing import Any
from collections.abc import Sequence
import re

from .base import SpecsVar


class SpecsProcessor:
    def __init__(self, df: pl.DataFrame):
        self.df = df

    def get_names(self) -> tuple[str, ...]:
        the_names = tuple(self.df.get_column(SpecsVar.LINE).to_list())
        return the_names

    def get_value(self, item_nm: str) -> dict[str, Any] | Any:
        the_values = {
            row[SpecsVar.LINE]: row[item_nm] for row in self.df.iter_rows(named=True)
        }
        if len(the_values) == 1:
            a_value = next(iter(the_values.values()))
            return a_value
        return the_values

    def get_values(self, item_nms: Sequence[str]) -> dict[str, Any] | Any:
        the_values = {
            row[SpecsVar.LINE]: (row[item_nm] for item_nm in item_nms)
            for row in self.df.iter_rows(named=True)
        }
        return the_values

    def get_split(self, item_nm: str) -> dict[str, Any] | Any:
        def split_it(text: str, sep=","):
            clean_text = re.sub(r"\s", "", text)
            split_text = clean_text.split(sep=sep)
            return tuple(split_text)

        the_splits = {
            row[SpecsVar.LINE]: split_it(row[item_nm])
            for row in self.df.iter_rows(named=True)
        }
        if len(the_splits) == 1:
            a_split = next(iter(the_splits.values()))
            return a_split
        return the_splits

    def filter_role(self, role: str) -> "SpecsProcessor":
        # NOTE: (?i) is for case insensitivity
        pat: str = rf"\b(?i){role}\b"
        filtered_df = self.df.filter(
            pl.col(SpecsVar.ROLE).str.replace_all(r"\s", "").str.contains(pat)
        )
        return SpecsProcessor(filtered_df)

    def filter_rule(self, rule: str) -> "SpecsProcessor":
        # NOTE: (?i) is for case insensitivity
        pat: str = rf"\b(?i){rule}\b"
        filtered_df = self.df.filter(
            pl.col(SpecsVar.RULE).str.replace_all(r"\s", "").str.contains(pat)
        )
        return SpecsProcessor(filtered_df)

    def get_tag(self, item_nm: str, default: dict[str, Any]) -> dict[str, Any] | Any:
        the_tags = {
            row[SpecsVar.LINE]: self.split_tag(tag_text=row[item_nm], default=default)
            for row in self.df.iter_rows(named=True)
        }
        if len(the_tags) == 1:
            a_tag = next(iter(the_tags.values()))
            return a_tag
        return the_tags

    @staticmethod
    def split_tag(
        tag_text: str,
        default: dict[str, Any],
        na: str = "_na",
        sep1: str = "~",
        sep2: str = "=",
    ) -> dict[str, str] | None:
        # NOTE: Must use a special separator not a comma because commas are found in sub text. e.g. mask="{:,.2f}"

        if tag_text is None:
            return None

        if tag_text == na:
            return default

        is_tag = sep2 in tag_text
        if is_tag:
            try:
                tags = dict(item.split(sep2) for item in tag_text.split(sep1))
            except ValueError:
                return None
        else:
            return None
        return tags
