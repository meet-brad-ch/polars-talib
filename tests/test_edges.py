"""Behaviour at the edges: windows longer than the data, invalid parameters, integer
columns, lazy evaluation."""

import polars as pl
import pytest

import polars_talib as plta

SHORT = pl.DataFrame({"close": [1.0, 2.0, 3.0]})


def test_window_longer_than_data_gives_nan_rows_not_an_error() -> None:
    out = SHORT.select(plta.sma(timeperiod=5).alias("s"), plta.macd().alias("m"))
    assert out.height == SHORT.height
    assert out["s"].is_nan().all()
    assert out["m"].struct.unnest().select(pl.all().is_nan().all()).row(0) == (True, True, True)


def test_integer_output_is_zero_before_lookback() -> None:
    out = SHORT.select(plta.maxindex(timeperiod=5).alias("i"))
    assert out["i"].dtype == pl.Int32 and out["i"].to_list() == [0, 0, 0]


def test_invalid_parameter_raises_talib_error() -> None:
    with pytest.raises(pl.exceptions.ComputeError, match="TA_BAD_PARAM"):
        SHORT.select(plta.sma(timeperiod=0))


def test_fraction_for_integer_parameter_is_refused() -> None:
    with pytest.raises(pl.exceptions.ComputeError, match="timeperiod must be an integer"):
        SHORT.select(plta.sma(timeperiod=2.5))  # type: ignore[arg-type]


def test_integer_columns_are_cast(ohlcv: pl.DataFrame) -> None:
    ints = ohlcv.drop_nulls().fill_nan(None).drop_nulls().cast(pl.Int64)
    expected = ints.cast(pl.Float64).select(plta.sma().alias("s"))
    assert ints.select(plta.sma().alias("s")).equals(expected)


def test_lazy_equals_eager(ohlcv: pl.DataFrame) -> None:
    exprs = [plta.sma().alias("s"), plta.bbands().alias("b")]
    eager = ohlcv.select(exprs)
    assert ohlcv.lazy().select(exprs).collect().equals(eager)
    assert ohlcv.lazy().select(exprs).collect(engine="streaming").equals(eager)


def test_column_names_can_be_strings(ohlcv: pl.DataFrame) -> None:
    assert ohlcv.select(plta.sma("high")).equals(ohlcv.select(plta.sma(pl.col("high"))))
