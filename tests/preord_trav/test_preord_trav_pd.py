import pytest
from pathlib import Path
import pandas as pd

from fltk.preord_trav.preord_trav_pd import PreordedTraversePd


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent.joinpath("fixtures")


@pytest.fixture
def tree_xl(fixtures_path) -> dict[str, str]:
    out = {"path": fixtures_path.joinpath("XL_Tree.xlsx"), "sheet": "tree_table"}
    return out


@pytest.fixture
def tree_data(tree_xl) -> dict[str, str]:
    data = pd.read_excel(tree_xl["path"], sheet_name=tree_xl["sheet"])
    return data


@pytest.fixture
def preord_trav_pd(tree_data) -> PreordedTraversePd:
    preord_trav_pd = PreordedTraversePd(
        tree_data,
        child="Child",
        parent="Parent",
        level="LevelID",
        left="LeftID",
        right="RightID",
        max_iter=100,
    )
    return preord_trav_pd


def test_preord_pd_trav_calc(preord_trav_pd) -> None:
    preord_trav_pd.fit()
    preord_trav_pd.transform()
    data = preord_trav_pd.data
    assert data["LeftID"].sum() == 146
    assert data["LeftID"].min() == 1
    assert data["RightID"].sum() == 205
    assert data["RightID"].max() == 26


def test_preord_trav_err(tree_data) -> None:
    preord_trav_pd = PreordedTraversePd(
        tree_data,
        child="Child",
        parent="Parent",
        level="LevelID",
        left="LeftID",
        right="RightID",
        max_iter=10,
    )
    with pytest.raises(ValueError):
        preord_trav_pd.fit_transform()
