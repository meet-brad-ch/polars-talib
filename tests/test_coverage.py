"""Every TA-Lib function is exposed, and its signature is what TA-Lib declares.

ta-lib-python (``talib``) is the oracle for names, parameters, defaults and outputs; it
reads the same metadata through its own abstract layer. Both are pinned to TA-Lib 0.7.1.
"""

import inspect

import polars as pl
import pytest
import talib
from talib import abstract

import polars_talib as plta
from polars_talib._build import DEFAULT_COLUMN, MODULES, specs

NAMES = [s.name for s in specs()]


def test_same_version_of_talib() -> None:
    assert plta.__talib_version__ == talib.__ta_version__.decode().split(" ")[0]


def test_every_talib_function_is_there_and_nothing_else() -> None:
    assert NAMES == talib.get_functions()
    assert plta.get_functions() == [n.lower() for n in talib.get_functions()]
    assert plta.get_function_groups() == {
        g: [n.lower() for n in names] for g, names in talib.get_function_groups().items()
    }
    assert set(MODULES) == set(talib.get_function_groups())


@pytest.mark.parametrize("name", NAMES)
def test_signature_matches_talib(name: str) -> None:
    info = abstract.Function(name).info  # type: ignore[attr-defined]  # absent from talib's stub
    fn = getattr(plta, name.lower())
    params = inspect.signature(fn).parameters

    expected_columns: list[str] = []
    for key, value in info["input_names"].items():
        expected_columns += value if isinstance(value, list) else [key.replace("price", "real")]
    columns = [p for p in params.values() if isinstance(p.default, pl.Expr)]
    assert [c.name for c in columns] == expected_columns
    for c in columns:
        assert c.default.meta.eq(pl.col(DEFAULT_COLUMN.get(c.name, c.name)))

    values = {p.name: p.default for p in params.values() if not isinstance(p.default, pl.Expr)}
    assert values == dict(info["parameters"])
    assert all(type(values[k]) is type(v) for k, v in info["parameters"].items())

    outputs = fn.__doc__.rsplit(": ", 1)[1].split(", ")
    assert outputs == info["output_names"]
    assert fn.__doc__.startswith(f"{info['display_name']} ({info['group']})")
