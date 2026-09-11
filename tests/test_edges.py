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


def test_chunked_input_equals_contiguous_input(ohlcv: pl.DataFrame) -> None:
    half = ohlcv.height // 2
    chunked = pl.concat([ohlcv.head(half), ohlcv.tail(ohlcv.height - half)], rechunk=False)
    assert chunked["close"].n_chunks() == 2
    exprs = [plta.sma().alias("s"), plta.ema().alias("e"), plta.macd().alias("m")]
    assert chunked.select(exprs).equals(ohlcv.select(exprs))


def test_sliced_frame_reads_the_buffer_from_its_offset(ohlcv: pl.DataFrame) -> None:
    """A slice shares the parent's buffer at an offset; the borrowed input must honour it."""
    part = ohlcv.slice(20, 200)
    exprs = [plta.sma().alias("s"), plta.maxindex().alias("i")]
    fresh = pl.DataFrame(part.to_dict())  # same values in buffers of their own
    assert part.select(exprs).equals(fresh.select(exprs))


def test_chunks_with_and_without_nulls(ohlcv: pl.DataFrame) -> None:
    """One chunk carries a validity bitmap, the other does not; nulls must land in place."""
    clean = ohlcv.tail(100)
    chunked = pl.concat([ohlcv.head(200), clean], rechunk=False)
    assert chunked["close"].null_count() == 1 and chunked["close"].n_chunks() == 2
    exprs = [plta.sma().alias("s"), plta.macd().alias("m")]
    assert chunked.select(exprs).equals(chunked.rechunk().select(exprs))


def test_all_null_column_gives_nan_rows() -> None:
    df = pl.DataFrame({"close": pl.Series([None] * 10, dtype=pl.Float64)})
    out = df.select(plta.sma(timeperiod=3).alias("s"), plta.maxindex(timeperiod=3).alias("i"))
    assert out["s"].is_nan().all() and out["i"].to_list() == [0] * 10


def test_over_interleaved_groups_equals_contiguous(ohlcv: pl.DataFrame) -> None:
    """Interleaved groups are gathered into fresh series; the result must not depend on it."""
    two = pl.concat([ohlcv.with_columns(pl.lit(s).alias("symbol")) for s in ("A", "B")])
    two = two.with_columns(pl.int_range(pl.len()).alias("row"))
    interleaved = two.sort(pl.col("row") % ohlcv.height, "symbol")
    exprs = [plta.ema().over("symbol").alias("e"), plta.macd().over("symbol").alias("m")]
    got = interleaved.with_columns(exprs).sort("row")
    assert got.select("e", "m").equals(two.with_columns(exprs).select("e", "m"))
