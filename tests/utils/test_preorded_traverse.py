import pytest
from pathlib import Path
import polars as pl

# from typing import Any
from fltk.utils.preorded_traverse import PreordedTraverse


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def tree_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("XL_Tree.xlsx"), "sheet": "tree_table"}
    return out


@pytest.fixture
def tree_data(tree_xl) -> dict[str, str]:
    data = pl.read_excel(tree_xl["path"], sheet_name=tree_xl["sheet"])
    return data


@pytest.fixture
def preord_trav(tree_data) -> PreordedTraverse:
    preord_trav = PreordedTraverse(
        tree_data,
        child="Child",
        parent="Parent",
        level="LevelID",
        left="LeftID",
        right="RightID",
        max_iter=100,
    )
    return preord_trav


def test_preord_trav(preord_trav) -> None:
    preord_trav.fit()
    preord_trav.transform()
    data = preord_trav.data
    assert not data.is_empty()
    assert "LevelID" in data.columns
    assert "LeftID" in data.columns
    assert "RightID" in data.columns


def test_preord_trav_calc(preord_trav) -> None:
    preord_trav.fit()
    preord_trav.transform()
    data = preord_trav.data
    assert data["LeftID"].sum() == 146
    assert data["LeftID"].min() == 1
    assert data["RightID"].sum() == 205
    assert data["RightID"].max() == 26
