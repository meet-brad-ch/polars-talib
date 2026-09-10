"""Builds the public API from TA-Lib's description of its own functions.

Every TA-Lib function becomes a Python function with a real signature: the input series
first, one parameter per series, then the parameters with TA-Lib's defaults. The body hands
everything to the plugin's single expression, ``call``. Nothing here names a function.
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl
from polars.plugins import register_plugin_function

from . import _polars_talib

PLUGIN = Path(__file__).parent

# TA-Lib group -> module of this package that carries its functions.
MODULES = {
    "Cycle Indicators": "cycle",
    "Math Operators": "math_operators",
    "Math Transform": "math_transform",
    "Momentum Indicators": "momentum",
    "Overlap Studies": "overlap",
    "Pattern Recognition": "pattern",
    "Price Transform": "price_transform",
    "Statistic Functions": "statistic",
    "Volatility Indicators": "volatility",
    "Volume Indicators": "volume",
}

# Column a single-series input reads unless told otherwise (ta-lib-python's convention);
# price components read the column of their own name.
DEFAULT_COLUMN = {"real": "close", "real0": "high", "real1": "low"}


@dataclass(frozen=True)
class Param:
    name: str
    integer: bool
    default: float
    hint: str

    @property
    def value(self) -> int | float:
        return int(self.default) if self.integer else self.default


@dataclass(frozen=True)
class Output:
    name: str
    integer: bool


@dataclass(frozen=True)
class Spec:
    """TA-Lib's description of one function."""

    name: str
    group: str
    hint: str
    columns: tuple[
        str, ...
    ]  # input series in TA-Lib's order: real/real0/real1/periods or price parts
    params: tuple[Param, ...]
    outputs: tuple[Output, ...]

    @property
    def python_name(self) -> str:
        return self.name.lower()

    @property
    def doc(self) -> str:
        lines = [f"{self.hint} ({self.group}), TA-Lib {self.name}.", ""]
        lines += [f"{p.name}: {p.hint} (default {p.value})" for p in self.params]
        outputs = ", ".join(o.name for o in self.outputs)
        lines.append(
            f"Output: {outputs}" if len(self.outputs) == 1 else f"Output struct: {outputs}"
        )
        return "\n".join(lines)


@functools.cache
def specs() -> tuple[Spec, ...]:
    """Every TA-Lib function: groups in ``MODULES`` order, TA-Lib's order within a group
    (the order ta-lib-python lists them in)."""
    groups = list(MODULES)
    described = (
        Spec(
            name=f["name"],
            group=f["group"],
            hint=f["hint"],
            columns=tuple(part for name, parts in f["inputs"] for part in (parts or [name])),
            params=tuple(Param(*p) for p in f["params"]),
            outputs=tuple(Output(*o) for o in f["outputs"]),
        )
        for f in _polars_talib.functions()
    )
    return tuple(sorted(described, key=lambda s: groups.index(s.group)))


def signature(spec: Spec) -> inspect.Signature:
    kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
    columns = [
        inspect.Parameter(c, kind, default=pl.col(DEFAULT_COLUMN.get(c, c)), annotation="IntoExpr")
        for c in spec.columns
    ]
    params = [
        inspect.Parameter(p.name, kind, default=p.value, annotation=int if p.integer else float)
        for p in spec.params
    ]
    return inspect.Signature(columns + params, return_annotation=pl.Expr)


def function(spec: Spec) -> Callable[..., pl.Expr]:
    sig = signature(spec)
    width = len(spec.columns)
    names = [p.name for p in spec.params]

    def call(*args: Any, **kwargs: Any) -> pl.Expr:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        values = list(bound.arguments.values())
        return register_plugin_function(
            args=values[:width],
            plugin_path=PLUGIN,
            function_name="call",
            kwargs={"name": spec.name, "params": dict(zip(names, values[width:], strict=True))},
            is_elementwise=False,
        )

    call.__name__ = call.__qualname__ = spec.python_name
    call.__module__ = f"{__package__}.{MODULES[spec.group]}"
    call.__doc__ = spec.doc
    call.__signature__ = sig  # type: ignore[attr-defined]
    return call


def group(name: str) -> dict[str, Callable[..., pl.Expr]]:
    """The functions of one TA-Lib group, keyed by Python name."""
    return {s.python_name: function(s) for s in specs() if s.group == name}
