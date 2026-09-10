"""The package surface beyond TA-Lib's functions: hma, stubs, docstrings."""

import inspect
import math

import numpy as np
import polars as pl
import pytest
import talib

import polars_talib as plta
from data import frame, talib_reference
from polars_talib import _stubs
from polars_talib._build import MODULES, PLUGIN, specs


def test_hma_is_the_hull_composition(ohlcv: pl.DataFrame) -> None:
    close = ohlcv["close"].to_numpy()
    raw = 2 * talib.WMA(close, 8) - talib.WMA(close, 16)
    got = ohlcv.select(plta.hma(period=16).alias("h"))["h"].to_numpy()
    np.testing.assert_array_equal(got, talib.WMA(raw, 4))


def test_committed_stubs_are_current() -> None:
    for group, module in MODULES.items():
        stub = (PLUGIN / f"{module}.pyi").read_text(encoding="utf-8")
        assert stub == _stubs.render(group), f"{module}.pyi is stale: python -m polars_talib._stubs"


def test_stub_signatures_match_runtime() -> None:
    for spec in specs():
        fn = getattr(plta, spec.python_name)
        rendered = _stubs._function(spec).split("\n", 1)[0]
        assert rendered.startswith(f"def {spec.python_name}(")
        for p in inspect.signature(fn).parameters.values():
            assert f"{p.name}: " in rendered


def test_each_function_lives_in_its_group_module() -> None:
    for spec in specs():
        fn = getattr(plta, spec.python_name)
        assert fn.__module__ == f"polars_talib.{MODULES[spec.group]}"
        assert fn is getattr(getattr(plta, MODULES[spec.group]), spec.python_name)


def reference_supersmoother(x: np.ndarray, period: float) -> np.ndarray:
    """The recursion as VolCore's engine and AmiBroker's IIR() run it."""
    c1 = 1.41421 * math.pi / period
    c2 = math.exp(-c1)
    a1 = 2.0 * c2 * math.cos(c1)
    a2 = -c2 * c2
    b0 = (1.0 - a1 - a2) / 2.0
    y = x.copy()
    begin = int(np.argmax(~np.isnan(x)))
    for i in range(begin + 2, len(x)):
        y[i] = b0 * x[i] + b0 * x[i - 1] + a1 * y[i - 1] + a2 * y[i - 2]
    return y


@pytest.mark.parametrize("data", [frame(), talib_reference()], ids=["synthetic", "talib-reference"])
@pytest.mark.parametrize("period", [10.0, 40.0])
def test_supersmoother_is_the_ehlers_recursion(data: pl.DataFrame, period: float) -> None:
    got = data.select(plta.supersmoother(period=period).alias("s"))["s"].to_numpy()
    expected = reference_supersmoother(data["close"].to_numpy(), period)
    np.testing.assert_array_equal(got, expected)


def test_supersmoother_refuses_a_non_positive_period() -> None:
    with pytest.raises(pl.exceptions.ComputeError, match="period must be positive"):
        pl.DataFrame({"close": [1.0, 2.0]}).select(plta.supersmoother(period=0.0))
