import pytest
import pandas as pd
# import json

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def df1():
    df = pd.read_json("tests/fixtures/df1.json")
    return df


@pytest.fixture
def df1a():
    df = pd.read_json("tests/fixtures/df1a.json")
    return df


@pytest.fixture
def df2():
    df = pd.read_json("tests/fixtures/df2.json")
    return df
