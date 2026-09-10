"""The package surface beyond TA-Lib's functions: hma, stubs, docstrings."""

import inspect

import numpy as np
import polars as pl
import talib

import polars_talib as plta
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
