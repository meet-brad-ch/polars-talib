"""Every function computes exactly what ta-lib-python computes: on the synthetic frame
(leading NaN rows, a null) and on TA-Lib's own 252-bar reference data, on float64 and
float32 input, for TA-Lib's defaults and for a short window. Per-group evaluation gives
per-group results."""

import numpy as np
import numpy.typing as npt
import polars as pl
import pytest
import talib

import polars_talib as plta
from data import frame, talib_reference
from polars_talib._build import DEFAULT_COLUMN, Spec, specs

SHORT_WINDOW = 3
FRAMES = {"synthetic": frame(), "talib-reference": talib_reference()}


def arrays(df: pl.DataFrame, spec: Spec) -> list[npt.NDArray[np.float64]]:
    return [df[DEFAULT_COLUMN.get(c, c)].to_numpy().astype(np.float64) for c in spec.columns]


def assert_same(expr: pl.Expr, df: pl.DataFrame, expected: object) -> None:
    got = df.select(expr.alias("out"))["out"]
    if isinstance(expected, tuple):
        for field, values in zip(got.struct.fields, expected, strict=True):
            np.testing.assert_array_equal(got.struct.field(field).to_numpy(), values)
    else:
        np.testing.assert_array_equal(got.to_numpy(), expected)


@pytest.mark.parametrize("dtype", [pl.Float64, pl.Float32], ids=["f64", "f32"])
@pytest.mark.parametrize("data", FRAMES.values(), ids=FRAMES.keys())
@pytest.mark.parametrize("spec", specs(), ids=lambda s: s.python_name)
def test_equals_talib(data: pl.DataFrame, spec: Spec, dtype: pl.DataType) -> None:
    df = data.cast(dtype)
    fn = getattr(plta, spec.python_name)
    reference = getattr(talib, spec.name)
    assert_same(fn(), df, reference(*arrays(df, spec)))
    if any(p.name == "timeperiod" for p in spec.params):
        assert_same(
            fn(timeperiod=SHORT_WINDOW), df, reference(*arrays(df, spec), timeperiod=SHORT_WINDOW)
        )


@pytest.mark.parametrize("expr", [plta.sma(), plta.macd(), plta.cdldoji(), plta.obv()])
def test_over_groups_evaluates_each_group_alone(ohlcv: pl.DataFrame, expr: pl.Expr) -> None:
    alone = ohlcv.select(expr.alias("out"))
    two = pl.concat([ohlcv.with_columns(pl.lit(s).alias("symbol")) for s in ("A", "B")]).select(
        expr.over("symbol").alias("out")
    )
    assert two.equals(pl.concat([alone, alone]))
