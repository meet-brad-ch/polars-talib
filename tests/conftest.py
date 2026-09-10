import polars as pl
import pytest

from data import frame


@pytest.fixture(scope="session")
def ohlcv() -> pl.DataFrame:
    return frame()
