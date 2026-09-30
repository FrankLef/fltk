"""Test the log1ps module."""

import pytest
from pathlib import Path
import random
import polars as pl

from fltk.feathr.feathr import Feathr


@pytest.fixture
def fixtures_path() -> Path:
    return Path(__file__).parent


def sample_df(nrows: int = 5) -> pl.DataFrame:
    random_data = {
        "integers": [random.randint(1, 100) for _ in range(nrows)],
        "floats": [random.random() for _ in range(nrows)],
        "categories": [random.choice(["A", "B", "C"]) for _ in range(nrows)],
    }
    return pl.DataFrame(random_data)


def test_feathr_init(fixtures_path):
    feathr = Feathr(fixtures_path)
    assert isinstance(feathr, Feathr)


def test_feathr_save(fixtures_path):
    feathr = Feathr(fixtures_path)
    names = ["feathr1", "feathr2"]
    for name in names:
        df = sample_df()
        feathr.save(df, name=name)
    assert feathr.names == names


def test_feathr_load(fixtures_path):
    feathr = Feathr(fixtures_path)
    df = feathr.load("feathr1")
    assert df.shape == (5, 3)


def test_feathr_drop_all(fixtures_path):
    feathr = Feathr(fixtures_path)
    n = feathr.drop()
    assert n == 2


def test_feathr_drop(fixtures_path):
    feathr = Feathr(fixtures_path)
    names = ["feathr1", "feathr2"]
    for name in names:
        df = sample_df()
        feathr.save(df, name=name)
    n = feathr.drop(names=["feathr1"])
    assert n == 1
    n = feathr.drop(names=["feathr2"])
    assert n == 1
