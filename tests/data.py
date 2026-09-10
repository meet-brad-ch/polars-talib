"""Two frames the tests run on: a synthetic one with the awkward cases real input has
(leading NaN rows, a null in the middle, a ``periods`` column for MAVP), and TA-Lib's own
252-bar daily reference series from its regression tool, real prices with volume."""

import re
from pathlib import Path

import numpy as np
import polars as pl

ROWS = 300
LEADING_NAN = 7
NULL_ROW = 150
SEED = 20260910

TALIB_TEST_DATA = (
    Path(__file__).parents[1] / "ta-lib" / "src" / "tools" / "ta_regtest" / "test_data.c"
)
TALIB_ARRAY = re.compile(r"TA_Real\s+TA_SREF_(\w+)_daily_ref_0_PRIV\[252\]\s*=\s*\{(.*?)\};", re.S)


def talib_reference() -> pl.DataFrame:
    """TA-Lib's ``*_daily_ref_0`` arrays: open, high, low, close, volume, 252 bars."""
    columns = {
        name: np.array(re.split(r"[,\s]+", body.strip()), dtype=np.float64)
        for name, body in TALIB_ARRAY.findall(TALIB_TEST_DATA.read_text())
    }
    assert list(columns) == ["open", "high", "low", "close", "volume"], list(columns)
    rng = np.random.default_rng(SEED)
    columns["periods"] = rng.integers(2, 30, 252).astype(np.float64)
    return pl.DataFrame(columns)


def frame() -> pl.DataFrame:
    rng = np.random.default_rng(SEED)
    close = 100.0 + np.cumsum(rng.normal(0.0, 1.0, ROWS))
    spread = rng.uniform(0.1, 2.0, ROWS)
    columns = {
        "open": close - rng.uniform(-1.0, 1.0, ROWS),
        "high": close + spread,
        "low": close - spread,
        "close": close,
        "volume": rng.integers(1_000, 100_000, ROWS).astype(np.float64),
        "periods": rng.integers(2, 30, ROWS).astype(np.float64),
    }
    for values in columns.values():
        values[:LEADING_NAN] = np.nan
    df = pl.DataFrame(columns)
    return df.with_columns(
        pl.when(pl.int_range(pl.len()) == NULL_ROW)
        .then(None)
        .otherwise(pl.col("close"))
        .alias("close")
    )
